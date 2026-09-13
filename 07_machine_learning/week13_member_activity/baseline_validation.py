"""Evaluate a majority-class baseline on simulated development data only.

The learner completed fit and predict with structural prompts.
Data loading and metric reporting are teaching scaffolding.
No test data is opened and no files are written.
"""

from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score


DATA_DIR = Path(__file__).resolve().parent / "data"
FEATURE_COLUMNS = ["past_active_days_7d", "past_order_count_7d"]
TARGET_COLUMN = "inactive_next_7d"


def main():
    train = pd.read_csv(DATA_DIR / "development_train.csv", encoding="utf-8-sig")
    valid = pd.read_csv(DATA_DIR / "development_valid.csv", encoding="utf-8-sig")

    if train.empty or valid.empty:
        raise ValueError("Training and validation data must both be nonempty.")
    if not train["prediction_date"].isin(["2026-06-01", "2026-07-01"]).all():
        raise ValueError("Training dates must follow the agreed June/July split.")
    if not valid["prediction_date"].eq("2026-08-01").all():
        raise ValueError("Validation must contain August snapshots only.")
    for frame in (train, valid):
        if not frame[TARGET_COLUMN].isin([0, 1]).all():
            raise ValueError("Labels must be known binary values: 0 or 1.")
        if frame[FEATURE_COLUMNS].isna().any().any():
            raise ValueError("Missing features require a training-only handling plan.")

    # Traceability keys and the future outcome are not model inputs.
    X_train = train[FEATURE_COLUMNS]
    y_train = train[TARGET_COLUMN]
    X_valid = valid[FEATURE_COLUMNS]
    y_valid = valid[TARGET_COLUMN]

    # Learn the most frequent TRAINING label, not the validation majority.
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)
    baseline_pred = baseline.predict(X_valid)

    print("SIMULATED DATA: DEVELOPMENT BASELINE ONLY")
    print("label: 0 = active at least once; 1 = completely inactive next 7 days")
    print("train_rows:", len(train))
    print("train_label_counts:")
    print(y_train.value_counts().sort_index().to_string())
    print("validation_rows:", len(valid))
    print("validation_label_counts:")
    print(y_valid.value_counts().sort_index().to_string())
    print("baseline_prediction_counts:")
    print(pd.Series(baseline_pred).value_counts().sort_index().to_string())

    # Metrics use class 1 (future inactivity) as the positive class.
    cm = confusion_matrix(y_valid, baseline_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    print("confusion_matrix: rows=true, columns=predicted, labels=[0, 1]")
    print(cm)
    print("accuracy:", round(accuracy_score(y_valid, baseline_pred), 4))
    precision = round(tp / (tp + fp), 4) if tp + fp else "undefined: no predicted class 1"
    recall = round(tp / (tp + fn), 4) if tp + fn else "undefined: no actual class 1"
    f1 = round(2 * tp / (2 * tp + fp + fn), 4) if 2 * tp + fp + fn else "undefined: no actual or predicted class 1"
    print("precision:", precision)
    print("recall:", recall)
    print("f1:", f1)

    # AUC takes scores rather than thresholded predictions.
    classes = list(baseline.classes_)
    if 1 in classes:
        inactive_probability = baseline.predict_proba(X_valid)[:, classes.index(1)]
    else:
        inactive_probability = [0.0] * len(X_valid)
    if y_valid.nunique() == 2:
        print("roc_auc:", round(roc_auc_score(y_valid, inactive_probability), 4))
    else:
        print("roc_auc: undefined: validation contains only one class")
    print("Baseline fitted using training data; evaluated on validation only.")
    print("No files were written. Test features and test labels were not opened.")
    print("Simulated validation results are not evidence of real business impact.")


if __name__ == "__main__":
    main()
