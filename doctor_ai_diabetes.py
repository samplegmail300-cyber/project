# =====================================================
# Doctor AI - Diabetes Prediction (learning project)
# Run this in Google Colab (colab.research.google.com)
# NOTE: For education only. Not real medical advice.
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             ConfusionMatrixDisplay)

# ---------- STEP 1: Load the data ----------
# PIMA Indians Diabetes dataset (768 patients)
URL = ("https://raw.githubusercontent.com/jbrownlee/Datasets/"
       "master/pima-indians-diabetes.data.csv")

columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
           "Insulin", "BMI", "DiabetesPedigree", "Age", "Outcome"]

df = pd.read_csv(URL, header=None, names=columns)
print("Dataset size (rows, columns):", df.shape)
print(df.head())
print("\nOutcome counts (0 = no diabetes, 1 = diabetes):")
print(df["Outcome"].value_counts())

# ---------- STEP 2: Clean the data ----------
# In this dataset, a 0 in these columns really means "missing"
cols_with_fake_zeros = ["Glucose", "BloodPressure", "SkinThickness",
                        "Insulin", "BMI"]
df[cols_with_fake_zeros] = df[cols_with_fake_zeros].replace(0, np.nan)
df = df.fillna(df.median())  # fill missing values with the median
print("\nMissing values left:", int(df.isna().sum().sum()))

# ---------- STEP 3: Split into train and test ----------
X = df.drop("Outcome", axis=1)   # patient information
y = df["Outcome"]                # the answer we want to predict

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print("\nTraining patients:", len(X_train), "| Testing patients:", len(X_test))

# ---------- STEP 4: Train two models ----------
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
rf_model.fit(X_train, y_train)

# ---------- STEP 5: Test the models ----------
log_acc = accuracy_score(y_test, log_model.predict(X_test))
rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
print(f"\nLogistic Regression accuracy: {log_acc:.2%}")
print(f"Random Forest accuracy:       {rf_acc:.2%}")

best_model = rf_model if rf_acc >= log_acc else log_model
best_name = "Random Forest" if rf_acc >= log_acc else "Logistic Regression"
print("\nBest model:", best_name)
print(classification_report(y_test, best_model.predict(X_test),
                            target_names=["No diabetes", "Diabetes"]))

# ---------- STEP 6: Charts for your report ----------
ConfusionMatrixDisplay.from_estimator(
    best_model, X_test, y_test,
    display_labels=["No diabetes", "Diabetes"], cmap="Blues")
plt.title(f"Confusion Matrix - {best_name}")
plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")
plt.show()

importances = pd.Series(rf_model.feature_importances_, index=X.columns)
importances.sort_values().plot(kind="barh", color="teal")
plt.title("Which patient data matters most? (Random Forest)")
plt.xlabel("Importance")
plt.savefig("feature_importance.png", dpi=150, bbox_inches="tight")
plt.show()

# ---------- STEP 7: Predict for a new patient ----------
new_patient = pd.DataFrame([{
    "Pregnancies": 2, "Glucose": 150, "BloodPressure": 85,
    "SkinThickness": 30, "Insulin": 120, "BMI": 33.6,
    "DiabetesPedigree": 0.6, "Age": 45}])

prediction = best_model.predict(new_patient)[0]
probability = best_model.predict_proba(new_patient)[0][1]

print("\n--- Doctor AI result ---")
print("Prediction:", "Possible diabetes" if prediction == 1 else "Low risk")
print(f"Risk probability: {probability:.1%}")
print("Disclaimer: This is a student project, not medical advice.")
