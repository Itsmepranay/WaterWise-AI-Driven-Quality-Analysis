import React from "react";
import ReactMarkdown from "react-markdown";

const PredictionResult = ({ result }) => {
  return (
    <div className="bg-gray-100 p-4 rounded-lg w-full shadow">
      <h2 className="text-xl font-bold text-gray-800 mb-2">Results</h2>
      <p><strong>Temperature:</strong> {result.temperature} °C</p>
      <p><strong>pH Level:</strong> {result.pH}</p>
      <p><strong>Conductivity:</strong> {result.conductivity} µmhos/cm</p>

      <h3 className="text-lg font-semibold mt-4">Precaution Advice</h3>
      <div className="text-gray-700">
        {result.precaution_advice ? (
          <ReactMarkdown>{result.precaution_advice}</ReactMarkdown>
        ) : (
          "No advice available."
        )}
      </div>
    </div>
  );
};

export default PredictionResult;
