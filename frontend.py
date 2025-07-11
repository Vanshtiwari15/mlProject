import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000/predictdata"

st.title("🎓 Student Performance Prediction")

gender = st.selectbox("Gender", ["male", "female"])  # ✅ lowercase!
ethnicity = st.selectbox("Race_Ethnicity", ["group A", "group B", "group C", "group D", "group E"])  # ✅ match your training
parental_level_of_education = st.text_input("Parental Level of Education", "bachelor's degree")
lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
reading_score = st.number_input("Reading Score", min_value=0, max_value=100, value=70)
writing_score = st.number_input("Writing Score", min_value=0, max_value=100, value=70)

if st.button("Predict"):
    payload = {
        "gender": gender,
        "ethnicity": ethnicity,
        "parental_level_of_education": parental_level_of_education,
        "lunch": lunch,
        "test_preparation_course": test_preparation_course,
        "reading_score": reading_score,
        "writing_score": writing_score
    }
    st.write("Payload:", payload)

    response = requests.post(FASTAPI_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"🎉 Predicted Score: {result['prediction']:.2f}")
    else:
        st.error(f"❌ Error: {response.status_code} - {response.text}")
