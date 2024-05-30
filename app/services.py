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

def adjust_dietary_goals(user, feedback=None, custom_macros=None):
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

    # Default macro ratios based on goals
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

    # Allow user customization of macro ratios if provided
    if custom_macros:
        protein_ratio = custom_macros.get('protein', protein_ratio)
        fat_ratio = custom_macros.get('fats', fat_ratio)
        carb_ratio = custom_macros.get('carbs', carb_ratio)

    return {
        'calories': caloric_needs,
        'protein': caloric_needs * protein_ratio / 4,  # 4 calories per gram of protein
        'fats': caloric_needs * fat_ratio / 9,         # 9 calories per gram of fats
        'carbs': caloric_needs * carb_ratio / 4        # 4 calories per gram of carbs
    }
def adjust_training_plan(user, feedback=None, custom_exercises=None):
    current_plan = user.retrieve_current_training_plan()  # Assuming the method is part of the user object
    if feedback and 'intensity_too_high' in feedback:
        adjustment_factor = 0.9  # Reduce volume by 10%
    elif feedback and 'intensity_too_low' in feedback:
        adjustment_factor = 1.1  # Increase volume by 10%
    else:
        adjustment_factor = 1  # No change

    # Apply adjustments to the current plan
    adjusted_plan = {
        'exercises': [
            {
                'name': exercise['name'],
                'sets': int(exercise['sets'] * adjustment_factor),
                'reps': int(exercise['reps'] * adjustment_factor)
            } for exercise in current_plan['exercises']
        ]
    }

    # Merge custom exercises provided by the user
    if custom_exercises:
        for custom_exercise in custom_exercises:
            # Find and update the exercise if it exists in the adjusted plan
            found = False
            for adj_exercise in adjusted_plan['exercises']:
                if adj_exercise['name'] == custom_exercise['name']:
                    adj_exercise.update(custom_exercise)
                    found = True
                    break
            # If not found, add as a new exercise
            if not found:
                adjusted_plan['exercises'].append(custom_exercise)

    return adjusted_plan

def calculate_energy_expenditure(user, activity_level):
    # Placeholder for Basal Metabolic Rate (BMR) calculation
    if user.sex == 'male':
        bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
    else:
        bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)
    
    # Placeholder for activity level multiplier
    activity_multiplier = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }.get(activity_level, 1)  # Default to sedentary if unknown

    return bmr * activity_multiplier

