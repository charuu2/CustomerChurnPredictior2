import requests

url = "http://127.0.0.1:5000/predict"

# Sample input data (Ensure all numerical values are standard Python float/int)
data = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "Yes",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": float(79.99),  # Ensure float type
    "TotalCharges": float(999.50)    # Ensure float type
}

try:
    # Send the POST request with JSON data
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:
    print("Request failed:", str(e))
