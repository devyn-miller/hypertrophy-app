from sklearn.linear_model import LinearRegression
import numpy as np

class TrainingAdjustmentModel:
    def __init__(self, data):
        self.model = LinearRegression()
        self.model.fit(data[['age', 'weight']], data['progress'])

    def predict_adjustment(self, user_data):
        return self.model.predict([user_data])[0]

