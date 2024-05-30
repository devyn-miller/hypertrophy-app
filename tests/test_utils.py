import unittest
from app import create_app, db
from app.models import User
from app.services import adjust_training_plan, adjust_dietary_goals, calculate_energy_expenditure

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
        self.assertIn('intensity increased', new_plan['description'])

    def test_adjust_dietary_goals(self):
        feedback = 'reduce carbs'
        new_goals = adjust_dietary_goals(self.user, feedback)
        self.assertIn('carbs', new_goals)

    def test_calculate_energy_expenditure(self):
        user = User(age=25, sex='male', weight=75, height=175)  # Example user details
        expected_bmr = 88.362 + (13.397 * 75) + (4.799 * 175) - (5.677 * 25)
        expected_value = expected_bmr * 1.55  # Using 'moderately_active' multiplier
        result = calculate_energy_expenditure(user=user, activity_level='moderately_active')
        self.assertAlmostEqual(result, expected_value)

if __name__ == '__main__':
    unittest.main()
    unittest.main()