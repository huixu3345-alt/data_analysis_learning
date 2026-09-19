from pathlib import Path
import pandas as pd

file_path = Path(__file__).resolve().parent / "inputs" / "sales_clean_week12.csv"
df = pd.read_csv(file_path)

valid_df = df[df["sales_amount_valid"] == "True"]

result = valid_df.groupby("channel", as_index=False).agg(
    valid_net_sales=("net_sales", "sum"),
    valid_order_count=("order_id", "size")
)
print(result)
