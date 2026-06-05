# MindSense AI - Mental Health Analyzer

## Why I Built This

Mental health is something nobody talks about enough — especially in India.
I wanted to build something that actually helps people understand their
emotional state using the power of AI and NLP. This project is my attempt
to combine technology with empathy.

## What Does It Do?

MindSense AI lets you type freely about how you are feeling — no filters,
no judgement. The system then analyzes your words and tells you:

- What emotion you are experiencing (Joy, Sadness, Anxiety, Anger, Fear)
- Whether your overall sentiment is Positive, Negative or Neutral
- A Wellness Score out of 100
- Your risk level and what it means
- Personalized suggestions based on your emotional state
- Emergency helpline numbers if you are in crisis

## How I Built It

I built this entirely from scratch using Python and Flask for the backend,
and plain HTML, CSS and JavaScript for the frontend. The NLP pipeline uses
TextBlob for sentiment analysis and a custom keyword-based emotion classifier
that I designed by studying emotional language patterns.

The visualizations — the bar chart and gauge — are built using Chart.js
and update in real time based on your input.

## Tech Stack

- Python 3.11
- Flask (lightweight web framework)
- TextBlob (Natural Language Processing)
- Chart.js (real-time interactive charts)
- HTML, CSS, JavaScript

## How to Run It Locally

Step 1 - Clone the repository
git clone https://github.com/HarapalKamani7/mental-health-analyzer.git

Step 2 - Install dependencies
pip install flask textblob

Step 3 - Run the app
python flask_app.py

Step 4 - Open your browser and go to
http://localhost:5000

## What I Learned

Building this project taught me how NLP works in practice — how raw human
text can be converted into meaningful numerical signals. I learned about
sentiment polarity, subjectivity scores, keyword extraction, and how to
combine multiple signals to generate a composite score. I also learned
how to build and serve a full web application using Flask.

## Wellness Score Guide

==> Score | What It Means 
70 to 100 | You are doing well — Low Risk 
45 to 69 | Some stress detected — Moderate 
25 to 44 | You may need support — High Risk 
0 to 24 | Please reach out immediately — Critical 

## If You Are Struggling Right Now

Please reach out. You are not alone.

- iCall (India): 9152987821
- Vandrevala Foundation: 1860-2662-345 (available 24 hours)
- AASRA: 9820466627

## Disclaimer

MindSense AI is built for educational and research purposes.
It is not a replacement for professional mental health care.
If you are going through a difficult time, please speak to a
qualified mental health professional.
