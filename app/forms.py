from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class RegistrationForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    body_measurements = TextAreaField('Body Measurements', validators=[DataRequired()])
    training_experience = SelectField('Training Experience', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[DataRequired()])
    dexa_scan_results = TextAreaField('DEXA Scan Results', validators=[Optional()])

class WorkoutLogForm(FlaskForm):
    exercises = TextAreaField('Exercises', validators=[DataRequired()])

class FoodLogForm(FlaskForm):
    name = StringField('Food Name', validators=[DataRequired(), Length(max=100)])
    calories = FloatField('Calories', validators=[DataRequired()])
    protein = FloatField('Protein', validators=[DataRequired()])
    carbs = FloatField('Carbs', validators=[DataRequired()])
    fats = FloatField('Fats', validators=[DataRequired()])

