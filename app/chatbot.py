from .mood_tracker import MoodTracker
from .resources import ResourceManager
from .exercises import ExerciseManager

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
        
        # Initialize managers
        self.mood_tracker = MoodTracker()
        self.resource_manager = ResourceManager()
        self.exercise_manager = ExerciseManager()
        
        # Add conversation state tracking
        self.conversation_state = {
            'exercise_in_progress': False,
            'current_exercise': None,
            'exercise_step': 0
        }
        
        # Add trigger words for exercises
        self.exercise_triggers = {
            'anxiety': ['breathing', 'meditation'],
            'stress': ['breathing', 'meditation'],
            'sadness': ['grounding', 'meditation']
        }

    def identify_emotion_category(self, text):
        text = text.lower()
        words = set(text.split())
        
        for category, keywords in self.emotion_categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        return 'general'

    def analyze_sentiment(self, text):
        # Add your sentiment analysis code here
        # For now, using a simple keyword approach
        positive_words = {'happy', 'good', 'great', 'wonderful', 'fantastic'}
        negative_words = {'sad', 'bad', 'anxious', 'stressed', 'worried'}
        
        text = text.lower()
        words = set(text.split())
        
        if len(words.intersection(positive_words)) > len(words.intersection(negative_words)):
            return 'positive'
        elif len(words.intersection(negative_words)) > len(words.intersection(positive_words)):
            return 'negative'
        return 'neutral'

    def check_for_exercise_request(self, user_input):
        exercise_words = {'exercise', 'technique', 'help', 'calm', 'relax'}
        return any(word in user_input.lower() for word in exercise_words)

    def get_exercise_response(self, emotion_category):
        if emotion_category in self.exercise_triggers:
            import random
            exercise_type = random.choice(self.exercise_triggers[emotion_category])
            exercise = self.exercise_manager.get_exercise(exercise_type)
            
            if exercise:
                self.conversation_state['exercise_in_progress'] = True
                self.conversation_state['current_exercise'] = exercise
                self.conversation_state['exercise_step'] = 0
                
                return {
                    'type': 'exercise',
                    'content': f"Let's try the {exercise['name']}. It takes about {exercise['duration']}. Would you like to begin?"
                }
        return None

    def handle_exercise_progress(self, user_input):
        if not self.conversation_state['exercise_in_progress']:
            return None
            
        exercise = self.conversation_state['current_exercise']
        step = self.conversation_state['exercise_step']
        
        if 'stop' in user_input.lower() or 'quit' in user_input.lower():
            self.conversation_state['exercise_in_progress'] = False
            return {
                'type': 'exercise',
                'content': "We've stopped the exercise. How are you feeling now?"
            }
            
        if step < len(exercise['steps']):
            current_step = exercise['steps'][step]
            self.conversation_state['exercise_step'] += 1
            
            if step == len(exercise['steps']) - 1:
                self.conversation_state['exercise_in_progress'] = False
                return {
                    'type': 'exercise',
                    'content': f"{current_step}\n\nThat completes our exercise. How do you feel now?"
                }
            
            return {
                'type': 'exercise',
                'content': f"{current_step}\n\nLet me know when you're ready for the next step."
            }
            
        return None

    def get_response(self, user_input):
        # Check for emergency first
        is_emergency, emergency_message = self.emergency_check(user_input)
        if is_emergency:
            return {
                'response': emergency_message,
                'sentiment': 'negative',
                'emergency': True
            }
        
        # Check if we're in the middle of an exercise
        exercise_response = self.handle_exercise_progress(user_input)
        if exercise_response:
            return {
                'response': exercise_response['content'],
                'type': 'exercise',
                'sentiment': 'neutral',
                'emergency': False
            }
        
        # Get sentiment and emotion category
        sentiment = self.analyze_sentiment(user_input)
        emotion_category = self.identify_emotion_category(user_input)
        
        # Check if user is requesting an exercise
        if self.check_for_exercise_request(user_input):
            exercise_response = self.get_exercise_response(emotion_category)
            if exercise_response:
                return {
                    'response': exercise_response['content'],
                    'type': 'exercise',
                    'sentiment': sentiment,
                    'emotion_category': emotion_category,
                    'emergency': False
                }
        
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

    def emergency_check(self, text):
        emergency_keywords = ['suicide', 'kill myself', 'want to die', 'end my life']
        text = text.lower()
        
        if any(keyword in text for keyword in emergency_keywords):
            return True, """I'm concerned about what you're saying. Please know that you're not alone. 
            Consider reaching out to a mental health professional or crisis hotline:
            National Suicide Prevention Lifeline (US): 988 or 1-800-273-8255
            Crisis Text Line: Text HOME to 741741"""
        return False, None