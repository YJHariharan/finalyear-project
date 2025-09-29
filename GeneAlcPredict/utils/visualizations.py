import plotly.graph_objects as go
import numpy as np
import plotly.express as px


def create_risk_bar_chart(preds: dict):
    labels = ["Heart", "Stroke", "Alcohol Impact", "DNA Heart", "DNA Liver"]
    values = [
        preds.get("heart_disease_risk", 0), 
        preds.get("stroke_risk", 0), 
        preds.get("alcohol_impact_score", 0),
        preds.get("dna_heart_risk", 0),
        preds.get("dna_liver_risk", 0)
    ]
    fig = go.Figure(
        data=[go.Bar(x=labels, y=values, marker_color=["crimson", "royalblue", "darkorange", "darkred", "brown"])]
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


def create_gene_impact_chart(gene_data, predictions):
    """Create a visualization showing DNA SNP impact on health risks."""
    # Prepare data for radar chart
    genes = list(gene_data.keys())
    gene_values = [gene_data[g] for g in genes]
    
    # Create radar chart for gene variants
    fig = go.Figure()
    
    # Add gene variants trace
    fig.add_trace(go.Scatterpolar(
        r=gene_values,
        theta=genes,
        fill='toself',
        name='DNA SNP Variants',
        line_color='purple'
    ))
    
    # Add risk impact reference
    fig.add_trace(go.Scatterpolar(
        r=[0.5] * len(genes),
        theta=genes,
        fill='toself',
        name='Neutral Reference',
        line_color='gray',
        opacity=0.3
    ))
    
    # Add risk predictions as a separate radar chart
    risk_labels = ["Alcoholism", "Liver Damage", "Neurological", "Heart Risk", "Liver Risk"]
    risk_values = [
        predictions.get("alcoholism_risk", 0) / 100,
        predictions.get("liver_damage_risk", 0) / 100,
        predictions.get("neurological_impact", 0) / 100,
        predictions.get("dna_heart_risk", 0) / 100,
        predictions.get("dna_liver_risk", 0) / 100
    ]
    
    # Add a second subplot for risks
    fig2 = go.Figure()
    
    # Add risk predictions trace
    fig2.add_trace(go.Scatterpolar(
        r=risk_values,
        theta=risk_labels,
        fill='toself',
        name='DNA-Based Risks',
        line_color='crimson'
    ))
    
    # Configure layout for second chart
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title="DNA-Based Health Risk Predictions",
        height=500,
        showlegend=True
    )
    
    # Return both charts as a list
    return fig, fig2