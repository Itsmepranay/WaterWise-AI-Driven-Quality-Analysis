# WaterWise-AI-Driven-Quality-Analysis


This project predicts groundwater quality parameters (Temperature, pH, and Conductivity) based on latitude and longitude. Additionally, it provides precautionary advice using the Eden AI API.

## 🚀 Features
- Predicts **temperature**, **pH level**, and **conductivity** based on user input.
- Finds the **nearest water station** to improve prediction accuracy.
- Uses **Eden AI API** to generate precautionary advice for drinking, irrigation, and livestock use.
- Built with **Flask** (backend) and **React** (frontend).

---

## 🛠 Tech Stack
- **Frontend:** React, Tailwind CSS
- **Backend:** Flask, Scikit-learn, Joblib
- **AI Model:** Random Forest Regressor
- **APIs:** Eden AI, Geopy (for location-based predictions)

---

## 📂 Project Structure
```
📁 groundwater-quality-prediction
├── 📁 backend                # Flask backend
│   ├── app.py               # Flask API endpoints
│   ├── models/              # Trained ML models
│   ├── dataset/             # Source dataset
│   ├── requirements.txt     # Backend dependencies
├── 📁 frontend               # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js           # Main React App
│   │   ├── index.js         # Entry point
│   ├── package.json         # Frontend dependencies
├── README.md                # Project documentation
```

---

## 🔧 Setup Instructions

### 1️⃣ Backend Setup (Flask)
```bash
# Clone the repository
git clone https://github.com/Itsmepranay/WaterWise-AI-Driven-Quality-Analysis
cd WaterWise-AI-Driven-Quality-Analysis/backend

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
pip install -r requirements.txt

# Run Flask server
python app.py
```

### 2️⃣ Frontend Setup (React)
```bash
cd ../frontend
npm install  # Install dependencies
npm start    # Start React app
```

---

## 🔗 API Usage
### **POST /predict**
**Request:**
```json
{
  "latitude": 28.7041,
  "longitude": 77.1025
}
```
**Response:**
```json
{
  "temperature": 27.93,
  "pH": 7.2,
  "conductivity": 3060.0,
  "distance": 2.5,
  "precaution_advice": "Avoid direct drinking due to high conductivity."
}
```

---



