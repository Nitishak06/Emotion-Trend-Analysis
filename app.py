from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app) 

# 1. THE BRAIN 

print("⏳ Loading Large-Scale AI Models... Please wait.")

# Using BART-Large for reasoning and DistilBERT for emotion detection

topic_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

labels = ["education", "career and jobs", "emotional health", "physical wellness", "peace and stability"]

# Policy logic based on the detected emotion

policy_alerts = {
    "NEGATIVE": "ACTION REQUIRED: Deploy support resources for ",
    "POSITIVE": "STABILITY DETECTED: Support continued growth in "
}

# 2. THE ANALYTICS ENGINE .

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_input = data.get("text", "").strip()


    if len(user_input.strip()) < 3:
        return jsonify({
            "intent": "UNKNOWN",
            "emotion": "NEUTRAL",
            "guidance": "Please enter more meaningful text."
    })

    # AI Processing
    t_res = topic_model(user_input, labels, multi_label=True)
    topic = t_res['labels'][0]
    score = t_res['scores'][0]
    tone = sentiment_model(user_input)[0]['label']

    
    now = datetime.now()
    month_name = now.strftime("%B") 

    try:
        try:
            df_history = pd.read_csv("youth_govt_analytics.csv")
        except:
            df_history = pd.DataFrame(columns=["Date", "Month", "Input", "Topic", "Tone"])
        
        new_row = {
            "Date": now.strftime("%Y-%m-%d"), 
            "Month": month_name,
            "Input": user_input, 
            "Topic": topic, 
            "Tone": tone
        }
        df_history = pd.concat([df_history, pd.DataFrame([new_row])], ignore_index=True)
        df_history.to_csv("youth_govt_analytics.csv", index=False)
    except Exception as e:
        print(f"Logging error: {e}")

    return jsonify({
        "intent": topic.upper(),
        "confidence": round(score * 100, 1),
        "emotion": tone,
        "policy": f"STABILITY DETECTED: Support growth in {topic.upper()}",
        "guidance": "Keep building on this positive momentum!" if tone == "POSITIVE" else "Take a small break."
    })

# --- NEW: MONTHLY REPORT ROUTE ---
@app.route('/monthly_report', methods=['GET'])
def monthly_report():
    try:
        df = pd.read_csv("youth_govt_analytics.csv")
        if 'Month' not in df.columns:
            return jsonify({"error": "Older data found. Please add a new entry to start monthly tracking."})

        # Calculate average wellness
        report = df.groupby('Month').agg({
            'Tone': lambda x: round((x == 'POSITIVE').sum() / len(x) * 100),
            'Topic': lambda x: x.mode()[0] if not x.empty else "None"
        }).to_dict(orient='index')

        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)})
    


    
@app.route('/government_report', methods=['GET'])

def government_report():
    try:
        df = pd.read_csv("youth_govt_analytics.csv")
        trends = df['Topic'].value_counts().to_dict()
        
        emotion_counts = df['Tone'].value_counts().to_dict()
        
        return jsonify({
            "total_samples": len(df),
            "trends": trends,
            "emotions": emotion_counts, # Sending this to the frontend
            "latest_alert": "ANALYSIS COMPLETE: Records processed."
        })
    except Exception as e:
        return jsonify({"error": str(e)})



import os
  
@app.route('/personal_report', methods=['GET'])
def personal_report():
    try:
        if not os.path.exists("youth_govt_analytics.csv"):
            return jsonify({"history": [], "error": "CSV missing"})

        df = pd.read_csv("youth_govt_analytics.csv")
        if df.empty:
            return jsonify({"history": [], "score": 0, "top_focus": "N/A"})

        # Find the columns automatically
        tone_col = next((c for c in df.columns if 'tone' in c.lower()), df.columns[1])
        text_col = next((c for c in df.columns if 'text' in c.lower() or 'input' in c.lower()), df.columns[0])
        date_col = next((c for c in df.columns if 'date' in c.lower()), None) # Finds the Date column

        history_list = []
        for index, row in df.iterrows():
            val = str(row[tone_col]).upper()
            score_num = 80 if "POS" in val else 30
            
            
            display_date = str(row[date_col]).split(' ')[0] if date_col else f"Entry {index + 1}"
            
            history_list.append({
                "date": display_date,
                "score": score_num,
                "text": str(row[text_col])[:20]
            })

        return jsonify({
            "score": round((len(df[df[tone_col].str.contains('POS', case=False, na=False)]) / len(df)) * 100),
            "history": history_list
        })
    except Exception as e:
        return jsonify({"error": str(e), "history": []})


@app.route('/reset_data', methods=['POST'])
def reset_data():
    try:
       

        df_empty = pd.DataFrame(columns=["Date", "Month", "Input", "Topic", "Tone"])
        df_empty.to_csv("youth_govt_analytics.csv", index=False)
        return jsonify({"message": "Project data reset successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == '__main__':
    print("✅ System Active. The website can now receive accurate data.")
    app.run(port=8080, debug=False)



