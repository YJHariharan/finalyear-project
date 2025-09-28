import streamlit as st
import numpy as np
import pandas as pd

# Local modules
from models.disease_predictor import DiseasePredictor
from models.data_processor import DataProcessor
from utils.helpers import validate_input_data, generate_recommendations
from utils.visualizations import create_risk_bar_chart, create_alcohol_surface_plot


st.set_page_config(page_title="Gene & Alcohol Risk Analyzer", page_icon="🧬", layout="wide")


@st.cache_resource
def load_components():
    predictor = DiseasePredictor()
    processor = DataProcessor()
    return predictor, processor


predictor, processor = load_components()

st.title("🧬 Gene & Alcohol Risk Analyzer")
st.caption("Rewritten app: live metrics and robust heart risk rendering")

analysis_mode = st.sidebar.radio("Analysis Mode", ["Individual Analysis", "Batch Analysis", "Insights"], index=0)


def individual_analysis():
    st.header("Individual Analysis")

    # Input form (live; no button required)
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=40)
        alcohol_percentage = st.number_input("Alcohol % (weekly avg)", min_value=0.0, max_value=100.0, value=10.0)
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
    with col2:
        systolic_bp = st.number_input("Systolic BP", min_value=80, max_value=200, value=120)
        cholesterol = st.number_input("Total Cholesterol", min_value=100, max_value=400, value=200)
        glucose = st.number_input("Fasting Glucose", min_value=60, max_value=300, value=95)
    with col3:
        smoker = st.selectbox("Smoker", ["no", "yes"], index=0)
        sex = st.selectbox("Sex", ["female", "male"], index=1)
        exercise_level = st.selectbox("Exercise Level", ["low", "medium", "high"], index=1)

    input_data = {
        "age": age,
        "alcohol_percentage": float(alcohol_percentage),
        "bmi": float(bmi),
        "systolic_bp": int(systolic_bp),
        "cholesterol": int(cholesterol),
        "glucose": int(glucose),
        "smoker": smoker,
        "sex": sex,
        "exercise_level": exercise_level,
    }

    is_valid, msg = validate_input_data(input_data)
    if not is_valid:
        st.error(msg)
        return

    processed = processor.process_single_patient(input_data)
    predictions = predictor.predict_diseases(processed)
    confidences = predictor.get_confidence_scores(processed)

    st.subheader("🔬 Analysis Results")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("❤️ Heart Disease Risk (Main)", f"{predictions['heart_disease_risk']:.1f}%")
        st.caption(f"Raw: {predictions.get('heart_raw_risk', np.nan):.3f}")
    with m2:
        st.metric("🧠 Stroke Risk", f"{predictions['stroke_risk']:.1f}%")
    with m3:
        st.metric("🍷 Alcohol-impact score", f"{predictions['alcohol_impact_score']:.1f}")

    with st.expander("Debug — Predictions and Confidence", expanded=False):
        st.write("Prediction keys:", list(predictions.keys()))
        st.write("Confidence keys:", list(confidences.keys()))
        st.json({"predictions": predictions, "confidence_scores": confidences})

    st.subheader("📈 Visualizations")
    chart = create_risk_bar_chart(predictions)
    st.plotly_chart(chart, use_container_width=True)

    surf = create_alcohol_surface_plot(predictor)
    st.plotly_chart(surf, use_container_width=True)

    st.subheader("🩺 Recommendations")
    recs = generate_recommendations(predictions, input_data)
    for r in recs:
        st.write("- ", r)


def batch_analysis():
    st.header("Batch Analysis")
    st.caption("Upload a CSV with columns matching the input fields. We'll compute risks.")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if not file:
        return

    df = pd.read_csv(file)
    results = []
    for _, row in df.iterrows():
        input_data = row.to_dict()
        ok, _ = validate_input_data(input_data)
        if not ok:
            continue
        processed = processor.process_single_patient(input_data)
        preds = predictor.predict_diseases(processed)
        results.append(preds)

    if not results:
        st.warning("No valid rows to analyze.")
        return

    out_df = pd.DataFrame(results)
    st.dataframe(out_df.head(100), use_container_width=True)
    st.write("Average risks:")
    st.write(out_df.mean().round(2))


def insights():
    st.header("Insights")
    st.write("This page will show deeper analyses. For now, adjust inputs in Individual Analysis to see live changes.")


if analysis_mode == "Individual Analysis":
    individual_analysis()
elif analysis_mode == "Batch Analysis":
    batch_analysis()
else:
    insights()