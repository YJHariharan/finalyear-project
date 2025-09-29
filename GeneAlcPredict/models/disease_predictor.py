import math
from typing import Dict


class DiseasePredictor:
    """
    Deterministic predictor using a logistic transform over engineered features.
    This avoids external training while providing sensible risk variation.
    """

    def __init__(self):
        # Weights for each condition; tuned for variation and plausibility
        self.heart_weights = {
            "intercept": -5.0,
            "age": 0.03,
            "alcohol_percentage": 0.02,
            "bmi": 0.02,
            "systolic_bp": 0.015,
            "cholesterol": 0.01,
            "smoker": 0.8,
            "sex_male": 0.3,
            "exercise_level": -0.25,  # higher exercise encodes larger value
        }

        self.stroke_weights = {
            "intercept": -6.0,
            "age": 0.04,
            "alcohol_percentage": 0.015,
            "bmi": 0.015,
            "systolic_bp": 0.02,
            "cholesterol": 0.008,
            "smoker": 0.6,
            "sex_male": 0.1,
            "exercise_level": -0.2,
        }

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    def _linear_score(self, features: Dict[str, float], weights: Dict[str, float]) -> float:
        s = weights.get("intercept", 0.0)
        for k, w in weights.items():
            if k == "intercept":
                continue
            s += w * float(features.get(k, 0.0))
        return s

    def predict_diseases(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        features: processed dict including encoded categorical values.
        Returns percent risks and raw scores.
        """
        heart_score = self._linear_score(features, self.heart_weights)
        heart_prob = self._sigmoid(heart_score)
        heart_percent = float(heart_prob * 100.0)

        # Light calibration to avoid extremes for typical ranges
        heart_calibrated = max(0.0, min(100.0, 0.9 * heart_percent + 2.0))

        stroke_score = self._linear_score(features, self.stroke_weights)
        stroke_prob = self._sigmoid(stroke_score)
        stroke_percent = float(stroke_prob * 100.0)

        # Alcohol impact score: scaled by alcohol %, modulated by risk context
        alcohol_pct = float(features.get("alcohol_percentage", 0.0))
        alcohol_impact = 0.4 * alcohol_pct + 0.1 * (heart_percent + stroke_percent) / 2.0

        return {
            "heart_disease_risk": round(heart_calibrated, 2),
            "heart_raw_risk": round(heart_prob, 4),
            "stroke_risk": round(stroke_percent, 2),
            "alcohol_impact_score": round(alcohol_impact, 2),
        }

    def get_confidence_scores(self, features: Dict[str, float]) -> Dict[str, float]:
        """Simple confidence based on feature completeness and signal strength."""
        completeness = 0
        total = 9
        for k in [
            "age",
            "alcohol_percentage",
            "bmi",
            "systolic_bp",
            "cholesterol",
            "glucose",
            "smoker",
            "sex_male",
            "exercise_level",
        ]:
            if k in features:
                completeness += 1
        completeness_conf = completeness / total

        # Signal confidence increases when values are within clinical typical ranges
        age = float(features.get("age", 40))
        alcohol = float(features.get("alcohol_percentage", 10))
        systolic = float(features.get("systolic_bp", 120))
        typical = (
            (18 <= age <= 85)
            and (0 <= alcohol <= 40)
            and (90 <= systolic <= 160)
        )
        signal_conf = 0.7 if typical else 0.5

        overall = 0.6 * completeness_conf + 0.4 * signal_conf
        return {
            "heart_confidence": round(overall, 3),
            "stroke_confidence": round(overall * 0.95, 3),
        }

    def analyze_alcohol_thresholds(self, age: int = 40) -> Dict[int, float]:
        """Return heart risk percent for alcohol % across range at a given age."""
        out = {}
        for apct in range(0, 101, 5):
            features = {
                "age": age,
                "alcohol_percentage": apct,
                "bmi": 25,
                "systolic_bp": 120,
                "cholesterol": 200,
                "glucose": 95,
                "smoker": 0,
                "sex_male": 1,
                "exercise_level": 2,
            }
            preds = self.predict_diseases(features)
            out[apct] = preds["heart_disease_risk"]
        return out