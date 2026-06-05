from textblob import TextBlob
import re
from utils import SUGGESTIONS, check_crisis, extract_key_phrases

EMOTION_KEYWORDS = {
    "joy": ["happy", "excited", "great", "wonderful", "amazing", "blessed",
            "fantastic", "joy", "love", "excellent", "thrilled", "grateful",
            "glad", "cheerful", "positive", "motivated", "energetic", "proud"],
    "sadness": ["sad", "lonely", "cry", "hopeless", "empty", "depressed",
                "worthless", "miserable", "unhappy", "lost", "alone", "grief",
                "heartbroken", "down", "upset", "disappointed", "failure"],
    "anxiety": ["anxious", "worried", "panic", "nervous", "overwhelmed",
                "stress", "tense", "scared", "fear", "racing", "overthink",
                "restless", "uncertain", "dread", "uneasy", "apprehensive"],
    "anger": ["angry", "furious", "rage", "frustrated", "irritated", "mad",
              "annoyed", "livid", "outraged", "hostile", "bitter", "hate",
              "resentful", "enraged", "fed up", "explosive"],
    "fear": ["terrified", "afraid", "frightened", "petrified", "horror",
             "dread", "scared", "paralyzed", "vulnerable", "unsafe",
             "phobia", "terror", "panic", "dreading"],
    "neutral": ["okay", "fine", "normal", "regular", "usual", "average",
                "typical", "routine", "stable", "calm", "balanced", "steady"]
}

class MentalHealthAnalyzer:

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        if polarity > 0.2:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        return {
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        }

    def predict_emotion(self, text):
        text_lower = text.lower()
        scores = {}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[emotion] = score
        total = sum(scores.values())
        if total == 0:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.3:
                detected = "joy"
            elif polarity < -0.2:
                detected = "sadness"
            else:
                detected = "neutral"
            proba = {e: 0.05 for e in EMOTION_KEYWORDS}
            proba[detected] = 0.70
        else:
            proba = {e: round(s / total, 3) for e, s in scores.items()}
            detected = max(scores, key=scores.get)
        return detected, proba

    def calculate_score(self, text, emotion, sentiment):
        score = 50
        score += sentiment['polarity'] * 30
        emotion_scores = {
            'joy': 25, 'neutral': 0,
            'sadness': -20, 'anxiety': -18,
            'anger': -15, 'fear': -18
        }
        score += emotion_scores.get(emotion, 0)
        neg, pos = extract_key_phrases(text)
        score -= len(neg) * 4
        score += len(pos) * 4
        return round(max(0, min(100, score)))

    def get_risk_level(self, score):
        if score >= 70:
            return "Low Risk", "#27AE60"
        elif score >= 45:
            return "Moderate", "#F39C12"
        elif score >= 25:
            return "High Risk", "#E74C3C"
        else:
            return "Critical", "#8E44AD"

    def analyze_text_features(self, text):
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        neg_words = ['not','no','never',"don't","can't","won't","isn't","aren't"]
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "negative_words": sum(1 for w in words if w.lower() in neg_words),
            "unique_words": len(set(words)),
            "question_marks": text.count('?'),
            "exclamations": text.count('!')
        }

    def full_analysis(self, text):
        is_crisis = check_crisis(text)
        sentiment = self.analyze_sentiment(text)
        emotion, emotion_proba = self.predict_emotion(text)
        score = self.calculate_score(text, emotion, sentiment)
        risk_level, risk_color = self.get_risk_level(score)
        suggestions = SUGGESTIONS.get(emotion, SUGGESTIONS['neutral'])
        text_features = self.analyze_text_features(text)
        negative_phrases, positive_phrases = extract_key_phrases(text)
        return {
            "is_crisis": is_crisis,
            "emotion": emotion,
            "emotion_probabilities": emotion_proba,
            "sentiment": sentiment,
            "mental_health_score": score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "suggestions": suggestions,
            "text_features": text_features,
            "negative_phrases": negative_phrases,
            "positive_phrases": positive_phrases
        }