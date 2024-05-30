import unittest
from app import create_app, db
from app.models import User, Exercise, TrainingProgram, FoodItem

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_exercise_model(self):
        exercise = Exercise(name='Squat', muscle_group='Legs')
        db.session.add(exercise)
        db.session.commit()
        self.assertIsNotNone(exercise.id)

    def test_training_program_model(self):
        user = User(age=25, sex='male', weight=70)
        program = TrainingProgram(name='Strength Training', user=user)
        db.session.add(program)
        db.session.commit()
        self.assertEqual(program.user.age, 25)

    def test_food_item_model(self):
        food = FoodItem(name='Apple', calories=95)
        db.session.add(food)
        db.session.commit()
        self.assertEqual(food.name, 'Apple')

    def test_user_complete_profile(self):
        user = User(
            age=30, sex='male', weight=80, height=180,
            body_measurements='{"chest": 42, "waist": 32}',
            training_experience='advanced',
            goals='{"main": "muscle gain", "secondary": "strength"}',
            dexa_scan_results='{"body_fat_percentage": 15}',
            progress_pictures='/path/to/image.jpg',
            streak_count=10
        )
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.get(user.id)
        self.assertEqual(retrieved_user.height, 180)
        self.assertEqual(retrieved_user.body_measurements, '{"chest": 42, "waist": 32}')
        self.assertEqual(retrieved_user.training_experience, 'advanced')
        self.assertEqual(retrieved_user.goals, '{"main": "muscle gain", "secondary": "strength"}')
        self.assertEqual(retrieved_user.dexa_scan_results, '{"body_fat_percentage": 15}')
        self.assertEqual(retrieved_user.progress_pictures, '/path/to/image.jpg')
        self.assertEqual(retrieved_user.streak_count, 10)

    def test_training_program_effectiveness(self):
        user = User(age=30, sex='male', weight=80)
        program = TrainingProgram(name='Bulk Up', user=user, effectiveness_rating=4.5)
        db.session.add(program)
        db.session.commit()
        self.assertEqual(program.effectiveness_rating, 4.5)

    def test_food_item_nutrient_tracking(self):
        food = FoodItem(name='Banana', calories=105, vitamins='Vitamin B6', minerals='Potassium')
        db.session.add(food)
        db.session.commit()
        self.assertEqual(food.vitamins, 'Vitamin B6')
        self.assertEqual(food.minerals, 'Potassium')

    def test_user_goals_serialization(self):
        user = User(
            age=30, sex='male', weight=80, height=180,
            goals='{"main": "muscle gain", "secondary": "strength"}'
        )
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.get(user.id)
        self.assertEqual(retrieved_user.goals, '{"main": "muscle gain", "secondary": "strength"}')

    def test_training_program_exercise_relationship(self):
        user = User(age=25, sex='male', weight=70)
        exercise = Exercise(name='Deadlift', muscle_group='Back')
        program = TrainingProgram(name='Strength Training', user=user)
        program.exercises.append(exercise)
        db.session.add_all([user, exercise, program])
        db.session.commit()
        self.assertIn(exercise, program.exercises)

if __name__ == '__main__':
    unittest.main()

