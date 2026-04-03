# 🧠 EmotionTracker Pro: Personal NLP Insights

A web application designed to help individuals track and analyze their daily emotional patterns. This project uses **Natural Language Processing (NLP)** to turn qualitative reflections into visual mental health trends.

---

### 🚀 Key Features
* **Emotion Decoding**: Uses the **DistilBERT** model for fast, high-accuracy sentiment analysis (Positive/Negative).
* **Contextual Analysis**: Leverages the **BART-Large** model for zero-shot topic classification (Education, Career, Wellness, Stability).
* **Personal Journey Mapping**: Visualizes "Wellness Scores" over time using interactive **Chart.js** graphs.
* **Monthly Summaries**: Automatically groups data by month to identify seasonal emotional trends.

---

### 🛠️ Technical Architecture
This project implements a full-stack AI pipeline, separating heavy model inference from the user interface.

* **Backend**: Python 3.x
* **Core Libraries & Imports**: 
    * `from flask import Flask, request, jsonify`: To build the RESTful Web API.
    * `from flask_cors import CORS`: To allow cross-origin communication between Frontend and Backend.
    * `import pandas as pd`: For data manipulation and CSV-based logging (`youth_govt_analytics.csv`).
    * `from transformers import pipeline`: For seamless AI model integration (BART & DistilBERT).
    * `import datetime`: To track and timestamp emotional entries for trend analysis.
* **Frontend**: Responsive UI built with **HTML5**, **CSS3**, and **JavaScript** (ES6+).
* **Visualization**: **Chart.js** library for dynamic, interactive data rendering.
* **Database**: Local CSV logging for persistent data tracking.

---

### 📦 Dependencies
To run this project, you must install these Python libraries:
```bash
pip install flask flask-cors pandas transformers torch
```

### 💻 How to Run

* **Start the AI Server**:
  Run the Python script to activate the models and Flask API:
  ```bash
  python app.py
