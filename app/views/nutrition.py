from flask import Blueprint, jsonify, request
from .models import User, FoodItem
from .services import adjust_dietary_goals
from .. import db

nutrition = Blueprint('nutrition', __name__)

@nutrition.route('/log_food', methods=['POST'])
def log_food():
    new_food = FoodItem(**request.form)
    db.session.add(new_food)
    db.session.commit()
    return 'Food logged successfully'

@nutrition.route('/get_diet/<int:user_id>')
def get_diet(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    diet_plan = adjust_dietary_goals(user)
    return jsonify(diet_plan)

