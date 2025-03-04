import React, { useState } from "react";
import PredictionForm from "./components/PredictionForm.jsx";
import PredictionResult from "./components/PredictionResult.jsx";

const App = () => {
  const [prediction, setPrediction] = useState(null);

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-indigo-300 p-6">
      <div className="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-md flex flex-col items-center">
        <h1 className="text-3xl font-extrabold text-gray-800 mb-6 text-center">
          🌊 Groundwater Quality Prediction
        </h1>
        <PredictionForm onPrediction={setPrediction} />
        {prediction && (
          <div className="mt-6 w-full">
            <PredictionResult result={prediction} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
