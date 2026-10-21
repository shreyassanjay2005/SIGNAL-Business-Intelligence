
from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score
)

# -----------------------------------------
# FILE PATHS
# -----------------------------------------

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "superstore.csv"

NUMERIC_FEATURES = [
    "Sales",
    "Quantity",
    "Discount"
]

CATEGORY_FEATURES = [
    "Region",
    "Segment",
    "Category",
    "Sub-Category"
]

FEATURES = NUMERIC_FEATURES + CATEGORY_FEATURES

# -----------------------------------------
# LOAD DATA
# -----------------------------------------

def main():

    if not DATA_PATH.exists():
        raise SystemExit(
            "superstore.csv was not found."
        )

    df = pd.read_csv(DATA_PATH)

    print("\n========== DATA QUALITY CHECK ==========")
    print(f"Original records: {len(df):,}")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d/%m/%y",
        errors="coerce"
    )

    for col in NUMERIC_FEATURES + ["Profit"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    print(
        "Successfully parsed dates:",
        df["Order Date"].notna().sum()
    )

    # Remove unusable records
    required = (
        ["Order Date", "Profit"] + FEATURES
    )

    df = df.dropna(
        subset=required
    ).copy()

    print(
        f"Usable records: {len(df):,}"
    )

    # -------------------------------------
    # TARGET VARIABLE
    # -------------------------------------

    df["Loss Risk"] = (
        df["Profit"] < 0
    ).astype(int)

    # -------------------------------------
    # TIME-BASED TRAIN TEST SPLIT
    # -------------------------------------

    train = df[
        df["Order Date"] < "2017-01-01"
    ].copy()

    test = df[
        df["Order Date"] >= "2017-01-01"
    ].copy()

    if train.empty or test.empty:
        raise ValueError(
            "Training or testing dataset is empty."
        )

    X_train = train[FEATURES]
    y_train = train["Loss Risk"]

    X_test = test[FEATURES]
    y_test = test["Loss Risk"]

    # -------------------------------------
    # DATA PREPROCESSING
    # -------------------------------------

    preprocessor = ColumnTransformer([
        (
            "numeric",
            StandardScaler(),
            NUMERIC_FEATURES
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            CATEGORY_FEATURES
        )
    ])

    # -------------------------------------
    # MACHINE LEARNING MODEL
    # -------------------------------------

    model = Pipeline([
        (
            "preprocessing",
            preprocessor
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000
            )
        )
    ])

    model.fit(
        X_train,
        y_train
    )

    # -------------------------------------
    # MODEL PREDICTIONS
    # -------------------------------------

    predictions = model.predict(
        X_test
    )

    probabilities = (
        model.predict_proba(X_test)[:, 1]
    )

    actual = y_test.to_numpy()

    # -------------------------------------
    # MODEL PERFORMANCE
    # -------------------------------------

    accuracy = accuracy_score(
        actual,
        predictions
    )

    baseline = max(
        actual.mean(),
        1 - actual.mean()
    )

    balanced_accuracy = balanced_accuracy_score(
        actual,
        predictions
    )

    precision = precision_score(
        actual,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        actual,
        predictions,
        zero_division=0
    )

    auc = roc_auc_score(
        actual,
        probabilities
    )

    brier = brier_score_loss(
        actual,
        probabilities
    )

    tn, fp, fn, tp = confusion_matrix(
        actual,
        predictions,
        labels=[0, 1]
    ).ravel()

    print("\n========== SIGNAL AI ENGINE ==========")

    print(
        f"Training records: {len(train):,}"
    )

    print(
        f"Testing records: {len(test):,}"
    )

    print("\n========== MODEL PERFORMANCE ==========")

    print(f"Accuracy: {accuracy:.2%}")
    print(f"Baseline Accuracy: {baseline:.2%}")
    print(f"Balanced Accuracy: {balanced_accuracy:.2%}")
    print(f"ROC-AUC: {auc:.3f}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"Brier Score: {brier:.4f}")

    print("\n========== CONFUSION MATRIX ==========")

    print(f"True Positives: {tp}")
    print(f"True Negatives: {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")

    # -------------------------------------
    # SAVE TRAINED MODEL
    # -------------------------------------

    model_path = ROOT / "signal_model.joblib"

    joblib.dump(
        model,
        model_path,
        compress=3
    )

    # -------------------------------------
    # SAVE VALIDATION RESULTS
    # -------------------------------------

    validation = pd.DataFrame({
        "Actual Loss": actual,
        "Predicted Loss": predictions,
        "Loss Probability": probabilities
    })

    validation.to_csv(
        ROOT / "signal_validation.csv",
        index=False
    )

    # -------------------------------------
    # SAVE MODEL METRICS
    # -------------------------------------

    metrics = {
        "model": "Logistic Regression",
        "total_rows": int(len(df)),
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "accuracy": float(accuracy),
        "baseline_accuracy": float(baseline),
        "balanced_accuracy": float(balanced_accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "roc_auc": float(auc),
        "brier_score": float(brier),
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn)
    }

    with open(
        ROOT / "signal_metrics.json",
        "w"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )

    print("\n========== FILES SAVED ==========")

    print("signal_model.joblib")
    print("signal_validation.csv")
    print("signal_metrics.json")

    print("\nMODEL TRAINING COMPLETE")


if __name__ == "__main__":
    main()
