from flask import Flask, render_template_string, request, jsonify
from textblob import TextBlob
import re
import json

app = Flask(__name__)

EMOTION_KEYWORDS = {
    "joy": ["happy", "excited", "great", "wonderful", "amazing", "blessed",
            "fantastic", "joy", "love", "excellent", "thrilled", "grateful",
            "glad", "cheerful", "positive", "motivated", "energetic", "proud"],
    "sadness": ["sad", "lonely", "cry", "hopeless", "empty", "depressed",
                "worthless", "miserable", "unhappy", "lost", "alone", "grief",
                "heartbroken", "down", "upset", "disappointed", "failure"],
    "anxiety": ["anxious", "worried", "panic", "nervous", "overwhelmed",
                "stress", "tense", "scared", "racing", "overthink",
                "restless", "uncertain", "uneasy", "apprehensive"],
    "anger": ["angry", "furious", "rage", "frustrated", "irritated", "mad",
              "annoyed", "livid", "outraged", "hostile", "bitter", "hate",
              "resentful", "enraged"],
    "fear": ["terrified", "afraid", "frightened", "petrified", "horror",
             "dread", "paralyzed", "vulnerable", "unsafe", "terror"],
    "neutral": ["okay", "fine", "normal", "regular", "usual", "average",
                "typical", "routine", "stable", "calm", "balanced"]
}

SUGGESTIONS = {
    "joy": [
        "Keep spreading your positivity — it is contagious!",
        "Write down what is making you happy today in a gratitude journal",
        "Share your good mood with someone who might need it",
        "Use this positive energy to build healthy habits"
    ],
    "sadness": [
        "It is okay to feel sad — your feelings are valid",
        "Try a short 10-minute walk outside — fresh air helps",
        "Reach out to a friend or family member you trust",
        "Remember: every difficult day is followed by a new one"
    ],
    "anxiety": [
        "Try box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s",
        "Write down your worries to get them out of your head",
        "Break your tasks into smaller manageable steps",
        "Limit caffeine and try to get proper sleep"
    ],
    "anger": [
        "Take 10 deep breaths before responding to anything",
        "Physical exercise is great for releasing anger safely",
        "Give yourself a 20-minute cooling off period",
        "Try to identify the root cause behind the anger"
    ],
    "fear": [
        "Break down what you are afraid of into smaller parts",
        "Remind yourself of past challenges you have overcome",
        "Challenge negative thoughts — is this fear realistic?",
        "Take one small step toward what scares you today"
    ],
    "neutral": [
        "Take a moment to check in with yourself today",
        "Try something new or creative today",
        "Even a short stretch or walk can boost your mood",
        "Read something inspiring or learn something new"
    ]
}

CRISIS_KEYWORDS = ['suicide', 'kill myself', 'want to die', 'end my life',
                   'no reason to live', 'better off dead', 'end it all', 'harm myself']

EMOTION_COLORS = {
    'joy': '#FFD700', 'sadness': '#4169E1', 'anxiety': '#FF8C00',
    'anger': '#DC143C', 'fear': '#8B008B', 'neutral': '#20B2AA'
}

def analyze(text):
    text_lower = text.lower()
    is_crisis = any(kw in text_lower for kw in CRISIS_KEYWORDS)
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.2:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        scores[emotion] = sum(1 for kw in keywords if kw in text_lower)
    total = sum(scores.values())
    if total == 0:
        if polarity > 0.3:
            detected = "joy"
        elif polarity < -0.2:
            detected = "sadness"
        else:
            detected = "neutral"
        proba = {e: 5 for e in EMOTION_KEYWORDS}
        proba[detected] = 70
    else:
        proba = {e: round((s/total)*100) for e, s in scores.items()}
        detected = max(scores, key=scores.get)
    score = 50 + polarity * 30
    emotion_adj = {'joy': 25, 'neutral': 0, 'sadness': -20,
                   'anxiety': -18, 'anger': -15, 'fear': -18}
    score += emotion_adj.get(detected, 0)
    score = round(max(0, min(100, score)))
    if score >= 70:
        risk = "Low Risk"
        risk_color = "#27AE60"
    elif score >= 45:
        risk = "Moderate"
        risk_color = "#F39C12"
    elif score >= 25:
        risk = "High Risk"
        risk_color = "#E74C3C"
    else:
        risk = "Critical"
        risk_color = "#8E44AD"
    words = text.split()
    return {
        "is_crisis": is_crisis,
        "emotion": detected,
        "emotion_color": EMOTION_COLORS.get(detected, '#20B2AA'),
        "proba": proba,
        "sentiment": sentiment,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "score": score,
        "risk": risk,
        "risk_color": risk_color,
        "suggestions": SUGGESTIONS.get(detected, SUGGESTIONS['neutral']),
        "word_count": len(words),
        "unique_words": len(set(words))
    }

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MindSense AI - Mental Health Analyzer</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', sans-serif; background: #F0F2F5; color: #1A1A2E; }
  .header { background: linear-gradient(135deg, #1A1A2E, #16213E);
            padding: 25px; text-align: center; color: white; }
  .header h1 { font-size: 36px; font-weight: 800; letter-spacing: 2px; }
  .header p { color: #A0AEC0; margin-top: 8px; font-size: 15px; }
  .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
  .input-card { background: white; border-radius: 16px; padding: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 25px; }
  .input-card h2 { font-size: 20px; margin-bottom: 15px; color: #1A1A2E; }
  textarea { width: 100%; padding: 15px; border: 2px solid #E2E8F0;
             border-radius: 10px; font-size: 15px; resize: vertical;
             min-height: 140px; font-family: inherit; outline: none;
             transition: border 0.3s; }
  textarea:focus { border-color: #1A1A2E; }
  button { background: linear-gradient(135deg, #1A1A2E, #16213E);
           color: white; border: none; padding: 14px 40px;
           border-radius: 10px; font-size: 16px; font-weight: 700;
           cursor: pointer; margin-top: 15px; width: 100%;
           transition: opacity 0.2s; }
  button:hover { opacity: 0.9; }
  .results { display: none; }
  .metrics { display: grid; grid-template-columns: repeat(3, 1fr);
             gap: 20px; margin-bottom: 25px; }
  .metric-card { background: white; border-radius: 14px; padding: 22px;
                 text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.07); }
  .metric-label { font-size: 13px; color: #718096; text-transform: uppercase;
                  letter-spacing: 1px; margin-bottom: 10px; }
  .metric-value { font-size: 28px; font-weight: 800; }
  .charts { display: grid; grid-template-columns: 1fr 1fr;
            gap: 20px; margin-bottom: 25px; }
  .chart-card { background: white; border-radius: 14px; padding: 22px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.07); }
  .chart-card h3 { font-size: 15px; margin-bottom: 15px; color: #1A1A2E; }
  .suggestions-card { background: white; border-radius: 14px; padding: 25px;
                      box-shadow: 0 4px 15px rgba(0,0,0,0.07); margin-bottom: 25px; }
  .suggestions-card h3 { font-size: 18px; margin-bottom: 15px; color: #1A1A2E; }
  .suggestion-item { background: #F7FAFC; border-left: 4px solid #3498DB;
                     padding: 12px 16px; margin: 8px 0; border-radius: 0 8px 8px 0;
                     font-size: 14px; color: #2C3E50; }
  .crisis-box { background: linear-gradient(135deg, #C0392B, #922B21);
                border-radius: 12px; padding: 20px; color: white;
                margin-bottom: 20px; }
  .crisis-box h3 { font-size: 18px; margin-bottom: 10px; }
  .crisis-box p { font-size: 14px; line-height: 1.6; }
  .loading { text-align: center; padding: 20px;
             font-size: 16px; color: #718096; display: none; }
  .score-bar { background: #E2E8F0; border-radius: 10px;
               height: 12px; margin-top: 10px; overflow: hidden; }
  .score-fill { height: 100%; border-radius: 10px;
                transition: width 1s ease; }
  @media(max-width:700px) {
    .metrics { grid-template-columns: 1fr; }
    .charts { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
<div class="header">
  <h1>MindSense AI</h1>
  <p>Advanced Mental Health Analysis powered by NLP and Machine Learning</p>
</div>
<div class="container">
  <div class="input-card">
    <h2>How are you feeling today?</h2>
    <textarea id="userText" placeholder="Write freely about how you are feeling, what is on your mind, or anything you want to express. The more you write, the more accurate the analysis will be..."></textarea>
    <div id="wordCount" style="font-size:13px;color:#718096;margin-top:8px;">Word count: 0</div>
    <button onclick="analyzeText()">Analyze My Mental State</button>
  </div>
  <div class="loading" id="loading">Analyzing your emotional state...</div>
  <div class="results" id="results">
    <div id="crisisBox"></div>
    <div class="metrics">
      <div class="metric-card">
        <div class="metric-label">Detected Emotion</div>
        <div class="metric-value" id="emotionVal"></div>
        <div style="font-size:13px;color:#718096;margin-top:6px;" id="confidenceVal"></div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Sentiment</div>
        <div class="metric-value" id="sentimentVal"></div>
        <div style="font-size:13px;color:#718096;margin-top:6px;" id="polarityVal"></div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Wellness Score</div>
        <div class="metric-value" id="scoreVal"></div>
        <div class="score-bar"><div class="score-fill" id="scoreFill"></div></div>
        <div style="font-size:13px;font-weight:700;margin-top:8px;" id="riskVal"></div>
      </div>
    </div>
    <div class="charts">
      <div class="chart-card">
        <h3>Emotion Probability Distribution</h3>
        <canvas id="emotionChart" height="200"></canvas>
      </div>
      <div class="chart-card">
        <h3>Wellness Score Gauge</h3>
        <canvas id="gaugeChart" height="200"></canvas>
      </div>
    </div>
    <div class="suggestions-card">
      <h3>Personalized Suggestions</h3>
      <div id="suggestionsList"></div>
    </div>
  </div>
</div>
<script>
  let emotionChart = null;
  let gaugeChart = null;

  document.getElementById('userText').addEventListener('input', function() {
    const words = this.value.trim() ? this.value.trim().split(/\s+/).length : 0;
    document.getElementById('wordCount').textContent = 'Word count: ' + words;
  });

  async function analyzeText() {
    const text = document.getElementById('userText').value.trim();
    if (!text || text.split(' ').length < 3) {
      alert('Please write at least a few words to get an accurate analysis.');
      return;
    }
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    const response = await fetch('/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: text})
    });
    const data = await response.json();
    document.getElementById('loading').style.display = 'none';
    displayResults(data);
  }

  function displayResults(d) {
    if (d.is_crisis) {
      document.getElementById('crisisBox').innerHTML = `
        <div class="crisis-box">
          <h3>IMPORTANT - Immediate Support Available</h3>
          <p>Your message suggests you may be in distress. Please reach out for support:<br>
          <strong>iCall (India):</strong> 9152987821 &nbsp;|&nbsp;
          <strong>Vandrevala Foundation:</strong> 1860-2662-345 (24/7) &nbsp;|&nbsp;
          <strong>AASRA:</strong> 9820466627<br>
          You are not alone. Help is available right now.</p>
        </div>`;
    } else {
      document.getElementById('crisisBox').innerHTML = '';
    }
    document.getElementById('emotionVal').textContent = d.emotion.toUpperCase();
    document.getElementById('emotionVal').style.color = d.emotion_color;
    document.getElementById('confidenceVal').textContent = 'Confidence: ' + Math.max(...Object.values(d.proba)) + '%';
    const sColor = d.sentiment === 'Positive' ? '#27AE60' : d.sentiment === 'Negative' ? '#E74C3C' : '#F39C12';
    document.getElementById('sentimentVal').textContent = d.sentiment;
    document.getElementById('sentimentVal').style.color = sColor;
    document.getElementById('polarityVal').textContent = 'Polarity: ' + d.polarity + ' | Subjectivity: ' + d.subjectivity;
    document.getElementById('scoreVal').textContent = d.score + '/100';
    document.getElementById('scoreVal').style.color = d.risk_color;
    document.getElementById('scoreFill').style.width = d.score + '%';
    document.getElementById('scoreFill').style.background = d.risk_color;
    document.getElementById('riskVal').textContent = d.risk;
    document.getElementById('riskVal').style.color = d.risk_color;
    const emotions = Object.keys(d.proba);
    const values = Object.values(d.proba);
    const colors = ['#FFD700','#4169E1','#FF8C00','#DC143C','#8B008B','#20B2AA'];
    if (emotionChart) emotionChart.destroy();
    emotionChart = new Chart(document.getElementById('emotionChart'), {
      type: 'bar',
      data: {
        labels: emotions.map(e => e.charAt(0).toUpperCase() + e.slice(1)),
        datasets: [{data: values, backgroundColor: colors, borderRadius: 6}]
      },
      options: {
        plugins: {legend: {display: false}},
        scales: {y: {beginAtZero: true, max: 100,
                     title: {display: true, text: 'Probability (%)'}}}
      }
    });
    if (gaugeChart) gaugeChart.destroy();
    gaugeChart = new Chart(document.getElementById('gaugeChart'), {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [d.score, 100 - d.score],
          backgroundColor: [d.risk_color, '#E2E8F0'],
          borderWidth: 0, circumference: 180, rotation: 270
        }]
      },
      options: {
        plugins: {
          legend: {display: false},
          tooltip: {enabled: false}
        },
        cutout: '75%'
      }
    });
    const sugList = document.getElementById('suggestionsList');
    sugList.innerHTML = d.suggestions.map(s =>
      `<div class="suggestion-item">${s}</div>`).join('');
    document.getElementById('results').style.display = 'block';
    document.getElementById('results').scrollIntoView({behavior: 'smooth'});
  }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/analyze', methods=['POST'])
def analyze_route():
    data = request.get_json()
    text = data.get('text', '')
    result = analyze(text)
    return jsonify(result)

if __name__ == '__main__':
    print("Starting MindSense AI...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=False, port=5000)