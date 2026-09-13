"""Compare two classifiers on simulated development snapshots only.

Teacher-provided comparison scaffolding follows the learner's supported
fit/predict exercise. No threshold search, test-data access, or file writes.
"""

from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score


DATA_DIR = Path(__file__).resolve().parent / "data"
FEATURE_COLUMNS = ["past_active_days_7d", "past_order_count_7d"]
TARGET_COLUMN = "inactive_next_7d"


def format_metric(value):
    return "undefined" if value is None else f"{value:.4f}"


def main():
    train = pd.read_csv(DATA_DIR / "development_train.csv", encoding="utf-8-sig")
    valid = pd.read_csv(DATA_DIR / "development_valid.csv", encoding="utf-8-sig")
    if train.empty or valid.empty:
        raise ValueError("Training and validation data must both be nonempty.")
    if not train["prediction_date"].isin(["2026-06-01", "2026-07-01"]).all():
        raise ValueError("Training must use the agreed June/July snapshots.")
    if not valid["prediction_date"].eq("2026-08-01").all():
        raise ValueError("Validation must use August snapshots only.")
    for frame in (train, valid):
        if not frame[TARGET_COLUMN].isin([0, 1]).all():
            raise ValueError("Labels must be known binary values: 0 or 1.")
        if frame[FEATURE_COLUMNS].isna().any().any():
            raise ValueError("Missing features require a training-only handling plan.")
    if train[TARGET_COLUMN].nunique() != 2:
        raise ValueError("Logistic regression requires both training classes.")

    X_train = train[FEATURE_COLUMNS]
    y_train = train[TARGET_COLUMN]
    X_valid = valid[FEATURE_COLUMNS]
    y_valid = valid[TARGET_COLUMN]

    # Both models see exactly the same training and validation inputs.
    # max_iter is a solver iteration cap, not a classification threshold.
    models = [
        ("majority", DummyClassifier(strategy="most_frequent")),
        ("logistic", LogisticRegression(max_iter=1000)),
    ]
    metric_rows = []
    count_rows = []
    for name, model in models:
        # Same fit/predict pattern as the learner's completed exercise.
        model.fit(X_train, y_train)
        predictions = model.predict(X_valid)
        positive_column = list(model.classes_).index(1)
        inactive_probability = model.predict_proba(X_valid)[:, positive_column]

        cm = confusion_matrix(y_valid, predictions, labels=[0, 1])
        tn, fp, fn, tp = (int(value) for value in cm.ravel())
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
        auc = roc_auc_score(y_valid, inactive_probability) if y_valid.nunique() == 2 else None
        metric_rows.append({
            "model": name,
            "accuracy": format_metric(accuracy_score(y_valid, predictions)),
            "precision": format_metric(precision),
            "recall": format_metric(recall),
            "f1": format_metric(f1),
            "roc_auc": format_metric(auc),
        })
        count_rows.append({
            "model": name,
            "flagged": tp + fp,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
        })

    print("SIMULATED DATA: TRAIN/VALIDATION COMPARISON ONLY")
    print("train_rows:", len(train))
    print("train_label_counts:")
    print(y_train.value_counts().sort_index().to_string())
    print("validation_rows:", len(valid))
    print("validation_label_counts:")
    print(y_valid.value_counts().sort_index().to_string())
    print("\nVALIDATION METRICS (class 1 = completely inactive next 7 days)")
    print(pd.DataFrame(metric_rows).to_string(index=False))
    print("\nVALIDATION COUNTS")
    print(pd.DataFrame(count_rows).to_string(index=False))
    print("flagged=predicted 1; tp=correct flags; fp=false alarms; fn=misses; tn=correct negatives")
    print("undefined means the metric denominator is zero or AUC lacks both classes.")
    print("Default predict rules used. No threshold search was performed.")
    print("No files were written. Test features and test labels were not opened.")
    print("These simulated validation results do not establish real business impact.")


if __name__ == "__main__":
    main()
