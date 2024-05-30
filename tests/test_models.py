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

if __name__ == '__main__':
    unittest.main()

