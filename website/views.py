from flask import Blueprint, render_template,request, jsonify
from .this_years_total_watched import get_movie_names, get_total_time

views = Blueprint('views', __name__)


@views.route('/')
def main_page():
  return render_template("base.html")

@views.route('/total-watched-info', methods=['POST'])
def info_page():
  user_name= request.form.get('user_name')
  watched_movies = get_movie_names(user_name)
  total_minutes, total_hours, total_minutes_by_hours, run_times_list = get_total_time(watched_movies)
  return render_template('info_show.html', 
                           user_name=user_name, 
                           total_minutes=total_minutes, 
                           total_hours=total_hours, 
                           total_minutes_by_hour=total_minutes_by_hours,
                           run_times_list=run_times_list)