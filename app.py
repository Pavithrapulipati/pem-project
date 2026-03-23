import streamlit as st
import pickle
import pandas as pd

# Page config
st.set_page_config(page_title="Medical Insurance Predictor", page_icon="🩺", layout="centered")

# 🎨 Medical UI CSS
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #e0f7fa, #ffffff);
}

/* Card */
.block-container {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}

/* Title */
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #0077b6;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #555;
    font-size: 16px;
}

/* Button */
.stButton>button {
    background-color: #0077b6;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #023e8a;
}

/* Result */
.result {
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    padding: 12px;
    border-radius: 10px;
    background-color: #caf0f8;
    color: #03045e;
    animation: fadeIn 1s ease-in;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🩺 Medical Insurance Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Estimate your insurance charges easily</div>", unsafe_allow_html=True)

st.write("")

# Load model
model = None
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    st.success("Model loaded successfully ✅")
except:
    st.error("Model not found ❌")

# Inputs
age = st.slider("Age", 18, 100, 25)
sex = st.selectbox("Sex", ["Male", "Female"])
bmi = st.number_input("BMI", value=25.0)
children = st.number_input("Children", 0, 5, 0)
smoker = st.selectbox("Smoker", ["Yes", "No"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

# Encoding
sex = 1 if sex == "Female" else 0
smoker = 1 if smoker == "Yes" else 0

region_northwest = 1 if region == "northwest" else 0
region_southeast = 1 if region == "southeast" else 0
region_southwest = 1 if region == "southwest" else 0

# Prediction
if st.button("🧾 Predict Charges"):

    if model is None:
        st.error("Model not loaded ❌")
    else:
        input_data = pd.DataFrame([[
            age, sex, bmi, children, smoker,
            region_northwest, region_southeast, region_southwest
        ]], columns=[
            'age', 'sex', 'bmi', 'children', 'smoker',
            'region_northwest', 'region_southeast', 'region_southwest'
        ])

        prediction = model.predict(input_data)

        st.markdown(
            f"<div class='result'>💰 Estimated Charges: ₹ {round(prediction[0], 2)}</div>",
            unsafe_allow_html=True
        )

        if smoker == 1:
            st.warning("⚠️ Smoking significantly increases medical costs.")

