import unittest
from app import create_app, db
from app.models import User
from app.services import adjust_training_plan, adjust_dietary_goals

class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(age=25, sex='male', weight=75)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_adjust_training_plan(self):
        feedback = 'increase intensity'
        new_plan = adjust_training_plan(self.user, feedback)
        self.assertIsNotNone(new_plan)

    def test_adjust_dietary_goals(self):
        feedback = 'reduce carbs'
        new_goals = adjust_dietary_goals(self.user, feedback)
        self.assertIn('carbs', new_goals)

if __name__ == '__main__':
    unittest.main()