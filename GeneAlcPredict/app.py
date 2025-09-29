import streamlit as st
import numpy as np
import pandas as pd

# Local modules
from models.disease_predictor import DiseasePredictor
from models.data_processor import DataProcessor
from models.deep_learning_model import DNAAlcoholDeepModel
from utils.helpers import validate_input_data, generate_recommendations
from utils.visualizations import create_risk_bar_chart, create_alcohol_surface_plot, create_gene_impact_chart


st.set_page_config(page_title="DNA & Alcohol Risk Analyzer", page_icon="🧬", layout="wide")


@st.cache_resource
def load_components():
    predictor = DiseasePredictor()
    processor = DataProcessor()
    deep_model = DNAAlcoholDeepModel()
    return predictor, processor, deep_model


predictor, processor, deep_model = load_components()

st.title("🧬 DNA & Alcohol Risk Analyzer")
st.caption("Deep learning analysis of DNA-level alcoholism side effects")

analysis_mode = st.sidebar.radio("Analysis Mode", ["Individual Analysis", "Batch Analysis", "Insights"], index=0)


def individual_analysis():
    st.header("Individual Analysis")

    # Clinical inputs
    st.subheader("Clinical Data")
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

    # DNA SNP variant inputs
    st.subheader("🧬 DNA SNP Variants")
    st.caption("Adjust DNA SNP variant values (0 = protective variant, 1 = risk variant)")
    
    # Get the list of SNPs from the model
    snp_list = deep_model.get_dna_snp_list()
    
    # DNA SNPs in two rows
    dna_data = {}
    snp_row1, snp_row2 = st.columns(2)
    
    # First half of SNPs
    with snp_row1:
        st.markdown("**Alcohol Metabolism SNPs**")
        dna_data["rs1229984"] = st.slider("rs1229984 (ADH1B)", 0.0, 1.0, 0.5, 0.1, 
                                      help="ADH1B gene - affects alcohol metabolism speed")
        dna_data["rs671"] = st.slider("rs671 (ALDH2)", 0.0, 1.0, 0.5, 0.1, 
                                      help="ALDH2 gene - affects acetaldehyde processing")
        dna_data["rs698"] = st.slider("rs698 (ADH1C)", 0.0, 1.0, 0.5, 0.1,
                                      help="ADH1C gene - affects alcohol metabolism")
        dna_data["rs1800497"] = st.slider("rs1800497 (ANKK1/DRD2)", 0.0, 1.0, 0.5, 0.1,
                                      help="ANKK1/DRD2 genes - affects dopamine signaling")
    
    # Second half of SNPs
    with snp_row2:
        st.markdown("**Neurological & Addiction SNPs**")
        dna_data["rs279858"] = st.slider("rs279858 (GABRA2)", 0.0, 1.0, 0.5, 0.1,
                                       help="GABRA2 gene - GABA receptor affects alcohol response")
        dna_data["rs4680"] = st.slider("rs4680 (COMT)", 0.0, 1.0, 0.5, 0.1, 
                                      help="COMT gene - affects dopamine breakdown")
        dna_data["rs2066702"] = st.slider("rs2066702 (ADH1B*3)", 0.0, 1.0, 0.5, 0.1,
                                      help="ADH1B*3 variant - common in certain populations")
        dna_data["rs1799971"] = st.slider("rs1799971 (OPRM1)", 0.0, 1.0, 0.5, 0.1,
                                     help="OPRM1 gene - opioid receptor affects reward pathway")

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

    # Process data and get predictions
    processed = processor.process_single_patient(input_data)
    predictions = predictor.predict_diseases(processed)
    confidences = predictor.get_confidence_scores(processed)
    
    # Get deep learning predictions based on DNA SNPs
    deep_predictions = deep_model.predict(dna_data, age, alcohol_percentage)
    
    # Merge predictions
    all_predictions = {**predictions, **deep_predictions}

    st.subheader("🔬 Analysis Results")
    
    # Standard metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("❤️ Heart Disease Risk", f"{predictions['heart_disease_risk']:.1f}%")
        st.caption(f"Raw: {predictions.get('heart_raw_risk', np.nan):.3f}")
    with m2:
        st.metric("🧠 Stroke Risk", f"{predictions['stroke_risk']:.1f}%")
    with m3:
        st.metric("🍷 Alcohol-impact score", f"{predictions['alcohol_impact_score']:.1f}")
    
    # Deep learning metrics
    st.markdown("### 🧪 Deep Learning DNA-Alcohol Analysis")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("🧬 Alcoholism Risk", f"{deep_predictions['alcoholism_risk']:.1f}%", 
                 delta=f"{deep_predictions['alcoholism_risk'] - 50:.1f}" if deep_predictions['alcoholism_risk'] != 50 else None)
    with d2:
        st.metric("🔴 Liver Damage Risk", f"{deep_predictions['liver_damage_risk']:.1f}%",
                 delta=f"{deep_predictions['liver_damage_risk'] - 50:.1f}" if deep_predictions['liver_damage_risk'] != 50 else None)
    with d3:
        st.metric("🧠 Neurological Impact", f"{deep_predictions['neurological_impact']:.1f}%",
                 delta=f"{deep_predictions['neurological_impact'] - 50:.1f}" if deep_predictions['neurological_impact'] != 50 else None)
    
    # New DNA-specific heart and liver risk metrics
    d4, d5 = st.columns(2)
    with d4:
        st.metric("❤️ DNA Heart Risk", f"{deep_predictions['dna_heart_risk']:.1f}%",
                 delta=f"{deep_predictions['dna_heart_risk'] - 50:.1f}" if deep_predictions['dna_heart_risk'] != 50 else None)
    with d5:
        st.metric("🫀 DNA Liver Risk", f"{deep_predictions['dna_liver_risk']:.1f}%",
                 delta=f"{deep_predictions['dna_liver_risk'] - 50:.1f}" if deep_predictions['dna_liver_risk'] != 50 else None)

    with st.expander("Debug — Predictions and Confidence", expanded=False):
        st.write("Prediction keys:", list(all_predictions.keys()))
        st.write("Confidence keys:", list(confidences.keys()))
        st.json({"predictions": all_predictions, "confidence_scores": confidences})

    st.subheader("📈 Visualizations")
    
    # Standard risk chart
    chart = create_risk_bar_chart(predictions)
    st.plotly_chart(chart, use_container_width=True)
    
    # DNA impact visualization
    dna_variant_chart, dna_risk_chart = create_gene_impact_chart(dna_data, deep_predictions)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(dna_variant_chart, use_container_width=True)
    with col2:
        st.plotly_chart(dna_risk_chart, use_container_width=True)
    
    # Alcohol surface plot
    surf = create_alcohol_surface_plot(predictor)
    st.plotly_chart(surf, use_container_width=True)

    st.subheader("🩺 Recommendations")
    recs = generate_recommendations(all_predictions, input_data)
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