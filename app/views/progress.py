from flask import Blueprint, render_template, request
from ..models import WorkoutLog
from .plotting import create_progress_plot

progress = Blueprint('progress', __name__)

@progress.route('/view_progress/<int:user_id>')
def view_progress(user_id):
    logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    plot = create_progress_plot(logs)  # Function to create a plot
    return render_template('progress.html', logs=logs, plot=plot)

