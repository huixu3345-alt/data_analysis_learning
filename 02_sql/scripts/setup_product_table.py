from pathlib import Path
import sqlite3


# 当前脚本位于 02_sql/scripts
# parents[1] 表示向上两层，得到 02_sql 文件夹
SQL_DIR = Path(__file__).resolve().parents[1]

# SQLite数据库文件位置
DATABASE_FILE = SQL_DIR / "data" / "sales_week4.db"


# 商品基础资料
product_data = [
    ("无线鼠标", "电脑配件", 60),
    ("机械键盘", "电脑配件", 180),
    ("蓝牙耳机", "数码产品", 120),
    ("移动硬盘", "数码产品", 300),
    ("显示器", "电脑配件", 700),
]


# 连接数据库
with sqlite3.connect(DATABASE_FILE) as conn:

    # 如果以前创建过product_info，先删除，保证脚本可以重复运行
    conn.execute("DROP TABLE IF EXISTS product_info")

    # 创建商品信息表
    conn.execute(
        """
        CREATE TABLE product_info (
            product_name TEXT PRIMARY KEY,
            standard_category TEXT,
            standard_cost REAL
        )
        """
    )

    # 一次插入多条商品资料
    conn.executemany(
        """
        INSERT INTO product_info (
            product_name,
            standard_category,
            standard_cost
        )
        VALUES (?, ?, ?)
        """,
        product_data,
    )

    # 保存修改
    conn.commit()

    # 检查实际写入的商品数量
    product_count = conn.execute(
        "SELECT COUNT(*) FROM product_info"
    ).fetchone()[0]


print("商品信息表创建完成")
print("数据库：", DATABASE_FILE)
print("商品数量：", product_count)