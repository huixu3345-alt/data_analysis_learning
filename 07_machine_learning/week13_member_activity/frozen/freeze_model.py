"""Build frozen model artifacts from DEVELOPMENT data only.

Teacher-provided persistence scaffolding. The learner runs this script.
Test features and test labels are never opened here. No metrics are evaluated.
"""

import hashlib
import io
import json
import platform
import sys
import tempfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression


CASE_DIR = Path(__file__).resolve().parent
DATA_DIR = CASE_DIR / "data"
FROZEN_DIR = CASE_DIR / "frozen"


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def write_new(path, content):
    with path.open("xb") as stream:
        stream.write(content)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")


def label_counts(frame, target):
    return {str(int(label)): int(count) for label, count in frame[target].value_counts().sort_index().items()}


def main():
    if FROZEN_DIR.exists():
        raise FileExistsError("Frozen artifacts already exist. Do not overwrite or rebuild them after seeing test results.")

    plan_bytes = (CASE_DIR / "frozen_plan.json").read_bytes()
    plan = json.loads(plan_bytes)
    if plan["decision_status"] != "learner_confirmed_before_test_access":
        raise ValueError("A learner-confirmed plan is required before freezing.")
    if plan["feature_columns"] != ["past_active_days_7d", "past_order_count_7d"]:
        raise ValueError("Feature columns differ from the confirmed comparison.")
    if plan["threshold"] != 0.4 or plan["positive_class"] != 1:
        raise ValueError("The confirmed decision is class-1 probability >= 0.4.")
    if plan["main_parameters"] != {"max_iter": 1000}:
        raise ValueError("Estimator settings differ from the confirmed comparison.")
    if plan["baseline_parameters"] != {"strategy": "most_frequent"}:
        raise ValueError("Baseline settings differ from the confirmed comparison.")

    # Hash and parse exactly the same source bytes, then preserve them below.
    train_bytes = (DATA_DIR / "development_train.csv").read_bytes()
    valid_bytes = (DATA_DIR / "development_valid.csv").read_bytes()
    train = pd.read_csv(io.BytesIO(train_bytes), encoding="utf-8-sig")
    valid = pd.read_csv(io.BytesIO(valid_bytes), encoding="utf-8-sig")
    features = plan["feature_columns"]
    target = plan["target_column"]
    expected_dates = [(train, ["2026-06-01", "2026-07-01"], 524), (valid, ["2026-08-01"], 256)]
    for frame, dates, expected_rows in expected_dates:
        if len(frame) != expected_rows or set(frame["prediction_date"]) != set(dates):
            raise ValueError("Development rows or dates differ from the confirmed evidence. Stop and investigate before freezing.")
        if frame.duplicated(["member_id", "prediction_date"]).any():
            raise ValueError("Duplicate member/date snapshots are not allowed.")
        if not frame[target].isin([0, 1]).all():
            raise ValueError("Training and validation labels must be known binary values.")
        if frame[features].isna().any().any():
            raise ValueError("Missing features need an explicit plan; do not silently change preprocessing.")
    if train[target].nunique() != 2:
        raise ValueError("Logistic regression needs both training classes.")

    # Preserve the established training split. Validation is NOT added to fit.
    X_train = train[features]
    y_train = train[target]
    model = LogisticRegression(**plan["main_parameters"])
    model.fit(X_train, y_train)
    baseline = DummyClassifier(**plan["baseline_parameters"])
    baseline.fit(X_train, y_train)

    # Publish a complete directory only after all artifact writes succeed.
    # On failure, a uniquely named staging directory is retained, not deleted.
    staging = Path(tempfile.mkdtemp(prefix=".freeze-stage-", dir=CASE_DIR))
    snapshots = {
        "frozen_plan.json": plan_bytes,
        "development_train.csv": train_bytes,
        "development_valid.csv": valid_bytes,
        "freeze_model.py": Path(__file__).read_bytes(),
    }
    for name, content in snapshots.items():
        write_new(staging / name, content)
    bundle = {
        "case_id": plan["case_id"],
        "main_model": model,
        "baseline_model": baseline,
        "feature_columns": features,
        "target_column": target,
        "positive_class": 1,
        "threshold": 0.4,
        "comparison_operator": ">=",
    }
    model_path = staging / "models.joblib"
    with model_path.open("xb") as stream:
        joblib.dump(bundle, stream)
    hashes = {name: sha256(content) for name, content in snapshots.items()}
    hashes["models.joblib"] = sha256(model_path.read_bytes())
    metadata = {
        "case_id": plan["case_id"],
        "data_scope": "simulated_development_only",
        "fit_policy": "June/July training only; no validation refit",
        "training_rows": len(train),
        "validation_rows": len(valid),
        "training_label_counts": label_counts(train, target),
        "validation_label_counts": label_counts(valid, target),
        "feature_dtypes": {column: str(train[column].dtype) for column in features},
        "main_effective_parameters": model.get_params(deep=False),
        "baseline_effective_parameters": baseline.get_params(deep=False),
        "main_classes": [int(value) for value in model.classes_],
        "environment": {
            "python": platform.python_version(),
            "python_executable": sys.executable,
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "joblib": joblib.__version__,
        },
        "sha256": hashes,
        "test_files_opened": False,
        "evaluation_performed": False,
    }
    write_new(staging / "metadata.json", json_bytes(metadata))
    staging.rename(FROZEN_DIR)

    print("FROZEN ARTIFACTS CREATED FROM SIMULATED DEVELOPMENT DATA")
    print("frozen_dir:", FROZEN_DIR)
    print("train_rows:", len(train))
    print("train_label_counts:", metadata["training_label_counts"])
    print("validation_rows:", len(valid))
    print("feature_columns:", features)
    print("decision_rule: class-1 probability >= 0.4")
    print("model_sha256:", hashes["models.joblib"])
    print("Saved models, plan, development snapshots, source, versions, and SHA-256 fingerprints.")
    print("Both models were fitted on June/July training data only.")
    print("Validation data was archived, not added to training. No evaluation was performed.")
    print("Test features and test labels were not opened. Do not overwrite this frozen directory.")


if __name__ == "__main__":
    main()
