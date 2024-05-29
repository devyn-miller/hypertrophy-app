from flask import Blueprint, render_template, request
from ..models import WorkoutLog
from .plotting import create_progress_plot

progress = Blueprint('progress', __name__)

@progress.route('/view_progress/<int:user_id>', methods=['GET'])
def view_progress(user_id):
    logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    progress_data = create_progress_plot(logs)
    return render_template('progress.html', logs=logs, progress_data=progress_data)


