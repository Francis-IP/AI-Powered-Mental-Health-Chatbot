class ResourceManager:
    def __init__(self):
        self.resources = {
            'anxiety': {
                'coping_strategies': [
                    "Try the 4-7-8 breathing exercise: Inhale for 4 seconds, hold for 7, exhale for 8",
                    "Practice progressive muscle relaxation",
                    "Take a short walk to clear your mind"
                ],
                'helpful_links': [
                    "National Anxiety Foundation: https://www.anxiety.org/",
                    "Anxiety and Depression Association: https://adaa.org/"
                ],
                'exercises': [
                    "Grounding Exercise: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
                    "Box Breathing: Draw a square with your breath - 4 seconds each side"
                ]
            },
            'sadness': {
                'coping_strategies': [
                    "Write down three things you're grateful for",
                    "Reach out to a friend or family member",
                    "Do something creative that you enjoy"
                ],
                'helpful_links': [
                    "Depression Support: https://www.dbsalliance.org/",
                    "Mental Health America: https://www.mhanational.org/"
                ],
                'exercises': [
                    "Mindful Walking: Take a 10-minute walk focusing on your surroundings",
                    "Journaling Exercise: Write about your feelings for 5 minutes"
                ]
            },
            'stress': {
                'coping_strategies': [
                    "Break large tasks into smaller, manageable steps",
                    "Practice time management with the Pomodoro Technique",
                    "Take regular breaks during work"
                ],
                'helpful_links': [
                    "Stress Management Tips: https://www.stress.org/",
                    "Mindfulness Resources: https://www.mindful.org/"
                ],
                'exercises': [
                    "Deep Breathing: Take 5 deep breaths, counting to 5 on each inhale and exhale",
                    "Quick Meditation: Close your eyes and focus on your breath for 2 minutes"
                ]
            },
            'general': {
                'coping_strategies': [
                    "Maintain a regular sleep schedule",
                    "Stay hydrated and eat balanced meals",
                    "Practice self-care activities daily"
                ],
                'helpful_links': [
                    "General Mental Health Resources: https://www.mentalhealth.gov/",
                    "Self-Help Tools: https://www.helpguide.org/"
                ],
                'exercises': [
                    "Daily Mood Journal",
                    "5-minute mindfulness practice"
                ]
            }
        }

    def get_resources(self, emotion_category):
        # Get resources for specific emotion or general resources
        category = emotion_category.lower() if emotion_category.lower() in self.resources else 'general'
        resources = self.resources[category]
        
        # Format response
        response = f"\nHere are some resources that might help:\n\n"
        response += "Coping Strategies:\n"
        response += "- " + "\n- ".join(resources['coping_strategies']) + "\n\n"
        response += "Exercises:\n"
        response += "- " + "\n- ".join(resources['exercises']) + "\n\n"
        response += "Helpful Links:\n"
        response += "- " + "\n- ".join(resources['helpful_links'])
        
        return response

    def get_quick_tip(self, emotion_category):
        category = emotion_category.lower() if emotion_category.lower() in self.resources else 'general'
        import random
        return random.choice(self.resources[category]['coping_strategies'])