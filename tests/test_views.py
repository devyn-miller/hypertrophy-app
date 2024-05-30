import unittest
from app import create_app, db
from app.models import User

class ViewTestCase(unittest.TestCase):
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

    def test_user_registration_view(self):
        response = self.client.post('/register', data={
            'age': 25, 'sex': 'male', 'weight': 70, 'height': 175
        })
        self.assertEqual(response.status_code, 200)

    def test_adjust_training_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.post(f'/adjust_training/{user.id}', data={'feedback': 'more cardio'})
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.get(f'/user/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'age': 25, 'sex': 'male', 'weight': 70
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

