#!/usr/bin/env python3
"""
Wiry Pulse Predictor — Cawcaw Data Analyst
============================================
Predicts wiry pulse diagnosis from clinical and pulse-sensor data.

Usage:
  python predict_wiry.py --age 65 --gender 0 --h3LBD 0.5 --h2LBL 38 --RET_L 0.13
  python predict_wiry.py --batch new_patients.csv

Required fields: age, gender
Optional fields: h3LBD, h2LBL, RET L, choppy_pulse, red dots, BH, h3h2_ratio_mean
  (if any sensor field is missing, the model falls back to clinical-only data)
"""

import pickle
import numpy as np
import json
import sys
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'wiry_pulse_model.pkl')

# --- Clinical-only model coefficients (trained on age, gender, BH, SYS, DIA) ---
# These are baked in so we can predict even without sensors
CLINICAL_FEATURES = ['age', 'gender', 'BH', 'SYS', 'DIA']
CLINICAL_COEFS = {
    'age': 0.086, 'gender': -0.968, 'BH': -0.059, 'SYS': -0.002, 'DIA': 0.022
}
CLINICAL_INTERCEPT = 0.412
CLINICAL_MEANS = {'age': 38.15, 'gender': 0.28, 'BH': 162.38, 'SYS': 119.05, 'DIA': 77.06}
CLINICAL_STDS = {'age': 12.83, 'gender': 0.45, 'BH': 7.53, 'SYS': 16.48, 'DIA': 8.12}


def load_model():
    """Load the trained model from disk."""
    if not os.path.exists(MODEL_PATH):
        print(f"Warning: Model file not found at {MODEL_PATH}")
        print("Falling back to clinical-only model (less accurate).")
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def predict_clinical(age, gender, BH=None, SYS=None, DIA=None):
    """
    Clinical-only prediction using age, gender, and optionally height/BP.
    Uses the baked-in logistic regression coefficients.
    """
    vals = [age, gender]
    feats = ['age', 'gender']
    for f, v in [('BH', BH), ('SYS', SYS), ('DIA', DIA)]:
        if v is not None:
            vals.append(v)
            feats.append(f)
    
    z = CLINICAL_INTERCEPT
    for f, v in zip(feats, vals):
        z += CLINICAL_COEFS.get(f, 0) * (v - CLINICAL_MEANS.get(f, 0)) / CLINICAL_STDS.get(f, 1)
    
    return sigmoid(z)


def predict_patient(age, gender, h3LBD=None, h2LBL=None, RET_L=None,
                    choppy_pulse=None, red_dots=None, BH=None, h3h2_ratio_mean=None,
                    SYS=None, DIA=None):
    """
    Predict wiry pulse probability for a single patient.
    Uses the full sensor model if all sensor data is available,
    falls back to clinical-only prediction otherwise.
    
    Parameters
    ----------
    age : float
        Patient age in years
    gender : int
        0 = female, 1 = male
    h3LBD, h2LBL, RET_L : float, optional
        Pulse sensor and retinal measurements
    choppy_pulse : int, optional
        0 or 1
    red_dots : float, optional
        Tongue red dots score (0-100)
    BH : float, optional
        Body height in cm
    h3h2_ratio_mean : float, optional
        Mean h3/h2 ratio across all pulse positions
    SYS, DIA : float, optional
        Systolic/diastolic blood pressure
    
    Returns
    -------
    dict with probability, prediction, and confidence
    """
    model = load_model()
    
    # Check if we have enough data for the full model
    sensor_fields = [h3LBD, h2LBL, RET_L, choppy_pulse, red_dots, BH, h3h2_ratio_mean]
    has_full_data = all(v is not None for v in sensor_fields)
    
    if has_full_data and model is not None:
        # Full sensor model
        features = model['features']
        scaler = model['scaler']
        classifier = model['classifier']
        
        # Build feature vector in the right order
        # features: ['age', 'gender', 'h3LBD', 'h2LBL', 'RET L', 'choppy_pulse', 'red dots', 'BH', 'h3h2_ratio_mean']
        raw = [
            age, gender, h3LBD, h2LBL, RET_L, choppy_pulse, red_dots, BH, h3h2_ratio_mean
        ]
        X = np.array(raw).reshape(1, -1)
        X_scaled = scaler.transform(X)
        
        prob = classifier.predict_proba(X_scaled)[0, 1]
        pred = classifier.predict(X_scaled)[0]
        model_type = "full sensor"
    else:
        # Fall back to clinical model
        prob = predict_clinical(age, gender, BH, SYS, DIA)
        pred = 1 if prob >= 0.5 else 0
        model_type = "clinical-only"
    
    # Confidence level
    if prob > 0.8 or prob < 0.2:
        confidence = "high"
    elif prob > 0.65 or prob < 0.35:
        confidence = "moderate"
    else:
        confidence = "borderline"
    
    # Key risk factors for wiry pulse
    risk_factors = []
    if age > 50:
        risk_factors.append(f"age ({age}, >50)")
    if gender == 0:
        risk_factors.append("female gender")
    if h3LBD is not None and h3LBD < 1.0:
        risk_factors.append(f"low h3LBD ({h3LBD:.2f}, <1.0)")
    if h3h2_ratio_mean is not None and h3h2_ratio_mean < 0.05:
        risk_factors.append(f"low h3/h2 ratio ({h3h2_ratio_mean:.3f}, <0.05)")
    if RET_L is not None and RET_L > 0.13:
        risk_factors.append(f"elevated RET L ({RET_L:.3f}, >0.13)")
    if choppy_pulse == 1:
        risk_factors.append("co-occurring choppy pulse")
    
    return {
        'probability': round(prob, 4),
        'prediction': 'wiry' if pred == 1 else 'non-wiry',
        'confidence': confidence,
        'model_used': model_type,
        'risk_factors': risk_factors,
        'interpretation': _interpret(prob, pred)
    }


def _interpret(prob, pred):
    if prob >= 0.8:
        return "High probability of wiry pulse. Consistent with age-related vascular changes."
    elif prob >= 0.5:
        return "Moderate probability of wiry pulse. Consider alongside other clinical findings."
    elif prob >= 0.2:
        return "Low probability of wiry pulse. Patient likely falls in the younger, non-wiry profile."
    else:
        return "Very low probability of wiry pulse. Normal pulse characteristics expected."


def predict_batch(csv_path):
    """Predict for a batch of patients from a CSV file."""
    import pandas as pd
    batch = pd.read_csv(csv_path)
    results = []
    for _, row in batch.iterrows():
        res = predict_patient(
            age=row.get('age'),
            gender=row.get('gender'),
            h3LBD=row.get('h3LBD'),
            h2LBL=row.get('h2LBL'),
            RET_L=row.get('RET L'),
            choppy_pulse=row.get('choppy_pulse'),
            red_dots=row.get('red dots'),
            BH=row.get('BH'),
            h3h2_ratio_mean=row.get('h3h2_ratio_mean'),
            SYS=row.get('SYS'),
            DIA=row.get('DIA')
        )
        results.append(res)
    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Predict wiry pulse diagnosis')
    parser.add_argument('--age', type=float, help='Age in years')
    parser.add_argument('--gender', type=int, choices=[0, 1], help='Gender (0=female, 1=male)')
    parser.add_argument('--h3LBD', type=float, help='Pulse sensor h3 at left cun (distal)')
    parser.add_argument('--h2LBL', type=float, help='Pulse sensor h2 at left chi (proximal)')
    parser.add_argument('--RET_L', type=float, help='Retinal measurement (left)')
    parser.add_argument('--choppy_pulse', type=int, choices=[0, 1], help='Choppy pulse present?')
    parser.add_argument('--red_dots', type=float, help='Tongue red dots score (0-100)')
    parser.add_argument('--BH', type=float, help='Body height (cm)')
    parser.add_argument('--h3h2_ratio_mean', type=float, help='Mean h3/h2 ratio')
    parser.add_argument('--SYS', type=float, help='Systolic BP')
    parser.add_argument('--DIA', type=float, help='Diastolic BP')
    parser.add_argument('--batch', type=str, help='CSV file with patient data')
    
    args = parser.parse_args()
    
    if args.batch:
        print(f"Processing batch: {args.batch}")
        results = predict_batch(args.batch)
        for i, r in enumerate(results):
            print(f"\nPatient {i+1}:")
            print(f"  Prediction: {r['prediction']} (p={r['probability']:.3f})")
            print(f"  Confidence: {r['confidence']}")
        sys.exit(0)
    
    if args.age is None or args.gender is None:
        print("Error: --age and --gender are required for single-patient prediction")
        parser.print_help()
        sys.exit(1)
    
    result = predict_patient(
        age=args.age, gender=args.gender,
        h3LBD=args.h3LBD, h2LBL=args.h2LBL, RET_L=args.RET_L,
        choppy_pulse=args.choppy_pulse, red_dots=args.red_dots,
        BH=args.BH, h3h2_ratio_mean=args.h3h2_ratio_mean,
        SYS=args.SYS, DIA=args.DIA
    )
    
    print(f"\n=== WIRY PULSE PREDICTION ===")
    print(f"Model used:         {result['model_used']}")
    print(f"Probability:        {result['probability']:.1%}")
    print(f"Prediction:         {result['prediction']}")
    print(f"Confidence:         {result['confidence']}")
    if result['risk_factors']:
        print(f"Risk factors:       {', '.join(result['risk_factors'])}")
    print(f"Interpretation:     {result['interpretation']}")