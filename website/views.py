from flask import Blueprint, render_template,request, jsonify, redirect, url_for, session
from .this_years_total_watched import get_movie_names, get_total_time

views = Blueprint('views', __name__)


@views.route('/')
def main_page():
  return render_template("base.html")

# @views.route('/process_data', methods=['POST'])
# def process_data():
#   user_name= request.form.get('user_name')
#   watched_movies = get_movie_names(user_name)
#   total_minutes, total_hours, total_minutes_by_hours, run_times_list, = get_total_time(watched_movies)
  
#   movie_list = zip(watched_movies, run_times_list)
#   session['movie_list'] = list(movie_list)

#   return redirect(url_for('views.total_watched_info',
#                            user_name=user_name, 
#                            total_minutes=total_minutes, 
#                            total_hours=total_hours,
#                            total_minutes_by_hours=total_minutes_by_hours
#                           )
#                         )

@views.route('/total_watched_info', methods=['POST'])
def info_page():
  user_name= request.form.get('user_name')
  watched_movies = get_movie_names(user_name)
  total_minutes, total_hours, total_minutes_by_hours, run_times_list, = get_total_time(watched_movies)
  
  movie_list = zip(watched_movies, run_times_list)
  
  return render_template('info_show.html',
                         user_name=user_name, 
                          total_minutes=total_minutes, 
                          total_hours=total_hours, 
                          total_minutes_by_hour=total_minutes_by_hours,
                          movie_list=movie_list)