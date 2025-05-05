import React, { useState } from "react";
import Typewriter from "typewriter-effect";
import "./App.css";

function App() {
  const today = new Date().toLocaleDateString();
  const [high, setHigh] = useState("");
  const [low, setLow] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await fetch("https://dummy-bitcoinpricepredictor.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ high, low }),
      });

      const data = await response.json();
      setPrediction(data.predicted_close);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      setPrediction("Error fetching prediction.");
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>BitCoin Price Predictor</h1>
      <div className="typewriter-text">
      <Typewriter
  onInit={(typewriter) => {
    typewriter
      .typeString(`Input High and Low Value to predict Close Value for today (${today})`)
      .start();
  }}
  options={{
    loop: false,
    delay: 50,
    cursor: "|", // optional: remove blinking cursor
  }}
/>

      </div>

      <div className="input-container">
        <input
          type="number"
          placeholder="Enter High Value"
          value={high}
          onChange={(e) => setHigh(e.target.value)}
        />
        <input
          type="number"
          placeholder="Enter Low Value"
          value={low}
          onChange={(e) => setLow(e.target.value)}
        />
        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {prediction && (
        <div className="result">
          Predicted Close Price: <strong>{prediction}</strong>
        </div>
      )}
    </div>
  );
}

export default App;
