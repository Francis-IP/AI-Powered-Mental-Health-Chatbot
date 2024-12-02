from .mood_tracker import MoodTracker
from .resources import ResourceManager

class MentalHealthBot:
    def __init__(self):
        # Enhanced response patterns with categories
        self.responses = {
            'negative': {
                'anxiety': [
                    "I understand anxiety can be overwhelming. Have you tried any breathing exercises?",
                    "Anxiety is challenging to deal with. What typically helps you feel more grounded?",
                    "Would you like to learn some simple techniques to manage anxiety symptoms?"
                ],
                'sadness': [
                    "I hear the sadness in your words. Would you like to talk more about what's troubling you?",
                    "It's okay to feel sad. Is there something specific that triggered these feelings?",
                    "Sometimes sadness can feel heavy. What usually helps lift your spirits?"
                ],
                'stress': [
                    "Stress can be really demanding. What's causing the most pressure right now?",
                    "Let's try to break down what's causing your stress. What's the biggest concern?",
                    "Would you like to explore some stress management techniques?"
                ]
            },
            'positive': {
                'joy': [
                    "Your joy is contagious! What's making you feel particularly happy?",
                    "It's wonderful to hear you're feeling good! What's contributed to this?",
                    "Those are such positive feelings! How can we help maintain this energy?"
                ],
                'gratitude': [
                    "It's beautiful to practice gratitude. What else are you thankful for?",
                    "Appreciating the good things can be so powerful. Would you like to share more?",
                    "That's a wonderful perspective! What other positives have you noticed lately?"
                ],
                'achievement': [
                    "Congratulations! That's definitely worth celebrating. How did you accomplish this?",
                    "You should be proud of yourself! What's your next goal?",
                    "That's fantastic progress! What helped you succeed?"
                ]
            },
            'neutral': [
                "I'm here to listen. What's on your mind?",
                "Would you like to explore your feelings further?",
                "How has your day been progressing?",
                "Sometimes it helps to talk things through. What would you like to focus on?"
            ]
        }

        # Add emotion categories
        self.emotion_categories = {
            'anxiety': ['nervous', 'anxious', 'worried', 'stressed', 'panic', 'fear'],
            'sadness': ['sad', 'down', 'depressed', 'lonely', 'hopeless', 'hurt'],
            'stress': ['overwhelmed', 'pressure', 'tired', 'exhausted', 'busy'],
            'joy': ['happy', 'excited', 'great', 'wonderful', 'fantastic'],
            'gratitude': ['thankful', 'grateful', 'blessed', 'appreciate'],
            'achievement': ['proud', 'accomplished', 'succeeded', 'achieved', 'completed']
        }
        
        # Add mood tracker
        self.mood_tracker = MoodTracker()
        
        # Add resource manager
        self.resource_manager = ResourceManager()

    def identify_emotion_category(self, text):
        text = text.lower()
        words = set(text.split())
        
        for category, keywords in self.emotion_categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        return 'general'

    def get_response(self, user_input):
        # Check for emergency first
        is_emergency, emergency_message = self.emergency_check(user_input)
        if is_emergency:
            return {
                'response': emergency_message,
                'sentiment': 'negative',
                'emergency': True
            }
        
        # Get sentiment and specific emotion category
        sentiment = self.analyze_sentiment(user_input)
        emotion_category = self.identify_emotion_category(user_input)
        
        # Select appropriate response
        if sentiment in ['positive', 'negative'] and emotion_category in self.responses[sentiment]:
            response_list = self.responses[sentiment][emotion_category]
        else:
            response_list = self.responses['neutral']
        
        import random
        response = random.choice(response_list)
        
        # Add mood tracking
        mood_data = self.mood_tracker.add_mood(
            user_input, 
            sentiment,
            emotion_category
        )
        mood_pattern = self.mood_tracker.get_mood_pattern()
        
        # Add resource recommendations
        resources = None
        quick_tip = None
        if emotion_category != 'general':
            resources = self.resource_manager.get_resources(emotion_category)
            quick_tip = self.resource_manager.get_quick_tip(emotion_category)
        
        return {
            'response': response,
            'sentiment': sentiment,
            'emotion_category': emotion_category,
            'emergency': False,
            'mood_data': mood_data,
            'mood_pattern': mood_pattern,
            'resources': resources,
            'quick_tip': quick_tip
        }