from typing import Dict, Tuple


class DataProcessor:
    """Minimal processor to ensure expected numeric features and encodings."""

    def __init__(self):
        self.exercise_map = {"low": 0, "medium": 1, "high": 2}
        self.smoker_map = {"no": 0, "yes": 1}
        self.sex_map = {"female": 0, "male": 1}

    def process_single_patient(self, input_data: Dict) -> Dict[str, float]:
        # Clip numeric ranges to sensible bounds
        def clip(v, lo, hi):
            try:
                x = float(v)
            except Exception:
                x = lo
            return float(max(lo, min(hi, x)))

        age = clip(input_data.get("age", 40), 18, 100)
        apct = clip(input_data.get("alcohol_percentage", 0), 0, 100)
        bmi = clip(input_data.get("bmi", 25), 10, 60)
        sbp = clip(input_data.get("systolic_bp", 120), 80, 220)
        chol = clip(input_data.get("cholesterol", 200), 100, 400)
        glucose = clip(input_data.get("glucose", 95), 60, 300)

        smoker = self.smoker_map.get(str(input_data.get("smoker", "no")).lower(), 0)
        sex = self.sex_map.get(str(input_data.get("sex", "male")).lower(), 1)
        exercise = self.exercise_map.get(str(input_data.get("exercise_level", "medium")).lower(), 1)

        features = {
            "age": age,
            "alcohol_percentage": apct,
            "bmi": bmi,
            "systolic_bp": sbp,
            "cholesterol": chol,
            "glucose": glucose,
            "smoker": smoker,
            "sex_male": sex,
            "exercise_level": exercise,
        }
        return features