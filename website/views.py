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
  year= request.form.get('year')
  
  watched_movies, release_dates = get_movie_names(user_name, year)
  total_minutes, total_hours, total_minutes_by_hours, run_times_list = get_total_time(watched_movies, release_dates )
  average_runtime_for_movie = round(total_hours / len(run_times_list), 2)
  
  total_number_of_watched_movies = len(watched_movies)

  movie_list = zip(watched_movies, run_times_list)
  max_from_movie_list = max(movie_list, key=lambda x: x[1])
  longest_movie = max_from_movie_list[0]
  longest_runtime = max_from_movie_list[1]
  return render_template('info_show.html',
                         user_name=user_name, 
                         total_minutes=total_minutes, 
                         total_hours=total_hours, 
                         total_minutes_by_hour=total_minutes_by_hours,
                         run_times_list=run_times_list,
                         #movie_list=movie_list,
                         longest_movie=longest_movie,
                         average_runtime_for_movie=average_runtime_for_movie,
                         total_number_of_watched_movies=total_number_of_watched_movies,
                         year=year,
                         longest_runtime=longest_runtime
                         )