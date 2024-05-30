import unittest
from app import create_app, db
from app.models import User, Exercise, TrainingProgram

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration_and_login(self):
        # Test registration
        response = self.client.post('/register', data={
            'age': 25, 'sex': 'male', 'weight': 70, 'height': 175
        })
        self.assertEqual(response.status_code, 200)
        # Test login
        response = self.client.post('/login', data={
            'age': 25, 'sex': 'male', 'weight': 70
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()