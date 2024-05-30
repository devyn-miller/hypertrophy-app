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

    def test_predict_progress_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.get(f'/predict_progress/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_adjust_dietary_goals_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.post(f'/adjust_dietary_goals/{user.id}', data={'feedback': 'less sugar'})
        self.assertEqual(response.status_code, 200)

    def test_view_progress(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.get(f'/progress/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_adjust_dietary_view(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.post(f'/adjust_diet/{user.id}', data={'adjustment': 'increase protein'})
        self.assertEqual(response.status_code, 200)

    def test_user_registration_error_handling(self):
        # Test with incomplete data
        response = self.client.post('/register', data={
            'age': 25,
            'sex': 'male'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

    def test_log_workout(self):
        user = User(age=25, sex='male', weight=70)
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/log_workout', data={
            'user_id': user.id,
            'exercises': 'Squat, Bench Press',
            'duration': 60
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Workout logged successfully', response.data)

    def test_log_workout_error_handling(self):
        # Test with non-existent user
        response = self.client.post('/log_workout', data={
            'user_id': 999,  # Assuming user ID 999 does not exist
            'exercises': 'Squat, Bench Press',
            'duration': 60
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.data)

if __name__ == '__main__':
    unittest.main()


