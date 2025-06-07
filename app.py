from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import io
import base64
from sklearn.preprocessing import StandardScaler

# Load the trained model and scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Load HTML frontend

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        data = request.form
        
        # Convert input to a list
        input_data = [[
            int(data["CreditScore"]),
            int(data["Geography"]),
            int(data["Gender"]),
            int(data["Age"]),
            int(data["Tenure"]),
            float(data["Balance"]),
            int(data["NumOfProducts"]),
            int(data["HasCrCard"]),
            int(data["IsActiveMember"]),
            float(data["EstimatedSalary"])
        ]]

        # Scale the data
        input_scaled = scaler.transform(input_data)

        # Predict churn
        prediction = model.predict(input_scaled)[0]

        # Generate a bar chart
        bar_url = generate_bar_chart(input_data[0])

        # Return the result to result.html
        result = "Churned" if prediction == 1 else "Not Churned"
        return render_template("result.html", prediction_text=f"Prediction: {result}", bar_url=bar_url)

    except Exception as e:
        return jsonify({"error": str(e)})

def generate_bar_chart(features):
    """Generate a bar chart from input features."""
    labels = [
        "Credit Score", "Geography", "Gender", "Age", "Tenure",
        "Balance", "Num of Products", "Has Credit Card",
        "Active Member", "Salary"
    ]
    values = features  # Use the original input values

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'red', 'green', 'orange', 'purple', 'pink', 'yellow', 'cyan', 'magenta', 'brown'])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Features")
    plt.ylabel("Values")
    plt.title("Customer Input Data Visualization")
    plt.tight_layout()

    # Convert plot to base64 image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return f"data:image/png;base64,{plot_url}"

if __name__ == "__main__":
    app.run(debug=True)
