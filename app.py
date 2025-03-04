from flask import Flask, request, jsonify
import requests
import pandas as pd
import joblib
from geopy.distance import geodesic
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load models and scalers
rf_pH = joblib.load("D:\\projects\\embedded\\models\\rf_pH_model.pkl")
rf_temp= joblib.load("D:\\projects\\embedded\\models\\rf_temp_model.pkl")
scaler_x = joblib.load("D:\\projects\\embedded\\models\\scaler_x.pkl")
scaler_temp = joblib.load("D:\\projects\\embedded\\models\\scaler_temp.pkl")
scaler_pH = joblib.load("D:\\projects\\embedded\\models\\scaler_pH.pkl")

dataset_path = "D:\\projects\\embedded\\dataset\\maindatasetforembedded.xlsx"
df = pd.read_excel(dataset_path, engine="openpyxl").dropna()

def find_nearest_station(user_lat, user_lon):
    df_filtered = df.dropna(subset=["Latitude", "Longitude"])
    df_filtered["Latitude"] = pd.to_numeric(df_filtered["Latitude"], errors="coerce")
    df_filtered["Longitude"] = pd.to_numeric(df_filtered["Longitude"], errors="coerce")
    df_filtered = df_filtered.dropna(subset=["Latitude", "Longitude"])
    df_filtered["Distance (km)"] = df_filtered.apply(
        lambda row: geodesic((user_lat, user_lon), (row["Latitude"], row["Longitude"])).km, axis=1
    )
    nearest_station = df_filtered.loc[df_filtered["Distance (km)"].idxmin()]
    return nearest_station["Conductivity (µmhos/cm) Mean"], nearest_station["Distance (km)"]

def generate_precaution_advice(temp, pH, conductivity):
    url = "https://api.edenai.run/v2/multimodal/chat"
    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_base_64": False,
        "show_original_response": False,
        "temperature": 0,
        "max_tokens": 1000,
        "providers": ["google/gemini-1.5-flash"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "content": {'text':f"""Using the predicted water quality values below:

Temperature: {temp}°C
pH: {pH}
Conductivity: {conductivity} µmhos/cm
For each of the following usage types, generate a bullet-point list of precautionary recommendations if the water parameters deviate from their respective ideal ranges.

Direct Drinking Water

Ideal Temperature: 10°C to 25°C
Ideal pH: 6.5 to 8.5
Ideal Conductivity: Below 500 µmhos/cm
Agricultural Use (Irrigation)

Ideal Temperature: Preferably below 35°C
Ideal pH: 6.0 to 8.5
Ideal Conductivity:
Best: 250 to 750 µmhos/cm
Acceptable for most crops: Up to 2000 µmhos/cm
Caution if above 3000 µmhos/cm (risk of soil salinity)
Livestock Feeding

Ideal Temperature: Preferably below 25°C
Ideal pH: 6.0 to 8.5
Ideal Conductivity:
Best: Below 1500 µmhos/cm
Acceptable Range: 1500 to 5000 µmhos/cm
Caution if above 5000 µmhos/cm
Your response should only provide precautionary recommendations based on deviations from these ideal values, formatted in clear bullet points under each category."""}
                    },
                ],
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzc5NmQ0M2UtN2M0MS00YmZjLTlmMTEtYzVmMTllOGNhODQzIiwidHlwZSI6ImFwaV90b2tlbiJ9.fNbGuzFXtSPih7LNOvRFZAFxqE53f_zkWKEifbAzSs4"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    # Debugging: Print full API response
    print("Eden AI Response:", response_json)  

    # Extract the assistant's response
    if "google/gemini-1.5-flash" in response_json:
        return response_json["google/gemini-1.5-flash"].get("generated_text", "No advice available.")
    else:
        return "Error: Unexpected API response format"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    user_lat = data.get("latitude")
    user_lon = data.get("longitude")
    
    if user_lat is None or user_lon is None:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    conductivity, distance = find_nearest_station(user_lat, user_lon)
    user_input_scaled = scaler_x.transform([[user_lat, user_lon]])

    temp_pred_scaled = rf_temp.predict(user_input_scaled)
    pH_pred_scaled = rf_pH.predict(user_input_scaled)

    temp_pred = scaler_temp.inverse_transform(temp_pred_scaled.reshape(-1, 1))[0][0]
    pH_pred = scaler_pH.inverse_transform(pH_pred_scaled.reshape(-1, 1))[0][0]

    # Get precaution advice from Eden AI
    precaution_advice = generate_precaution_advice(temp_pred, pH_pred, conductivity)
    
    # Debugging: Print final response before sending
    print(f"Predicted Temp: {temp_pred}, pH: {pH_pred}, Conductivity: {conductivity}")
    print(f"Precaution Advice: {precaution_advice}")

    response = {
        "temperature": round(temp_pred, 2),
        "pH": round(pH_pred, 2),
        "conductivity": round(conductivity, 2),
        "distance": round(distance, 2),
        "precaution_advice": precaution_advice
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
