from typing import Dict, List, Tuple


def validate_input_data(input_data: Dict) -> Tuple[bool, str]:
    # Required
    if "age" not in input_data:
        return False, "Missing age"
    if "alcohol_percentage" not in input_data:
        return False, "Missing alcohol_percentage"

    age = input_data.get("age")
    apct = input_data.get("alcohol_percentage")
    try:
        age = float(age)
        apct = float(apct)
    except Exception:
        return False, "Age and alcohol_percentage must be numeric"

    if not (18 <= age <= 100):
        return False, "Age must be between 18 and 100"
    if not (0 <= apct <= 100):
        return False, "Alcohol percentage must be between 0 and 100"

    return True, "Valid"


def generate_recommendations(predictions: Dict[str, float], input_data: Dict) -> List[str]:
    recs: List[str] = []
    heart = predictions.get("heart_disease_risk", 0)
    stroke = predictions.get("stroke_risk", 0)
    alcohol = predictions.get("alcohol_impact_score", 0)

    if heart >= 20:
        recs.append("Consider a cardiology check-up and lipid panel.")
    if stroke >= 15:
        recs.append("Discuss blood pressure management strategies with a clinician.")
    if input_data.get("smoker", "no") == "yes":
        recs.append("Enroll in a smoking cessation program.")
    if input_data.get("exercise_level", "medium") in ["low"]:
        recs.append("Increase activity to at least 150 minutes of moderate exercise weekly.")
    if input_data.get("alcohol_percentage", 0) > 20:
        recs.append("Reduce alcohol intake; target under 14% weekly average.")

    if not recs:
        recs.append("Maintain current healthy habits and routine screenings.")
    return recs