import re

SUGGESTIONS = {
    "joy": [
        "Keep spreading your positivity — it is contagious!",
        "Write down what is making you happy today",
        "Share your good mood with someone who might need it",
        "Use this positive energy to build healthy habits"
    ],
    "sadness": [
        "It is okay to feel sad — your feelings are valid",
        "Try a short 10-minute walk outside",
        "Reach out to a friend or family member you trust",
        "Remember: every difficult day is followed by a new one"
    ],
    "anxiety": [
        "Try box breathing: inhale 4s, hold 4s, exhale 4s",
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
        "Challenge negative thoughts: is this fear realistic?",
        "Take one small step toward what scares you today"
    ],
    "neutral": [
        "Take a moment to check in with yourself today",
        "Try something new or creative today",
        "Even a short stretch or walk can boost your mood",
        "Read something inspiring or learn something new"
    ]
}

EMOTION_COLORS = {
    'joy': '#FFD700',
    'sadness': '#4169E1',
    'anxiety': '#FF8C00',
    'anger': '#DC143C',
    'fear': '#8B008B',
    'neutral': '#20B2AA'
}

CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'want to die', 'end my life',
    'no reason to live', 'better off dead', 'end it all',
    'harm myself', 'self harm'
]

def check_crisis(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRISIS_KEYWORDS)

def extract_key_phrases(text):
    negative_phrases = [
        'feel lonely', 'feel alone', 'no one cares', 'hate myself',
        'worthless', 'hopeless', 'feel empty', 'no motivation',
        'cant sleep', 'feeling lost', 'no hope', 'feel depressed',
        'feel anxious', 'feel stressed', 'feel numb', 'feel helpless'
    ]
    positive_phrases = [
        'feel happy', 'feel great', 'feel good', 'doing well',
        'feeling better', 'grateful', 'thankful', 'excited',
        'feel strong', 'feel confident', 'feel peaceful', 'feel calm'
    ]
    text_lower = text.lower()
    found_negative = [p for p in negative_phrases if p in text_lower]
    found_positive = [p for p in positive_phrases if p in text_lower]
    return found_negative, found_positive