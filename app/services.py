from .models import User, WorkoutLog
from .ml_models import ProgressPredictor
from . import db
import numpy as np

def calculate_caloric_needs(user):
    # Placeholder for Basal Metabolic Rate (BMR) calculation
    if user.sex == 'male':
        bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
    else:
        bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)
    return bmr * activity_level_to_multiplier(user.activity_level)

def activity_level_to_multiplier(level):
    # Returns a multiplier corresponding to the user's activity level
    return {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }.get(level, 1)  # Default to sedentary if unknown

def adjust_dietary_goals(user, feedback=None):
    caloric_needs = calculate_caloric_needs(user)
    # Adjust macronutrient ratios based on user goals and feedback
    if feedback and 'satisfaction' in feedback:
        satisfaction = feedback['satisfaction']
        if satisfaction < 3:  # Assuming satisfaction is rated on a scale of 1-5
            # Increase protein ratio for satiety
            protein_boost = 0.05
        else:
            protein_boost = 0
    else:
        protein_boost = 0

    if user.goal == 'weight_loss':
        protein_ratio = 0.35 + protein_boost
        fat_ratio = 0.25
        carb_ratio = 0.40 - protein_boost
    elif user.goal == 'muscle_gain':
        protein_ratio = 0.30 + protein_boost
        fat_ratio = 0.20
        carb_ratio = 0.50 - protein_boost
    else:  # Maintenance or unspecified
        protein_ratio = 0.25 + protein_boost
        fat_ratio = 0.30
        carb_ratio = 0.45 - protein_boost

    return {
        'calories': caloric_needs,
        'protein': caloric_needs * protein_ratio / 4,  # 4 calories per gram of protein
        'fats': caloric_needs * fat_ratio / 9,         # 9 calories per gram of fats
        'carbs': caloric_needs * carb_ratio / 4        # 4 calories per gram of carbs
    }

def adjust_training_plan(user_id):
    user = User.query.get(user_id)
    workout_logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    
    # Example feature extraction: using workout volume and frequency as features
    X = np.array([[log.volume, log.frequency] for log in workout_logs])
    y = np.array([log.progress_metric for log in workout_logs])

    predictor = ProgressPredictor()
    predictor.train(X, y)
    
    # Predict the next step in the training plan
    next_step = predictor.predict([[user.current_volume, user.current_frequency]])
    
    # Logic to adjust the training plan based on the prediction
    # This could involve increasing volume, changing exercises, etc.
    return next_step
    
    