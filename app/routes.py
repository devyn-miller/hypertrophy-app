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
from .forms import RegistrationForm, WorkoutLogForm
from .views.training import training

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
    form = WorkoutLogForm()
    if form.validate_on_submit():
        user_id = request.form['user_id']
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        new_log = WorkoutLog(
            user_id=user_id,
            exercises=form.exercises.data,
            # Additional fields...
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Workout logged successfully'}), 200
    return jsonify({'error': 'Invalid data'}), 400

@training.route('/suggest_split', methods=['POST'])
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

@app.route('/view_progress/<int:user_id>', methods=['GET'])
def view_progress(user_id):
    logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    progress_data = create_progress_plot(logs)  # Assuming a function to create visual progress
    return render_template('progress.html', logs=logs, progress_data=progress_data)

@app.route('/log_food', methods=['POST'])
def log_food():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/diet', methods=['GET'])
def get_diet(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    diet_plan = adjust_dietary_goals(user)
    return jsonify(diet_plan)

@app.route('/adjust_training/<int:user_id>', methods=['POST'])
def adjust_training(user_id):
    feedback = request.form['feedback']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        new_plan = adjust_training_plan(user, feedback)
        return jsonify(new_plan=new_plan)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
