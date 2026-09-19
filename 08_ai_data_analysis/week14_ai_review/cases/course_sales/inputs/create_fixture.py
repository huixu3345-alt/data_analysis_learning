"""Prepare simulated teaching inputs only; contains no analysis or solution query."""

from pathlib import Path
import csv
import hashlib
import json
import sqlite3

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "course_sales_review.db"
ORDER_COLUMNS = ["order_id", "course_category", "payment_status", "paid_amount"]
REFUND_COLUMNS = ["refund_id", "order_id", "refund_amount"]

ORDERS = [
    ("C1001", "Python", "已支付", 1000),
    ("C1002", "Python", "已支付", 800),
    ("C1003", "SQL", "已支付", 600),
    ("C1004", "SQL", "已支付", 1200),
    ("C1005", "BI", "已支付", 1500),
    ("C1006", "BI", "已支付", 900),
    ("C1007", "Python", "未支付", 0),
    ("C1008", "SQL", "未支付", 0),
]
REFUNDS = [
    ("RF001", "C1001", 200),
    ("RF002", "C1001", 100),
    ("RF003", "C1003", 600),
    ("RF004", "C1004", 100),
    ("RF005", "C1004", 200),
    ("RF006", "C1006", 150),
]

outputs = [DATABASE, ROOT / "course_orders.csv", ROOT / "course_refunds.csv", ROOT / "manifest.json"]
if any(path.exists() for path in outputs):
    raise SystemExit("Teaching inputs already exist; refusing to replace them.")

with sqlite3.connect(DATABASE) as connection:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript("""
        CREATE TABLE course_orders (
            order_id TEXT PRIMARY KEY NOT NULL,
            course_category TEXT NOT NULL,
            payment_status TEXT NOT NULL CHECK(payment_status IN ('已支付', '未支付')),
            paid_amount REAL NOT NULL CHECK(paid_amount >= 0)
        );
        CREATE TABLE course_refunds (
            refund_id TEXT PRIMARY KEY NOT NULL,
            order_id TEXT NOT NULL REFERENCES course_orders(order_id),
            refund_amount REAL NOT NULL CHECK(refund_amount >= 0)
        );
    """)
    connection.executemany("INSERT INTO course_orders VALUES (?, ?, ?, ?)", ORDERS)
    connection.executemany("INSERT INTO course_refunds VALUES (?, ?, ?)", REFUNDS)
    connection.commit()
    schemas = {
        table: [dict(zip(("cid", "name", "type", "notnull", "default", "pk"), row))
                for row in connection.execute(f"PRAGMA table_info({table})")]
        for table in ("course_orders", "course_refunds")
    }
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    foreign_key_issues = connection.execute("PRAGMA foreign_key_check").fetchall()
    assert integrity == "ok" and not foreign_key_issues
    assert connection.execute("SELECT * FROM course_orders ORDER BY order_id").fetchall() == ORDERS
    assert connection.execute("SELECT * FROM course_refunds ORDER BY refund_id").fetchall() == REFUNDS

for filename, columns, rows in (
    ("course_orders.csv", ORDER_COLUMNS, ORDERS),
    ("course_refunds.csv", REFUND_COLUMNS, REFUNDS),
):
    with (ROOT / filename).open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(rows)

manifest = {
    "purpose": "Week 14 session 5 / W14-I simulated classroom inputs",
    "real_business_data": False,
    "currency_unit": "CNY yuan",
    "tables": {
        "course_orders": {"rows": len(ORDERS), "grain": "one order", "schema": schemas["course_orders"]},
        "course_refunds": {"rows": len(REFUNDS), "grain": "one successful refund transaction", "schema": schemas["course_refunds"]},
    },
    "integrity_check": integrity,
    "foreign_key_issues": foreign_key_issues,
    "files": {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in outputs if path.name != "manifest.json"
    },
    "analysis_executed": False,
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, ensure_ascii=False, indent=2))
