# ==============================
# CREDIT CARD FRAUD DETECTION
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, classification_report
)
from imblearn.over_sampling import SMOTE

# ===== Load Dataset =====
# Dataset: https://www.kaggle.com/mlg-ulb/creditcardfraud
file_path = input("Enter CSV file path (creditcard.csv): ").strip()
df = pd.read_csv(file_path)

print("Dataset Shape:", df.shape)
print(df.head())

# ===== Data Preprocessing =====
X = df.drop("Class", axis=1)  # Features
y = df["Class"]              # Target: 0 = Legit, 1 = Fraud

# Standardize features (Time, Amount, etc.)
scaler = StandardScaler()
X[["Time", "Amount"]] = scaler.fit_transform(X[["Time", "Amount"]])

# Handle Imbalance with SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
print("Resampled dataset shape:", X_resampled.shape, y_resampled.shape)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# ===== Logistic Regression =====
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_train)
y_pred_lr = log_reg.predict(X_test)

# ===== Random Forest =====
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# ===== Evaluation Function =====
def evaluate_model(name, y_true, y_pred):
    print(f"\n📌 Model: {name}")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred))
    print("Recall:", recall_score(y_true, y_pred))
    print("F1 Score:", f1_score(y_true, y_pred))
    print("ROC-AUC:", roc_auc_score(y_true, y_pred))
    print("\nClassification Report:\n", classification_report(y_true, y_pred))
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix - {name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

# ===== Evaluate Both Models =====
evaluate_model("Logistic Regression", y_test, y_pred_lr)
evaluate_model("Random Forest", y_test, y_pred_rf)
