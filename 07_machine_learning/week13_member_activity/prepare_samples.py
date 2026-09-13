"""Week 13: prepare labeled training and validation snapshots.

The learner drafted the filter with support and supplied the label expression.
Read only development_raw.csv and rebuild two derived development CSV files.
No model is fitted. Raw input files are never overwritten.
Test features and held-out test labels are not opened.
"""

from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "data" / "development_raw.csv"
FEATURE_COLUMNS = ["past_active_days_7d", "past_order_count_7d"]
TARGET_COLUMN = "inactive_next_7d"


def main():
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    # Keep members valid at prediction time and outcomes that are known.
    # A recorded zero is a known outcome and must remain eligible.
    eligible = df[
        (df["status_at_prediction"] == "valid")
        & (df["future_active_days_7d"].notnull())
    ]

    # Label expression supplied by the learner.
    y = (eligible["future_active_days_7d"] == 0).astype(int)

    # Keep traceability keys, the two agreed inputs, and the target.
    # Work on a copy so adding a target does not modify the raw DataFrame.
    prepared = eligible[["member_id", "prediction_date"] + FEATURE_COLUMNS].copy()
    prepared[TARGET_COLUMN] = y

    # Follow the time allocation already decided by the learner.
    train = prepared[
        prepared["prediction_date"].isin(["2026-06-01", "2026-07-01"])
    ]
    valid = prepared[prepared["prediction_date"] == "2026-08-01"]

    print("SIMULATED DEVELOPMENT DATA ONLY")
    print("raw_rows:", len(df))
    print("eligible_rows:", len(eligible))
    print("excluded_rows:", len(df) - len(eligible))
    print(
        "eligible_zero_active_days_rows:",
        int((eligible["future_active_days_7d"] == 0).sum()),
    )
    print("eligible_rows_by_batch:")
    print(eligible.groupby("prediction_date").size().to_string())
    print("y_dtype:", y.dtype)
    print("development_label_counts:")
    print(y.value_counts().sort_index().to_string())
    print("train_rows:", len(train))
    print("train_label_counts:")
    print(train[TARGET_COLUMN].value_counts().sort_index().to_string())
    print("validation_rows:", len(valid))
    print("validation_label_counts:")
    print(valid[TARGET_COLUMN].value_counts().sort_index().to_string())

    # Re-running rebuilds only these two generated files, not the raw data.
    train_path = DATA_PATH.parent / "development_train.csv"
    valid_path = DATA_PATH.parent / "development_valid.csv"
    train.to_csv(train_path, index=False, encoding="utf-8-sig")
    valid.to_csv(valid_path, index=False, encoding="utf-8-sig")
    print("saved_train:", train_path)
    print("saved_validation:", valid_path)
    print("Only the two derived development CSV files were written.")
    print("Raw data files were not changed. No model was trained.")
    print("Test features and test labels were not opened.")


if __name__ == "__main__":
    main()
