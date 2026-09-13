"""
Advanced_Features.py
====================

Add-on module for FileGaurd — PE Malicious File Detection using Machine Learning.

Author : Mayur Nhavalde
Repo   : https://github.com/mayurOG/FILEGAURD-USING-MACHINE-LEARNING-ML-

This script demonstrates 3 advanced, high-accuracy ML features that build on top
of the existing Random Forest (Extra Trees feature selection) pipeline:

  1. STACKING ENSEMBLE
     Combines multiple strong learners (RandomForest, XGBoost, GradientBoosting)
     through a Logistic-Regression meta-learner, so the strengths of each model
     are fused -> higher, more stable accuracy than any single model.

  2. HYPERPARAMETER TUNING (RandomizedSearchCV)
     Automatically searches the best hyper-parameters for the champion model,
     improving both accuracy and robustness (cross-validated).

  3. OPTIMIZED DECISION THRESHOLD
     Instead of the default 0.5 probability cut-off, the threshold is tuned on a
     validation fold to balance False-Positive and False-Negative rates, making
     the detector safer in the real world.

Input data: final_pe_data.csv (the 13 features selected by Extra Trees + label)
"""

import os
import sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, roc_curve)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

RANDOM_STATE = 42


def load_data(path="final_pe_data.csv"):
    """Load the reduced PE dataset (13 features + target)."""
    df = pd.read_csv(path)
    X = df.drop(columns=["legitimate"])
    y = df["legitimate"].values
    return X, y


def evaluate(name, model, X_test, y_test):
    """Print a full set of metrics for a model."""
    proba = model.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    acc = accuracy_score(y_test, pred)
    prec = precision_score(y_test, pred)
    rec = recall_score(y_test, pred)
    f1 = f1_score(y_test, pred)
    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
    fpr = (fp / float(tp + fp)) * 100 if (tp + fp) else 0.0
    fnr = (fn / float(tn + fn)) * 100 if (tn + fn) else 0.0
    print(f"\n[{name}]")
    print(f"  Accuracy        : {acc:.5f}")
    print(f"  Precision       : {prec:.5f}")
    print(f"  Recall          : {rec:.5f}")
    print(f"  F1-Score        : {f1:.5f}")
    print(f"  False positive  : {fpr:.4f} %")
    print(f"  False negative  : {fnr:.4f} %")
    return acc, prec, rec, f1, fpr, fnr


# ---------------------------------------------------------------------------
# 1. STACKING ENSEMBLE
# ---------------------------------------------------------------------------
def stacking_ensemble(X, y, test_size=0.2):
    print("\n" + "=" * 60)
    print("ADVANCED FEATURE 1 : STACKING ENSEMBLE")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y)

    base_learners = [
        ("random_forest", RandomForestClassifier(n_estimators=300, n_jobs=-1,
                                                 random_state=RANDOM_STATE)),
        ("xgboost", XGBClassifier(n_estimators=300, learning_rate=0.1,
                                  use_label_encoder=False, eval_metric="logloss",
                                  random_state=RANDOM_STATE)),
        ("gradient_boosting", GradientBoostingClassifier(n_estimators=200,
                                                         random_state=RANDOM_STATE)),
    ]
    meta_model = LogisticRegression(max_iter=1000)

    stack = StackingClassifier(
        estimators=base_learners,
        final_estimator=meta_model,
        cv=StratifiedKFold(5),
        stack_method="predict_proba",
        n_jobs=-1,
    )
    stack.fit(X_train, y_train)
    evaluate("Stacking Ensemble (RF + XGB + GBoost -> LR)", stack, X_test, y_test)

    cv = cross_val_score(stack, X, y, cv=StratifiedKFold(5), n_jobs=-1)
    print(f"  5-fold Cross-Validation Accuracy : {cv.mean():.5f} (+/- {cv.std():.4f})")
    return stack


# ---------------------------------------------------------------------------
# 2. HYPERPARAMETER TUNING (RandomizedSearchCV)
# ---------------------------------------------------------------------------
def tuned_random_forest(X, y, test_size=0.2):
    print("\n" + "=" * 60)
    print("ADVANCED FEATURE 2 : HYPERPARAMETER OPTIMIZATION (RandomizedSearchCV)")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y)

    rf = RandomForestClassifier(random_state=RANDOM_STATE)
    param_grid = {
        "n_estimators": [200, 400, 600],
        "max_depth": [None, 15, 25, 35],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
        "criterion": ["gini", "entropy"],
    }
    search = RandomizedSearchCV(
        rf, param_distributions=param_grid,
        n_iter=30, cv=StratifiedKFold(5), scoring="accuracy",
        n_jobs=-1, random_state=RANDOM_STATE, verbose=0,
    )
    search.fit(X_train, y_train)

    print("  Best parameters :")
    for k, v in search.best_params_.items():
        print(f"      {k} = {v}")
    evaluate("Tuned Random Forest", search.best_estimator_, X_test, y_test)
    return search.best_estimator_


# ---------------------------------------------------------------------------
# 3. OPTIMIZED DECISION THRESHOLD
# ---------------------------------------------------------------------------
def optimized_threshold(model, X, y, test_size=0.2):
    print("\n" + "=" * 60)
    print("ADVANCED FEATURE 3 : OPTIMIZED DECISION THRESHOLD")
    print("=" * 60)

    # Split into train, validation (to tune threshold) and test (to verify)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=RANDOM_STATE, stratify=y_train)

    model.fit(X_train, y_train)
    val_proba = model.predict_proba(X_val)[:, 1]

    fpr, tpr, thresholds = roc_curve(y_val, val_proba)
    # Pick the threshold that maximises Youden's J = TPR - FPR,
    # i.e. the best balance of sensitivity and specificity.
    j = tpr - fpr
    idx = int(np.argmax(j))
    best_thresh = float(thresholds[idx])
    print(f"  Optimized threshold (Youden's J) : {best_thresh:.4f}")
    print(f"  Default threshold                : 0.5000")

    test_proba = model.predict_proba(X_test)[:, 1]
    default_pred = (test_proba >= 0.5).astype(int)
    opt_pred = (test_proba >= best_thresh).astype(int)

    print("\n  -- Model with DEFAULT threshold (0.50) --")
    evaluate("Default", _ThresholdModel(model, 0.5), X_test, y_test)
    print("\n  -- Model with OPTIMIZED threshold --")
    evaluate("Optimized", _ThresholdModel(model, best_thresh), X_test, y_test)
    return best_thresh


class _ThresholdModel:
    """Small wrapper so a tuned probability threshold can be evaluated cleanly."""
    def __init__(self, estimator, threshold):
        self.estimator = estimator
        self.threshold = threshold

    def predict(self, X):
        return (self.estimator.predict_proba(X)[:, 1] >= self.threshold).astype(int)

    def predict_proba(self, X):
        return self.estimator.predict_proba(X)


def _subsample(X, y, n):
    """Optionally subsample (for quick smoke tests only)."""
    if n is None or n >= len(X):
        return X, y
    rng = np.random.RandomState(RANDOM_STATE)
    legit_idx = np.where(y == 1)[0]
    mal_idx = np.where(y == 0)[0]
    keep = np.concatenate([rng.choice(legit_idx, size=max(1, n // 2), replace=False),
                           rng.choice(mal_idx, size=max(1, n // 2), replace=False)])
    keep = np.sort(keep)
    return X.iloc[keep], y[keep]


if __name__ == "__main__":
    print("\nFileGaurd — Advanced Machine-Learning Features")
    print("Author: Mayur Nhavalde\n")

    # `--samples N` limits the data only for a quick smoke test; remove it for full training.
    n = None
    if "--samples" in sys.argv:
        n = int(sys.argv[sys.argv.index("--samples") + 1])

    X, y = load_data()
    X, y = _subsample(X, y, n)
    print(f"Dataset shape : {X.shape}   (13 selectBest features + 1 target)")
    print(f"Class balance : legitimate={int((y == 1).sum())}, malicious={int((y == 0).sum())}")
    if n is not None:
        print("NOTE: running in quick smoke-test mode (--samples).")

    tuned_rf = tuned_random_forest(X, y)          # Feature 2 (also the champion base model)
    stacking_ensemble(X, y)                        # Feature 1
    optimized_threshold(tuned_rf, X, y)            # Feature 3 on the tuned model

    print("\nDone. All three advanced features executed successfully.\n")
