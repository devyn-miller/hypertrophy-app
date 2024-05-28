from flask import render_template, request, redirect, url_for, jsonify
from . import app, db
from .models import User, WorkoutLog, FoodItem
from .services import adjust_dietary_goals, adjust_training_plan
from .ml_models import ProgressPredictor
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from .utils.algorithms import calculate_adjustments
from .utils.validators import validate_positive_number, validate_user_age
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class RegistrationForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), validate_user_age])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired(), validate_positive_number])
    height = FloatField('Height', validators=[DataRequired()])
    body_measurements = TextAreaField('Body Measurements', validators=[DataRequired()])
    training_experience = SelectField('Training Experience', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[DataRequired()])
    dexa_scan_results = TextAreaField('DEXA Scan Results', validators=[Optional()])

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            age=form.age.data,
            sex=form.sex.data,
            weight=form.weight.data,
            height=form.height.data,
            body_measurements=form.body_measurements.data,
            training_experience=form.training_experience.data,
            goals=form.goals.data,
            dexa_scan_results=form.dexa_scan_results.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/log_workout', methods=['POST'])
def log_workout():
    workout_log = WorkoutLog(
        user_id=request.form['user_id'],
        exercises=request.form['exercises'],
        # Additional fields...
    )
    db.session.add(workout_log)
    db.session.commit()
    return 'Workout logged successfully'


@app.route('/suggest_split', methods=['POST'])
def suggest_split():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    # Expanded logic to determine split based on more detailed criteria
    if user.training_experience == 'beginner':
        recommended_split = 'Full Body'
    elif user.training_experience == 'intermediate':
        recommended_split = 'Upper/Lower'
    else:
        recommended_split = 'Push/Pull/Legs (PPL)'
    return jsonify({'recommended_split': recommended_split})

def create_progress_plot(logs):
    # Example: Assuming logs have 'date' and 'performance' attributes
    dates = [log.date for log in logs]
    performances = [log.performance for log in logs]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, performances, marker='o')
    plt.title('Performance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Performance')
    plt.grid(True)
    plt.tight_layout()

    # Convert plot to PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Return HTML img tag with base64 data
    return f'<img src="data:image/png;base64,{plot_url}" alt="Progress Plot"/>'

@app.route('/view_progress', methods=['GET'])
def view_progress():
    user_id = request.args.get('user_id')
    logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    plot = create_progress_plot(logs)  # Function to create a plot
    return render_template('progress.html', logs=logs, plot=plot)

@app.route('/log_food', methods=['POST'])
def log_food():
    food_data = {
        'name': request.form['name'],
        'calories': request.form['calories'],
        'protein': request.form['protein'],
        'carbs': request.form['carbs'],
        'fats': request.form['fats'],
        'user_id': request.form['user_id']
    }
    new_food = FoodItem(**food_data)
    db.session.add(new_food)
    db.session.commit()
    return 'Food logged successfully'

@app.route('/user/<int:user_id>/diet', methods=['GET'])
def get_diet(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    diet_plan = adjust_dietary_goals(user)
    return jsonify(diet_plan)

@app.route('/adjust_training/<int:user_id>', methods=['POST'])
def adjust_training(user_id):
    try:
        new_plan = calculate_adjustments(user_id)
        return jsonify(new_plan=new_plan), 200
    except Exception as e:
        return str(e), 500

def get_user_workout_data(user_id):
    logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    X = [[log.volume, log.frequency] for log in logs]  # Example feature extraction
    y = [log.performance for log in logs]  # Assuming 'performance' is a measurable outcome
    return X, y

@app.route('/predict_progress/<int:user_id>', methods=['GET'])
def predict_progress(user_id):
    # Assume get_user_workout_data fetches and prepares data
    X, y = get_user_workout_data(user_id)
    
    predictor = ProgressPredictor()
    predictor.train(X, y)
    
    # Example of making a prediction using new data
    new_data = [[5, 3]]  # Example new data
    prediction = predictor.predict(new_data)
    
    return jsonify({'predicted_progress': prediction.tolist()})

@app.route('/adjust_program', methods=['POST'])
def adjust_program():
    user_id = request.form['user_id']
    feedback = request.form['feedback']
    # Logic to adjust program based on feedback
    new_program = ProgressPredictor.adjust(user_id, feedback)
    return jsonify(new_program)
