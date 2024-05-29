from . import db
from sqlalchemy import Table, Column, Integer, ForeignKey

# Define the association table for a many-to-many relationship between TrainingProgram and Exercise
training_exercises = db.Table('training_exercises',
    db.Column('training_program_id', db.Integer, db.ForeignKey('trainingprogram.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
)

# Define the association table for a many-to-many relationship between DailyIntake and FoodItem
intake_foods = db.Table('intake_foods',
    db.Column('daily_intake_id', db.Integer, db.ForeignKey('dailyintake.id'), primary_key=True),
    db.Column('food_item_id', db.Integer, db.ForeignKey('fooditem.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    body_measurements = db.Column(db.String(200))  # JSON or serialized format
    training_experience = db.Column(db.String(50))
    goals = db.Column(db.String(200))  # JSON or serialized format
    dexa_scan_results = db.Column(db.String(200))  # Optional, JSON or serialized format
    progress_pictures = db.Column(db.String(200))  # Path to progress pictures
    streak_count = db.Column(db.Integer, default=0)  # Track consecutive days of logging

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    muscle_group = db.Column(db.String(50))
    notes = db.Column(db.String(200))
    effectiveness = db.Column(db.String(100))  # New field for effectiveness notes

class TrainingProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercises = db.relationship('Exercise', secondary=training_exercises, backref='programs')
    # Additional fields as needed

class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)  # Date of the workout
    exercises = db.Column(db.String(200))
    # Additional fields...

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fats = db.Column(db.Float)
    vitamins = db.Column(db.String(200))  # New field for vitamins
    minerals = db.Column(db.String(200))  # New field for minerals
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class DailyIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_items = db.relationship('FoodItem', secondary=intake_foods, backref='daily_intakes')

