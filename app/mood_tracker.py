from datetime import datetime

class MoodTracker:
    def __init__(self):
        self.mood_history = []
    
    def add_mood(self, message, sentiment, emotion_category):
        mood_entry = {
            'timestamp': datetime.now(),
            'message': message,
            'sentiment': sentiment,
            'emotion_category': emotion_category
        }
        self.mood_history.append(mood_entry)
        return self.get_mood_summary()
    
    def get_mood_summary(self):
        if not self.mood_history:
            return "No mood data available yet."
            
        # Get last 5 moods
        recent_moods = self.mood_history[-5:]
        mood_summary = "Recent Mood Pattern:\n"
        for mood in recent_moods:
            mood_summary += f"- {mood['timestamp'].strftime('%H:%M')} - {mood['emotion_category']} ({mood['sentiment']})\n"
        
        return mood_summary

    def get_mood_pattern(self):
        if len(self.mood_history) < 3:
            return "Need more data to analyze patterns"
            
        # Analyze last three moods
        recent_moods = self.mood_history[-3:]
        sentiments = [mood['sentiment'] for mood in recent_moods]
        
        if all(s == 'negative' for s in sentiments):
            return "I notice you've been feeling down lately. Would you like to talk about it?"
        elif all(s == 'positive' for s in sentiments):
            return "You've been maintaining positive spirits! What's been helping you feel good?"
        
        return "Your mood has been varying. How can I help support you?"