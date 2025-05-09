# -*- coding: utf-8 -*-
"""02_App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aB1dYmscOYt02BiPqK9oRE32mJ6p6lVv

### Phase 2: Building the App
"""

# Install streamlit
# !pip install streamlit

# Import required libraries
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Use Colab's file upload tool
# from google.colab import files

# Upload the 3 files
# uploaded = files.upload()

#Load the trained model and tools
model = joblib.load('model.joblib')
explainer = joblib.load('explainer.joblib')
label_encoders = joblib.load('label_encoders.joblib')

# Title of the app
st.title("📚 Exam Score Predictor & Habit Optimizer")
st.write("Enter your daily habits to predict your exam score and see what to improve!")

# User input fields (adjust these to match your dataset)
age = st.slider("Age", 17, 30, 20)
gender = st.selectbox("Gender", ["Male", "Female"])
study_hours = st.slider("Study hours per day", 0.0, 10.0, 2.0)
social_media = st.slider("Social media hours", 0.0, 10.0, 3.0)
netflix = st.slider("Netflix hours", 0.0, 5.0, 1.0)
part_time_job = st.selectbox("Part-time job", ["Yes", "No"])
attendance = st.slider("Attendance (%)", 0.0, 100.0, 85.0)
sleep_hours = st.slider("Sleep hours per night", 0.0, 12.0, 7.0)
diet_quality = st.selectbox("Diet quality", ["Poor", "Fair", "Good"])
exercise_freq = st.slider("Exercise frequency (per week)", 0, 14, 3)
parent_edu = st.selectbox("Parental education level", ["High School", "Bachelor", "Master"])
internet_quality = st.selectbox("Internet quality", ["Poor", "Average", "Good"])
mental_health = st.slider("Mental health rating (1–10)", 1, 10, 5)
extracurricular = st.selectbox("Extracurricular participation", ["Yes", "No"])

# Create a DataFrame from user input
input_dict = {
    'age': age,
    'gender': gender,
    'study_hours_per_day': study_hours,
    'social_media_hours': social_media,
    'netflix_hours': netflix,
    'part_time_job': part_time_job,
    'attendance_percentage': attendance,
    'sleep_hours': sleep_hours,
    'diet_quality': diet_quality,
    'exercise_frequency': exercise_freq,
    'parental_education_level': parent_edu,
    'internet_quality': internet_quality,
    'mental_health_rating': mental_health,
    'extracurricular_participation': extracurricular
}

input_df = pd.DataFrame([input_dict])

# Encode categorical columns
for column in input_df.select_dtypes(include='object').columns:
    input_df[column] = label_encoders[column].transform(input_df[column])

# Make prediction
prediction = model.predict(input_df)[0]

# Use SHAP to find the most impactful negative habit
shap_values = explainer(input_df)
impact_array = shap_values[0].values
feature_names = input_df.columns
impact_dict = dict(zip(feature_names, impact_array))
worst_habit = min(impact_dict, key=impact_dict.get)

# Show results
st.markdown(f"### 🎯 Predicted Exam Score: `{round(prediction, 2)}`")
st.markdown(f"### 💡 Suggested Improvement: Try improving `{worst_habit}` — it reduces your score by `{round(impact_dict[worst_habit], 2)}` points.")

# show SHAP explanation
if st.checkbox("Show feature impact (SHAP)"):
    st.write("Most impactful habits on your predicted score:")
    sorted_impacts = sorted(impact_dict.items(), key=lambda x: x[1])
    for feat, val in sorted_impacts:
        st.write(f"- **{feat}**: {round(val, 2)}")

