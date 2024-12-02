class ExerciseManager:
    def __init__(self):
        self.exercises = {
            'breathing': {
                'name': 'Box Breathing Exercise',
                'steps': [
                    "Find a comfortable position and close your eyes",
                    "Inhale slowly for 4 counts",
                    "Hold your breath for 4 counts",
                    "Exhale slowly for 4 counts",
                    "Hold for 4 counts before the next breath"
                ],
                'duration': '5 minutes'
            },
            'grounding': {
                'name': '5-4-3-2-1 Grounding Exercise',
                'steps': [
                    "Name 5 things you can see",
                    "Name 4 things you can touch",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste"
                ],
                'duration': '3-5 minutes'
            },
            'meditation': {
                'name': 'Quick Mindfulness Meditation',
                'steps': [
                    "Sit or lie comfortably",
                    "Close your eyes and breathe naturally",
                    "Focus on your breath",
                    "Notice thoughts without judgment",
                    "Gently return focus to breathing"
                ],
                'duration': '5-10 minutes'
            }
        }

    def get_exercise(self, exercise_type):
        if exercise_type in self.exercises:
            return self.exercises[exercise_type]
        return None

    def get_random_exercise(self):
        import random
        exercise_type = random.choice(list(self.exercises.keys()))
        return self.exercises[exercise_type]