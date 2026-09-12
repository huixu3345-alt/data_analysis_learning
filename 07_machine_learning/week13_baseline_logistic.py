"""Week 13: simulated data for learning classification, not business evaluation.

Training snapshots: 2026-05-31; outcomes: 2026-06-01 to 2026-06-07.
Validation snapshots: 2026-06-30; outcomes: 2026-07-01 to 2026-07-07.
All outcomes below are simulated and fully observed.
"""

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression


# Each row is one member. The feature is active days in the PAST seven days.
X_train = [[4], [2], [0], [5], [1], [0], [3], [0]]

# Labels describe the NEXT seven days:
# 0 = active at least once; 1 = no activity.
y_train = [0, 0, 1, 0, 0, 1, 0, 0]

X_valid = [[0], [3], [7]]
y_valid = [1, 0, 0]

# Baseline: predict the most frequent TRAINING label for every member.
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_pred = baseline.predict(X_valid)

# Logistic regression: learn from training features and labels.
model = LogisticRegression()
model.fit(X_train, y_train)
probabilities = model.predict_proba(X_valid)
predictions = model.predict(X_valid)

print("X_valid:", X_valid)
print("y_valid:", y_valid)
print("baseline_predictions:", baseline_pred)
print("classes:", model.classes_)
print("probabilities:\n", probabilities)
print("predictions:", predictions)

inactive_prob = probabilities[:, 1]
predictions_03 = (inactive_prob >= 0.3).astype(int)
print("predictions_03:", predictions_03)

from sklearn.tree import DecisionTreeClassifier, export_text

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

print("tree_rules:")
print(export_text(tree, feature_names=["past_active_days_7d"]))
print("tree_predictions:", tree.predict(X_valid))

from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score
)

print("\n--- validation metrics ---")
print("cm_default:\n", confusion_matrix(y_valid, predictions, labels=[0, 1]))
print("cm_03:\n", confusion_matrix(y_valid, predictions_03, labels=[0, 1]))
print("recall_default:", recall_score(y_valid, predictions, pos_label=1))
print("precision_03:", precision_score(y_valid, predictions_03, pos_label=1))
print("recall_03:", recall_score(y_valid, predictions_03, pos_label=1))
print("f1_03:", f1_score(y_valid, predictions_03, pos_label=1))
print("roc_auc:", roc_auc_score(y_valid, inactive_prob))