"""
Helper functions for the application.
"""

def validate_input_data(data):
    """
    Validate input data for disease prediction.
    
    Args:
        data (dict): Input data dictionary
        
    Returns:
        tuple: (is_valid, message)
    """
    # Required fields
    if "age" not in data:
        return False, "Age is required"
    if "alcohol_percentage" not in data:
        return False, "Alcohol percentage is required"
    
    # Validate age
    age = data.get("age")
    if not isinstance(age, (int, float)) or age < 18 or age > 100:
        return False, "Age must be between 18 and 100"
    
    # Validate alcohol percentage
    alc = data.get("alcohol_percentage")
    if not isinstance(alc, (int, float)) or alc < 0 or alc > 100:
        return False, "Alcohol percentage must be between 0 and 100"
    
    # Optional numeric fields
    numeric_fields = {
        "bmi": (10, 60),
        "systolic_bp": (80, 200),
        "cholesterol": (100, 400),
        "glucose": (60, 300),
    }
    
    for field, (min_val, max_val) in numeric_fields.items():
        if field in data:
            val = data.get(field)
            if not isinstance(val, (int, float)) or val < min_val or val > max_val:
                return False, f"{field} must be between {min_val} and {max_val}"
    
    # Optional categorical fields
    categorical_fields = {
        "smoker": ["yes", "no"],
        "sex": ["male", "female"],
        "exercise_level": ["low", "medium", "high"],
    }
    
    for field, valid_values in categorical_fields.items():
        if field in data:
            val = data.get(field)
            if val not in valid_values:
                return False, f"{field} must be one of {valid_values}"
    
    return True, "Valid input data"


def generate_recommendations(predictions, input_data):
    """
    Generate health recommendations based on predictions and input data.
    
    Args:
        predictions (dict): Prediction results
        input_data (dict): Input data
        
    Returns:
        list: List of recommendation strings
    """
    recommendations = []
    
    # Get key values
    heart_risk = predictions.get("heart_disease_risk", 0)
    stroke_risk = predictions.get("stroke_risk", 0)
    alcohol_impact = predictions.get("alcohol_impact_score", 0)
    age = input_data.get("age", 40)
    alcohol_pct = input_data.get("alcohol_percentage", 0)
    
    # Get DNA-specific risks if available
    alcoholism_risk = predictions.get("alcoholism_risk", 0)
    liver_risk = predictions.get("liver_damage_risk", 0)
    neuro_impact = predictions.get("neurological_impact", 0)
    
    # General recommendations
    if alcohol_pct > 0:
        recommendations.append(f"Your current alcohol consumption is {alcohol_pct}% of recommended maximum. " +
                              ("Consider reducing intake." if alcohol_pct > 30 else "This is within moderate limits."))
    
    # Heart disease recommendations
    if heart_risk > 20:
        recommendations.append("Your heart disease risk is elevated. Consider regular cardiovascular check-ups.")
        if alcohol_pct > 20:
            recommendations.append("Reducing alcohol consumption may help lower your heart disease risk.")
    
    # Stroke recommendations
    if stroke_risk > 15:
        recommendations.append("Your stroke risk is above average. Monitor blood pressure regularly.")
        if alcohol_pct > 30:
            recommendations.append("High alcohol consumption significantly increases stroke risk. Consider reducing intake.")
    
    # Age-specific recommendations
    if age > 50 and alcohol_pct > 20:
        recommendations.append("As we age, alcohol tolerance decreases. Consider reducing intake after age 50.")
    
    # DNA-specific recommendations
    if alcoholism_risk > 60:
        recommendations.append("Your DNA variants indicate higher susceptibility to alcohol dependence. Consider limiting consumption and being aware of this predisposition.")
    
    if liver_risk > 50:
        recommendations.append("Your DNA profile shows increased risk for alcohol-related liver damage. Regular liver function tests are recommended if you consume alcohol regularly.")
    
    if neuro_impact > 50:
        recommendations.append("Your DNA variants suggest higher sensitivity to alcohol's neurological effects. You may experience stronger effects from alcohol than others.")
    
    # Add general health recommendations
    recommendations.append("Regular exercise and a balanced diet can help mitigate health risks regardless of genetic predisposition.")
    
    if alcoholism_risk > 40 or liver_risk > 40:
        recommendations.append("Consider discussing your DNA risk profile with a healthcare provider who specializes in addiction medicine or hepatology.")
    
    return recommendations