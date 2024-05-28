from flask import Blueprint, jsonify, request
from .models import User, Exercise, TrainingProgram
from .services import adjust_training_plan
from . import db

training = Blueprint('training', __name__)

@training.route('/suggest_split', methods=['POST'])
def suggest_split():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    recommended_split = adjust_training_plan(user)
    return jsonify({'recommended_split': recommended_split})

@training.route('/view_training_plan/<int:user_id>')
def view_training_plan(user_id):
    user = User.query.get(user_id)
    training_plan = TrainingProgram.query.filter_by(user_id=user_id).first()
    return jsonify(training_plan)

@training.route('/adjust_training_plan/<int:user_id>', methods=['POST'])
def adjust_training_plan(user_id):
    new_plan = adjust_training_plan(user_id)
    return jsonify(new_plan=new_plan)
