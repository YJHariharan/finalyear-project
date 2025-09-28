import plotly.graph_objects as go
import numpy as np


def create_risk_bar_chart(preds: dict):
    labels = ["Heart", "Stroke", "Alcohol Impact"]
    values = [preds.get("heart_disease_risk", 0), preds.get("stroke_risk", 0), preds.get("alcohol_impact_score", 0)]
    fig = go.Figure(
        data=[go.Bar(x=labels, y=values, marker_color=["crimson", "royalblue", "darkorange"])]
    )
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    fig.update_yaxes(title_text="Score / %")
    return fig


def create_alcohol_surface_plot(predictor):
    # Surface: age vs alcohol, z = heart risk
    ages = np.arange(18, 81, 3)
    alcohols = np.arange(0, 101, 5)
    Z = np.zeros((len(ages), len(alcohols)))
    for i, a in enumerate(ages):
        for j, ap in enumerate(alcohols):
            features = {
                "age": a,
                "alcohol_percentage": ap,
                "bmi": 25,
                "systolic_bp": 120,
                "cholesterol": 200,
                "glucose": 95,
                "smoker": 0,
                "sex_male": 1,
                "exercise_level": 1,
            }
            Z[i, j] = predictor.predict_diseases(features)["heart_disease_risk"]

    fig = go.Figure(data=[go.Surface(z=Z, x=alcohols, y=ages, colorscale="RdBu")])
    fig.update_layout(title="Heart Risk by Age and Alcohol %", scene=dict(xaxis_title="Alcohol %", yaxis_title="Age", zaxis_title="Heart Risk %"), height=450, margin=dict(l=10, r=10, t=30, b=10))
    return fig