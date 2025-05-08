# 📚 Exam Score Predictor & Habit Optimizer

This is a Streamlit web application that predicts a student's final exam score based on their lifestyle habits — and suggests the one habit they should improve to get better results.

---

## 🎓 Project Context

This project was developed as part of a **[school](https://formations.pantheonsorbonne.fr/fr/catalogue-des-formations/diplome-d-universite-DU/diplome-d-universite-KBVXM363/diplome-d-universite-sorbonne-data-analytics-KPMK3V7Z.html) assignment** focused on using machine learning to turn data into actionable insights. The objective was not just to build a predictive model, but also to deliver a useful, intuitive web application using real-world practices (modeling, explainability, and deployment).

---

## 📊 Dataset

The dataset used in this project is a **synthetic dataset** published on [Kaggle](https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance), titled:

**"Student Lifestyle and Performance Data"**  
- 1,000 student records
- 15+ features including:
  - Study time
  - Sleep hours
  - Social media and Netflix usage
  - Mental health rating
  - Parental education, diet quality, and more
- Target: `exam_score`

> This dataset simulates how lifestyle choices affect academic performance, making it perfect for ML-based regression and explainability projects.

---

## 🔮 Model Training Details

The predictive model was trained using the **Random Forest Regressor** algorithm, following these steps:

1. **Preprocessing:**
   - Dropped irrelevant fields like `student_id`
   - Label-encoded categorical features (e.g. gender, diet quality)
   - Split into training and testing sets (80/20 split)

2. **Training:**
   - Used `RandomForestRegressor` with 100 trees (`n_estimators=100`)
   - Trained the model on the training set
   - Evaluated with RMSE and R² on the test set

3. **Explainability:**
   - Used **SHAP (SHapley Additive exPlanations)** to identify how each feature contributes to the final exam score prediction
   - For each prediction, the app identifies the *one habit* (feature) that most negatively impacts the result — and recommends changing it

---

## ✅ Why Random Forest?

Random Forest is a strong choice for this project because:
- It handles both numerical and categorical data well
- It's **robust to outliers and noise**
- It doesn’t require much feature scaling or normalization
- It gives high accuracy **without overfitting** easily
- It's compatible with SHAP for interpreting predictions

These properties make it ideal for a real-world app where input data can vary and where **interpretability is essential**.

---

## 🛠 How to Use

1. Visit the app: [Streamlit App Link](https://exam-score-predictor-udnkbvaum7vtpaffzzx7nb.streamlit.app/)
2. Enter your lifestyle habits using sliders and dropdowns
3. Click "Predict"
4. See your predicted exam score
5. Get a clear recommendation for **which habit to improve** to boost your score

---

## 🧪 Tech Stack

- Python 3
- Streamlit
- Scikit-learn
- SHAP
- Pandas / NumPy
- Joblib

---

## 📁 File Structure

📁 exam-score-predictor/
│
├── streamlit_app.py # Main Streamlit app
├── model.joblib # Trained ML model (Random Forest)
├── explainer.joblib # SHAP explainer
├── label_encoders.joblib # Label encoders for preprocessing
├── requirements.txt # Dependencies
└── README.md # This file


---

## 🙌 Acknowledgements

- Special thanks to [Alexis Bogroff](https://www.linkedin.com/in/alexisbogroff/), our professor, for his guidance and for designing a project framework.

- Dataset by Sourav Banerjee on Kaggle  
  [Student Lifestyle and Performance Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/student-lifestyle-and-performance-data)

---

## 📬 Contact

For feedback or suggestions, feel free to open an issue.
