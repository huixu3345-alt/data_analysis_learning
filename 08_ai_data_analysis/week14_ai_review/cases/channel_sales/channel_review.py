from pathlib import Path
import pandas as pd

file_path = Path(__file__).resolve().parent / "inputs" / "sales_clean_week12.csv"
df = pd.read_csv(file_path)

valid_df = df[df["sales_amount_valid"] == True]

result = valid_df.groupby("channel", as_index=False).agg(
    valid_net_sales=("net_sales", "sum"),
    valid_order_count=("order_id", "size")
)
result["valid_net_sales"] = result["valid_net_sales"].round(2)

# 总体汇总
total_net_sales = valid_df["net_sales"].sum().round(2)
total_valid_orders = valid_df.shape[0]

# 对账
check_sales = result["valid_net_sales"].sum().round(2) == total_net_sales
check_order = result["valid_order_count"].sum() == total_valid_orders

print(result.to_string(index=False))
print("channel_net_sales:", result["valid_net_sales"].sum().round(2))
print("total_net_sales:", total_net_sales)
print("channel_orders:", result["valid_order_count"].sum())
print("total_orders:", total_valid_orders)
print("sales_check:", check_sales)
print("orders_check:", check_order)
