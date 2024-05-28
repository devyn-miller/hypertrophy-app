from sklearn.linear_model import LinearRegression
import numpy as np
from app.models import User, WorkoutLog

class TrainingAdjustmentModel:
    def __init__(self):
        self.model = LinearRegression()

    def train_model(self, X, y):
        self.model.fit(X, y)

    def predict_adjustment(self, user_data):
        return self.model.predict([user_data])[0]

def calculate_adjustments(user_id):
    user = User.query.get(user_id)
    workout_logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    X = np.array([[log.volume, log.frequency] for log in workout_logs])
    y = np.array([log.progress_metric for log in workout_logs])

    model = TrainingAdjustmentModel()
    model.train_model(X, y)
    next_step = model.predict_adjustment([user.current_volume, user.current_frequency])

    return next_step

