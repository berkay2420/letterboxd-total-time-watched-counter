from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os

def configure():
  load_dotenv()

configure()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://www.omdbapi.com/"


def get_movie_names(user_name):
    
  options = Options()
  options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)
  watched_movies = []

  driver.get(f"https://letterboxd.com/{user_name}/films/diary/")
  time.sleep(1)


  year_selection_button = driver.find_element(By.XPATH, '//*[@id="content-nav"]/div[1]/section[6]/div')
  button_2024 = driver.find_element(By.XPATH, '//*[@id="html"]/body/ul[6]/li[3]/a')


  def get_movie_name(i):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="diary-table"]/tbody/tr[{i}]/td[3]/h3/a'))
    )
    movie_name = element.text
    return movie_name

  def get_movies_table():
    movies_table = driver.find_elements(By.XPATH, '//*[@id="diary-table"]/tbody/tr')
    return movies_table

  def check_older_button():
    try:
        
        button = driver.find_element(By.XPATH, '//*[@id="content"]/div/section[2]/div[2]/div[2]/a')
        
        return True
    except NoSuchElementException:
        return False

  def get_older_button():
    older_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/section[2]/div[2]/div[2]/a')
    return older_button

  year_selection_button.click()
  time.sleep(1)
  button_2024.click()
  time.sleep(1)
  movies_table = get_movies_table()

  for i in range(1,len(movies_table) + 1):
    movie_name = get_movie_name(i)
    watched_movies.append(movie_name)

  time.sleep(1)



  if check_older_button():
    older_button = get_older_button()
    older_button.click()
    time.sleep(1)
    new_movies_table = get_movies_table()
    # try:
    #   print(len(new_movies_table))
    # except:
    #   print("An exception occurred")
    for i in range(1,len(new_movies_table) + 1):
      movie_name = get_movie_name(i)
      watched_movies.append(movie_name)

  driver.quit()
  return watched_movies
  
run_times_list = []
def get_total_time(watched_movies):
  total_minutes = 0
  for movie in watched_movies:
    params = {
      "apikey": API_KEY,  
      "t": movie,   
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:  
      data = response.json()
      runtime = data.get("Runtime")
      run_times_list.append(runtime)
      if runtime and "min" in runtime:  
          runtime = int(runtime.split(" ")[0])  
          total_minutes += runtime
    else:
      print("API isteği başarısız oldu. Durum kodu:", response.status_code)

  total_hours = total_minutes // 60
  total_minutes_by_hours = total_minutes % 60
  return total_minutes, total_hours, total_minutes_by_hours, run_times_list





