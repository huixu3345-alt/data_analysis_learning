"""Evaluate the frozen classifiers once on the September holdout.

The learner runs this teacher-provided evaluation scaffolding.
Predictions are persisted before outcome labels are read. Re-running after
completion displays the saved report without re-evaluating the holdout.
"""

import hashlib
import io
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import confusion_matrix, roc_auc_score


CASE_DIR = Path(__file__).resolve().parent
DATA_DIR = CASE_DIR / "data"
FROZEN_DIR = CASE_DIR / "frozen"
OUTPUT_DIR = CASE_DIR / "final_test"
KEYS = ["member_id", "prediction_date"]
FEATURES = ["past_active_days_7d", "past_order_count_7d"]
OUTCOME = "future_active_days_7d"
EXPECTED_MODEL_SHA256 = "d266ffb052659184e2c1a6c688fbc98dcfce46978248765bbfc6129087a79266"


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")


def write_new(path, content):
    with path.open("xb") as stream:
        stream.write(content)


def csv_bytes(frame):
    return frame.to_csv(index=False).encode("utf-8-sig")


def score_predictions(y, predictions, probabilities):
    if len(y):
        cm = confusion_matrix(y, predictions, labels=[0, 1])
        tn, fp, fn, tp = (int(value) for value in cm.ravel())
    else:
        tn = fp = fn = tp = 0
    return {
        "evaluated_rows": len(y),
        "flagged_evaluated": tp + fp,
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "confusion_matrix": [[tn, fp], [fn, tp]],
        "accuracy": (tp + tn) / len(y) if len(y) else None,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None,
        "roc_auc": float(roc_auc_score(y, probabilities)) if y.nunique() == 2 else None,
    }


def show_report(report, cached=False):
    print("SAVED REPORT ONLY; NO NEW EVALUATION" if cached else "FROZEN SEPTEMBER TEST EVALUATION COMPLETED")
    print("SIMULATED DATA ONLY; NOT EVIDENCE OF REAL BUSINESS IMPACT")
    print("rule: frozen logistic model, class-1 probability >= 0.4")
    for name, value in report["population_counts"].items():
        print(f"{name}: {value}")
    metric_rows = []
    count_rows = []
    for name in ["majority", "logistic"]:
        metrics = report["models"][name]
        metric_row = {"model": name}
        for key in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
            value = metrics[key]
            metric_row[key] = "undefined" if value is None else f"{value:.4f}"
        metric_rows.append(metric_row)
        count_rows.append({"model": name, **{key: metrics[key] for key in ["flagged_evaluated", "tp", "fp", "fn", "tn"]}})
    print("\nTEST METRICS: known outcomes among eligible predictions only")
    print(pd.DataFrame(metric_rows).to_string(index=False))
    print("\nTEST COUNTS: same known-outcome subset")
    print(pd.DataFrame(count_rows).to_string(index=False))
    print("all_eligible_reminders_within_150:", report["capacity_diagnostic"]["within_150"])
    print("150 was a validation teaching assumption. No list clipping or threshold adjustment was performed.")
    print("Unknown outcomes were retained in predictions and excluded only from outcome metrics.")
    print("No model was fitted and no threshold was tuned in this evaluation.")
    print("results_dir:", OUTPUT_DIR)
    print("This holdout is now used. Do not tune from it and still call the same assessment independent.")


def main():
    # A completed report can be displayed again without reopening test inputs.
    if OUTPUT_DIR.exists():
        report_path = OUTPUT_DIR / "metrics.json"
        if report_path.is_file():
            show_report(json.loads(report_path.read_bytes()), cached=True)
            return
        raise RuntimeError("An incomplete final-test attempt exists. Do not delete or overwrite it; investigate before any retry.")

    metadata = json.loads((FROZEN_DIR / "metadata.json").read_bytes())
    assets = {}
    for name in ["models.joblib", "frozen_plan.json", "development_train.csv", "development_valid.csv", "freeze_model.py"]:
        content = (FROZEN_DIR / name).read_bytes()
        if sha256(content) != metadata["sha256"][name]:
            raise ValueError(f"Frozen artifact fingerprint mismatch: {name}. Stop before test access.")
        assets[name] = content
    if sha256(assets["models.joblib"]) != EXPECTED_MODEL_SHA256:
        raise ValueError("Model fingerprint differs from the learner-confirmed frozen output.")
    versions = {"python": platform.python_version(), "scikit_learn": sklearn.__version__, "pandas": pd.__version__, "numpy": np.__version__, "joblib": joblib.__version__}
    for name, value in versions.items():
        if value != metadata["environment"][name]:
            raise ValueError(f"Version mismatch for {name}. Use the original frozen environment before testing.")
    plan = json.loads(assets["frozen_plan.json"])
    if plan["feature_columns"] != FEATURES or plan["threshold"] != 0.4 or plan["positive_class"] != 1:
        raise ValueError("Frozen feature or decision settings differ from the confirmed plan.")
    if plan["training_dates"] != ["2026-06-01", "2026-07-01"] or plan["validation_dates"] != ["2026-08-01"] or plan["test_prediction_date"] != "2026-09-01":
        raise ValueError("The frozen time allocation differs from the confirmed plan.")

    # Load only the locally created, fingerprint-matched bundle. Never fit here.
    bundle = joblib.load(io.BytesIO(assets["models.joblib"]))
    if bundle["feature_columns"] != FEATURES or bundle["threshold"] != 0.4 or bundle["positive_class"] != 1 or bundle["comparison_operator"] != ">=":
        raise ValueError("Frozen model bundle and confirmed decision rule disagree.")
    model = bundle["main_model"]
    baseline = bundle["baseline_model"]

    feature_bytes = (DATA_DIR / "test_features_raw.csv").read_bytes()
    raw = pd.read_csv(io.BytesIO(feature_bytes), encoding="utf-8-sig")
    required = KEYS + FEATURES + ["status_at_prediction", "feature_start_date", "feature_end_date", "label_start_date", "label_end_date"]
    if not set(required).issubset(raw.columns) or OUTCOME in raw.columns:
        raise ValueError("Unexpected test feature schema or an outcome column in feature data.")
    if len(raw) != 300 or raw[KEYS].isna().any().any() or raw.duplicated(KEYS).any():
        raise ValueError("Test snapshots must have 300 rows and unique nonmissing member/date keys.")
    expected_dates = {"prediction_date": "2026-09-01", "feature_start_date": "2026-08-25", "feature_end_date": "2026-08-31", "label_start_date": "2026-09-01", "label_end_date": "2026-09-07"}
    for column, expected in expected_dates.items():
        if not raw[column].eq(expected).all():
            raise ValueError(f"Unexpected test window in {column}.")
    if not raw["status_at_prediction"].isin(["valid", "disabled"]).all():
        raise ValueError("Unknown prediction-time membership status; do not silently exclude it.")
    eligible = raw[raw["status_at_prediction"] == "valid"].copy()
    if eligible.empty or eligible[FEATURES].isna().any().any():
        raise ValueError("Eligible test features are empty or missing. Stop rather than invent new preprocessing.")

    predictions = eligible.copy()
    predictions["inactive_probability"] = model.predict_proba(eligible[FEATURES])[:, list(model.classes_).index(1)]
    predictions["prediction"] = (predictions["inactive_probability"] >= 0.4).astype(int)
    predictions["baseline_probability"] = baseline.predict_proba(eligible[FEATURES])[:, list(baseline.classes_).index(1)]
    predictions["baseline_prediction"] = baseline.predict(eligible[FEATURES])
    prediction_bytes = csv_bytes(predictions)

    # This directory reserves the attempt before ANY holdout-label read.
    OUTPUT_DIR.mkdir(exist_ok=False)
    labels_access_attempted = False
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        write_new(OUTPUT_DIR / "attempt.json", json_bytes({"started_at_utc": started_at, "model_sha256": EXPECTED_MODEL_SHA256, "threshold": 0.4, "state": "reserved_before_holdout_label_access"}))
        write_new(OUTPUT_DIR / "test_predictions.csv", prediction_bytes)
        evaluator_bytes = Path(__file__).read_bytes()
        write_new(OUTPUT_DIR / "evaluator_source.py", evaluator_bytes)

        # The first label access occurs only after fixed predictions are saved.
        labels_access_attempted = True
        label_bytes = (DATA_DIR / "test_labels_holdout.csv").read_bytes()
        labels = pd.read_csv(io.BytesIO(label_bytes), encoding="utf-8-sig")
        if set(labels.columns) != set(KEYS + [OUTCOME]):
            raise ValueError("Unexpected held-out label schema.")
        if len(labels) != 300 or labels[KEYS].isna().any().any() or labels.duplicated(KEYS).any():
            raise ValueError("Held-out labels must have 300 unique, nonmissing member/date keys.")
        if not (labels[OUTCOME].isna() | labels[OUTCOME].isin(range(8))).all():
            raise ValueError("Observed future active days must be integer values between 0 and 7.")
        matched_keys = raw[KEYS].merge(labels[KEYS], on=KEYS, how="outer", validate="one_to_one", indicator=True)
        if not matched_keys["_merge"].eq("both").all():
            raise ValueError("Test feature and outcome keys do not match exactly; no silent row dropping is allowed.")
        joined = predictions.merge(labels, on=KEYS, how="left", validate="one_to_one")
        known = joined[OUTCOME].notna()
        joined["outcome_known"] = known
        joined["y_true"] = pd.Series(pd.NA, index=joined.index, dtype="Int64")
        joined.loc[known, "y_true"] = (joined.loc[known, OUTCOME] == 0).astype(int)
        observed = joined.loc[known].copy()
        y = observed["y_true"].astype(int)
        models = {
            "majority": score_predictions(y, observed["baseline_prediction"], observed["baseline_probability"]),
            "logistic": score_predictions(y, observed["prediction"], observed["inactive_probability"]),
        }
        joined_bytes = csv_bytes(joined)
        write_new(OUTPUT_DIR / "evaluation_rows.csv", joined_bytes)
        reminders = int(predictions["prediction"].sum())
        report = {
            "case_id": plan["case_id"],
            "started_at_utc": started_at,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_scope": "simulated_September_holdout_only",
            "model_sha256": EXPECTED_MODEL_SHA256,
            "feature_columns": FEATURES,
            "positive_class": 1,
            "threshold": 0.4,
            "comparison_operator": ">=",
            "model_fitted_in_this_run": False,
            "threshold_tuned_in_this_run": False,
            "versions": versions,
            "population_counts": {
                "raw_test_rows": len(raw),
                "excluded_disabled_rows": len(raw) - len(eligible),
                "eligible_predictions": len(predictions),
                "eligible_unknown_outcomes": int((~known).sum()),
                "known_outcomes_evaluated": len(observed),
                "actual_inactive_evaluated": int(y.sum()),
                "logistic_reminders_all_eligible": reminders,
            },
            "models": models,
            "capacity_diagnostic": {"validation_teaching_limit": 150, "test_reminders_all_eligible": reminders, "within_150": reminders <= 150, "enforced_as_a_test_cap": False},
            "sha256": {
                "test_features_raw.csv": sha256(feature_bytes),
                "test_labels_holdout.csv": sha256(label_bytes),
                "test_predictions.csv": sha256(prediction_bytes),
                "evaluation_rows.csv": sha256(joined_bytes),
                "evaluator_source.py": sha256(evaluator_bytes),
            },
            "test_hash_provenance": "Test input hashes were recorded at this first evaluation; no claim of comparison against a pre-freeze test-data hash is made.",
            "limitations": ["Synthetic data, not measured production impact.", "Unknown outcomes are excluded from outcome metrics, not from prediction eligibility.", "150 is a validation teaching assumption; no test-time truncation or threshold tuning.", "Subsequent test-feedback tuning would require a new independent evaluation set."],
        }
        # Written last: this file marks a completed evaluation for cached replay.
        write_new(OUTPUT_DIR / "metrics.json", json_bytes(report))
    except Exception as error:
        try:
            write_new(OUTPUT_DIR / "failure.json", json_bytes({"labels_access_attempted": labels_access_attempted, "error_type": type(error).__name__, "error": str(error), "action": "Preserve this attempt and investigate. Do not delete it to silently rerun."}))
        except OSError:
            pass
        raise
    show_report(report)


if __name__ == "__main__":
    main()
