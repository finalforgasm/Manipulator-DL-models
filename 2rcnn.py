# -*- coding: utf-8 -*-
"""2RCNN

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17wXePh9p0b0UKLiUbXlPUHNoB5ouJdlH
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

#finding missing values
data = pd.read_csv("/content/inverse_kinematics_data (1).csv")
data.isnull().sum()

#remove missing values
data = data.dropna()

#find outliers
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

#remove outliers
data = data[~((data < (Q1 - 1.5 * IQR)) |(data > (Q3 + 1.5 * IQR))).any(axis=1)]
data.shape

# Define the CNN model
def create_cnn_model(input_shape):
    model = models.Sequential()

    # Input layer
    model.add(layers.Input(shape=input_shape))

    # Hidden layers
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.3))

    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.3))

    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.3))

    # Output layer
    model.add(layers.Dense(2, activation='linear'))  # Outputs θ1 and θ2

    return model

# Generate synthetic data for training
def generate_data(num_samples):
    # Random joint angles θ1 and θ2
    theta1 = np.random.uniform(0, np.pi, num_samples)
    theta2 = np.random.uniform(0, np.pi, num_samples)

    # Calculate end-effector positions (x, y)
    l1, l2 = 1.0, 1.0  # Lengths of the two links
    x = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    y = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)

    # Input data (x, y)
    X = np.column_stack((x, y))

    # Output data (θ1, θ2)
    y = np.column_stack((theta1, theta2))

    return X, y

# Parameters
num_samples = 50000  # Larger dataset for better accuracy
input_shape = (2,)  # Input is (x, y)

# Generate data
#X, y = generate_data(num_samples)
X = data[['x', 'y']].values
y = data[['theta1', 'theta2']].values

# Normalize input data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and compile the model
model = create_cnn_model(input_shape)
model.compile(optimizer='adam', loss='mse')

# Train the model
history = model.fit(X_train, y_train, epochs=25, batch_size=64, validation_data=(X_test, y_test))

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print(f"Test Loss (MSE): {loss}")

# Predict joint angles for the test set
y_pred = model.predict(X_test)

# Calculate accuracy (mean absolute error in radians)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error (MAE) in radians: {mae}")

# Convert MAE to degrees for better interpretability
mae_degrees = np.degrees(mae)
print(f"Mean Absolute Error (MAE) in degrees: {mae_degrees}")

# Function to predict theta1 and theta2 based on user input (x, y)
def predict_theta1_theta2(model, scaler):
    # Take user input for x and y
    x = float(input("Enter the value of x: "))
    y = float(input("Enter the value of y: "))

    # Prepare input data
    input_data = np.array([[x, y]])

    # Normalize the input data using the same scaler used for training
    input_data_normalized = scaler.transform(input_data)

    # Predict theta1 and theta2
    predicted_angles = model.predict(input_data_normalized)

    # Extract theta1 and theta2 from the prediction
    theta1_pred, theta2_pred = predicted_angles[0]

    # Convert radians to degrees for better interpretability
    theta1_pred_deg = np.degrees(theta1_pred)
    theta2_pred_deg = np.degrees(theta2_pred)

    # Print the results
    print(f"Predicted joint angles (in radians): theta1 = {theta1_pred:.4f}, theta2 = {theta2_pred:.4f}")
    print(f"Predicted joint angles (in degrees): theta1 = {theta1_pred_deg:.4f}°, theta2 = {theta2_pred_deg:.4f}°")

# Call the function to predict theta1 and theta2
predict_theta1_theta2(model, scaler)

# Plot actual vs predicted joint angles
def plot_actual_vs_predicted(y_test, y_pred):
    plt.figure(figsize=(10, 10))

    for i, (q_real, q_pred, label) in enumerate(zip(y_test.T, y_pred.T, ['theta1', 'theta2'])):
        plt.subplot(2, 1, i + 1)
        plt.plot(q_real, label=f'{label} real', color='blue')
        plt.plot(q_pred, label=f'{label} prediction', linestyle='dashed', color='red')
        plt.legend()
        plt.xlabel("Sample Index")
        plt.ylabel("Angle (radians)")
        plt.title(f"Actual vs Predicted for {label}")

    plt.tight_layout()
    plt.show()

# Call the function to visualize results
plot_actual_vs_predicted(y_test[:200], y_pred[:200])  # Plot first 200 samples