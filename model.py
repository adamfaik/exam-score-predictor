# -*- coding: utf-8 -*-
"""01_Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18o9j20FOCjmU8gYCz6gpPIOKDGKaHJd3

### Phase 1: Modeling

#### 1. Load and Explore the Data
"""

# Import the files module from Colab to allow uploading local files
from google.colab import files

# Launch a file picker to upload upload the dataset from the computer
uploaded = files.upload()

# Import pandas to work with tabular data
import pandas as pd

# Read the uploaded CSV file into a DataFrame
df = pd.read_csv('student_habits_performance.csv')

#Display the first 5 rows of the dataset to understand its structure
df.head()

"""#### 2. Clean and preprocess data"""

# Import the libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Drop 'student_id' because it's just an identifier not useful for prediction
df = df.drop(columns=['student_id'])

# Separate the target (what we want to predict) — the exam score
y = df['exam_score']  # Target variable
X = df.drop(columns=['exam_score'])  # Features (everything except exam_score)

# Encode categorical columns using LabelEncoder (converts text to numbers)
label_encoders = {}  # We'll store encoders in case we need to decode later

for column in X.select_dtypes(include='object').columns:
    le = LabelEncoder()  # Create a new label encoder
    X[column] = le.fit_transform(X[column])  # Apply it to the column
    label_encoders[column] = le  # Save it so we can reuse later

# Split the data into a training set (80%) and a testing set (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Show the shape of the data to verify it worked
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

"""#### 3. Train a Random Forest Model"""

# Import the Random Forest model from scikit-learn
from sklearn.ensemble import RandomForestRegressor

# Create the model (we'll use 100 trees and a random seed for reproducibility)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train (fit) the model using the training data
model.fit(X_train, y_train)

# Model is now trained! Let's test how well it performs on the test set
y_pred = model.predict(X_test)  # Make predictions on the test set

# Evaluate the model using some metrics
from sklearn.metrics import mean_squared_error, r2_score

#Compute the regular Mean Squared Error
mse = mean_squared_error(y_test, y_pred)

# Compute the Root Mean Squared Error (RMSE) manually
rmse = np.sqrt(mse)

# Calculate R² Score (how well predictions match real values; 1.0 = perfect)
r2 = r2_score(y_test, y_pred)

# Print the results
print("RMSE (Root Mean Squared Error):", rmse)
print("R² Score:", r2)

"""#### 4. Install SHAP and use it"""

# Install SHAP
!pip install shap

#Import SHAP
import shap

# Create a SHAP explainer for the trained Random Forest model
explainer = shap.Explainer(model, X_train)

# Pick one sample from the test set to explain
sample = X_test.iloc[[0]]

# Explain how each feature contributed to the prediction
shap_values = explainer(sample)

# Visualize the impact of each feature for that one student
shap.plots.waterfall(shap_values[0])

"""#### 4. Example Code: Explain Prediction + Recommend Improvement"""

# This function takes in user input (a single row of data),
#    predicts the exam score, and recommends which habit to improve
def explain_prediction_and_suggest_improvement(input_df, model, explainer, label_encoders):
    # Step 1: Encode categorical columns using the same LabelEncoders used during training
    for column in input_df.select_dtypes(include='object').columns:
        if column in label_encoders:
            input_df[column] = label_encoders[column].transform(input_df[column])

    # Step 2: Make the prediction
    prediction = model.predict(input_df)[0]

    # Step 3: Use SHAP to explain the prediction
    shap_values = explainer(input_df)

    # Step 4: Get SHAP values as a list (1 value per feature)
    feature_impact = shap_values[0].values  # SHAP values for this sample
    feature_names = input_df.columns        # Names of the features

    # Step 5: Create a dictionary mapping each feature to its SHAP value
    impact_dict = dict(zip(feature_names, feature_impact))

    # Step 6: Find the feature with the **most negative impact** on the prediction
    feature_to_improve = min(impact_dict, key=impact_dict.get)
    impact_value = impact_dict[feature_to_improve]

    # Step 7: Return the prediction and the recommendation
    return {
        'predicted_score': round(prediction, 2),
        'habit_to_improve': feature_to_improve,
        'negative_impact': round(impact_value, 2)
    }

# Pick a student sample to test (as if it's a user's input)
sample_input = X_test.iloc[[0]]

# Call the function
result = explain_prediction_and_suggest_improvement(sample_input, model, explainer, label_encoders)

# Show the result
print("Predicted Exam Score:", result['predicted_score'])
print("Habit to Improve:", result['habit_to_improve'])
print("Negative Impact on Score:", result['negative_impact'])

"""#### 5. Save the Model and Tools for Use in the App"""

#Import joblib (used to save and load Python objects)
import joblib

# Save the trained model
joblib.dump(model, 'model.joblib')

# Save the SHAP explainer
joblib.dump(explainer, 'explainer.joblib')

# Save the label encoders dictionary
joblib.dump(label_encoders, 'label_encoders.joblib')

# Download the files to my computer

files.download('model.joblib')
files.download('explainer.joblib')
files.download('label_encoders.joblib')