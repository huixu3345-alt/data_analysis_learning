"""Prepare reproducible SIMULATED member snapshots for the Week 13 case.

This is teacher-provided preparation scaffolding, not a trained model.
No real members, production outcomes, or model metrics are included.
Run this script yourself. Do not open test_labels_holdout.csv for tuning.
"""

import argparse
import csv
import hashlib
import io
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path


DEFAULT_SEED = 20260914
BATCHES = (
    (date(2026, 6, 1), "train"),
    (date(2026, 7, 1), "train"),
    (date(2026, 8, 1), "validation"),
    (date(2026, 9, 1), "test"),
)
MODEL_FEATURES = ["past_active_days_7d", "past_order_count_7d"]
FEATURE_COLUMNS = [
    "member_id",
    "prediction_date",
    "feature_start_date",
    "feature_end_date",
    "label_start_date",
    "label_end_date",
    "status_at_prediction",
    *MODEL_FEATURES,
]
LABEL_COLUMNS = ["member_id", "prediction_date", "future_active_days_7d"]
OUTPUT_NAMES = (
    "development_raw.csv",
    "test_features_raw.csv",
    "test_labels_holdout.csv",
    "manifest.json",
)


def write_csv(path, fields, rows):
    """Write a new CSV and hash its serialized bytes without rereading it."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    payload = buffer.getvalue().encode("utf-8-sig")
    with path.open("xb") as stream:
        stream.write(payload)
    return {"rows": len(rows), "sha256": hashlib.sha256(payload).hexdigest()}


def make_rows(seed, members_per_batch):
    rng = random.Random(seed)
    development = []
    test_features = []
    test_labels = []
    day_weights = (20, 18, 16, 14, 12, 9, 7, 4)

    for batch_number, (prediction_date, role) in enumerate(BATCHES):
        feature_start = prediction_date - timedelta(days=7)
        feature_end = prediction_date - timedelta(days=1)
        label_end = prediction_date + timedelta(days=6)

        for member_number in range(1, members_per_batch + 1):
            member_id = f"SYN_{member_number:04d}"
            status = "valid" if rng.random() < 0.9 else "disabled"
            past_days = rng.choices(range(8), weights=day_weights, k=1)[0]
            # Orders occur only on simulated active days. An order means
            # a completed payment during the historical feature window.
            orders = sum(
                rng.choices((0, 1, 2), weights=(70, 25, 5), k=past_days)
            )

            # An intentionally invented noisy relationship, not a business
            # estimate. Future outcomes never enter the feature columns.
            logit = 1.2 - 0.5 * past_days - 0.18 * orders + 0.03 * batch_number
            logit += rng.gauss(0.0, 0.45)
            inactivity_probability = 1.0 / (1.0 + math.exp(-logit))
            future_days = (
                0 if rng.random() < inactivity_probability else rng.randint(1, 7)
            )
            if status == "disabled":
                future_days = 0
            # Empty outcomes represent unknown labels, NEVER zero activity.
            if rng.random() < 0.03:
                future_days = None

            row = {
                "member_id": member_id,
                "prediction_date": prediction_date.isoformat(),
                "feature_start_date": feature_start.isoformat(),
                "feature_end_date": feature_end.isoformat(),
                "label_start_date": prediction_date.isoformat(),
                "label_end_date": label_end.isoformat(),
                "status_at_prediction": status,
                "past_active_days_7d": past_days,
                "past_order_count_7d": orders,
            }
            if role == "test":
                test_features.append(row)
                test_labels.append(
                    {
                        "member_id": member_id,
                        "prediction_date": prediction_date.isoformat(),
                        "future_active_days_7d": future_days,
                    }
                )
            else:
                development.append({**row, "future_active_days_7d": future_days})

    return development, test_features, test_labels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--members-per-batch", type=int, default=300)
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent / "data"
    )
    args = parser.parse_args()
    if args.members_per_batch < 1:
        parser.error("--members-per-batch must be positive")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if any((output_dir / name).exists() for name in OUTPUT_NAMES):
        parser.error(
            "Output files already exist; nothing was overwritten. "
            "Use a different --output-dir for a reproducibility run."
        )

    development, test_features, test_labels = make_rows(
        args.seed, args.members_per_batch
    )
    files = {}
    files["development_raw.csv"] = write_csv(
        output_dir / "development_raw.csv",
        FEATURE_COLUMNS + ["future_active_days_7d"],
        development,
    )
    files["test_features_raw.csv"] = write_csv(
        output_dir / "test_features_raw.csv", FEATURE_COLUMNS, test_features
    )
    files["test_labels_holdout.csv"] = write_csv(
        output_dir / "test_labels_holdout.csv", LABEL_COLUMNS, test_labels
    )
    manifest = {
        "generator_version": "1.0",
        "source": "SIMULATED classroom data; not real business evidence",
        "seed": args.seed,
        "members_per_batch": args.members_per_batch,
        "row_grain": "one member at one prediction date",
        "key_columns": ["member_id", "prediction_date"],
        "member_scope": "existing members observed across monthly snapshots",
        "feature_columns_for_model": MODEL_FEATURES,
        "status_mapping": {"valid": "eligible", "disabled": "exclude"},
        "activity_definition": "a day with at least one member activity event",
        "order_definition": "payment completed inside the past seven full days",
        "unknown_outcome": "empty CSV field; exclude from supervised fitting/scoring",
        "target_rule": "future_active_days_7d == 0 -> 1; >= 1 -> 0; missing -> unknown",
        "label_observation_as_of": "2026-09-08",
        "split_by_prediction_date": {day.isoformat(): role for day, role in BATCHES},
        "test_policy": "Do not use test labels for feature/model/threshold selection",
        "files": files,
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    with (output_dir / "manifest.json").open("xb") as stream:
        stream.write(manifest_bytes)

    print("SIMULATED DATA ONLY - NOT BUSINESS EVIDENCE")
    print(f"seed: {args.seed}")
    print(f"output_dir: {output_dir}")
    for prediction_date, role in BATCHES:
        start = prediction_date - timedelta(days=7)
        end = prediction_date - timedelta(days=1)
        print(f"{prediction_date} | {role} | feature window: {start} to {end}")
    for filename, info in files.items():
        print(f"{filename}: {info['rows']} raw rows")
    print("manifest.json records definitions, the split plan, and CSV hashes.")
    print("Raw rows still include disabled members and unknown outcomes.")
    print("Test labels are held out. No training or evaluation was performed.")


if __name__ == "__main__":
    main()
