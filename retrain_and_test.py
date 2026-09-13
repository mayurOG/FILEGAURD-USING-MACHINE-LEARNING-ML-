"""
The shipped classifier/classifier.pkl was pickled with scikit-learn 0.24.2.
Loading it under the currently installed scikit-learn (1.8.0) fails with:
    ValueError: node array from the pickle has an incompatible dtype
(sklearn changed the internal binary layout of DecisionTree nodes since then).

This script retrains an equivalent Random Forest on final_pe_data.csv --
the same 13 Extra-Trees-selected features the README describes -- using the
currently installed library versions, so the model can actually be loaded
and used. It then runs it on test_sample/ exactly like Final_Testing.py does.
"""
import os
import sys
import pickle
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from Final_Testing import extract_infos

RANDOM_STATE = 42

df = pd.read_csv("final_pe_data.csv")
feature_names = [c for c in df.columns if c != "legitimate"]
X = df[feature_names]
y = df["legitimate"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=RANDOM_STATE)
clf.fit(X_train, y_train)
acc = accuracy_score(y_test, clf.predict(X_test))
print(f"Retrained RandomForestClassifier held-out accuracy: {acc:.4f}")
print(f"Trained on {len(X_train)} rows, tested on {len(X_test)} rows, {len(feature_names)} features.\n")

os.makedirs("classifier_retrained", exist_ok=True)
joblib.dump(clf, "classifier_retrained/classifier.pkl")
with open("classifier_retrained/features.pkl", "wb") as f:
    pickle.dump(feature_names, f)

# ---- Run it on a real file, same logic as Final_Testing.py's __main__ block ----
target = sys.argv[1] if len(sys.argv) > 1 else "test_sample/sublime_text_build_4169_x64_setup.exe"
data = extract_infos(target)
pe_features = [data[x] for x in feature_names]
pe_row = pd.DataFrame([pe_features], columns=feature_names)
res = clf.predict(pe_row)[0]
proba = dict(zip(clf.classes_, clf.predict_proba(pe_row)[0]))

# NOTE: the "legitimate" column in final_pe_data.csv is 1=legitimate, 0=malicious,
# and clf.predict() returns that same raw value -- unlike Final_Testing.py's
# ['legitimate','malicious'][res] indexing, which matched the OLD classifier.pkl's
# own (unverified) internal label order, not this dataset's.
print(f"File tested        : {os.path.basename(target)}")
print(f"Prediction          : {'legitimate' if res == 1 else 'malicious'}")
print(f"Model confidence    : legitimate={proba.get(1, 0):.4f}  malicious={proba.get(0, 0):.4f}")
