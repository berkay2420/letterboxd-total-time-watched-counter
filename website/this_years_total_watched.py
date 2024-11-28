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
from bs4 import BeautifulSoup


def configure():
  load_dotenv()

configure()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://www.omdbapi.com/"

def get_movie_names(user_name, year):

  options = Options()
  options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)

  watched_movies = []
  release_dates = []

  years_and_paths = {
    "2024": '//*[@id="html"]/body/ul[6]/li[3]/a',
    "2023": '//*[@id="html"]/body/ul[6]/li[4]/a',
    "2022": '//*[@id="html"]/body/ul[6]/li[5]/a',
    "2021": '//*[@id="html"]/body/ul[6]/li[6]/a', 
    "2020": '//*[@id="html"]/body/ul[6]/li[7]/a',
  }
  driver.get(f"https://letterboxd.com/{user_name}/films/diary/")
  time.sleep(1)

  year_selection_button = driver.find_element(By.XPATH, '//*[@id="content-nav"]/div[1]/section[6]/div')

  def hide_tv_shows():
    eye_button = driver.find_element(By.XPATH, '//*[@id="content-nav"]/div[1]/section[1]/div/label')
    eye_button.click()
    time.sleep(1)
    select_hide_tv_shows = driver.find_element(By.XPATH, '//*[@id="hide-toggle-menu"]/li[3]/ul/li[4]/a')
    select_hide_tv_shows.click()

  def selecet_year(year):
    year_button = driver.find_element(By.XPATH, years_and_paths[year])
    year_button.click()
  


  def get_movie_name(i):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="diary-table"]/tbody/tr[{i}]/td[3]/h3/a'))
    )
    movie_name = element.text
    return movie_name

  def get_movies_table():
    movies_table = driver.find_elements(By.XPATH, '//*[@id="diary-table"]/tbody/tr')
    return movies_table
  
  def append_movies(table):
    for i in range(1,len(table) + 1):
      movie_name = get_movie_name(i)
      watched_movies.append(movie_name)
  
  def get_release_year(i):
    element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, f'//*[@id="diary-table"]/tbody/tr[{i}]/td[3]/div'))
    
    )
    date_html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(date_html, 'html.parser')
    film_poster = soup.find('div', class_='film-poster')
    release_year = film_poster.get('data-film-release-year', None)

    if release_year==None:
      release_year="0"
    return int(release_year)
  
  def append_dates(table):
    for i in range(1,len(table) + 1):
      year = get_release_year(i)
      release_dates.append(year)

  def check_older_button():
    try:
        
        button = driver.find_element(By.XPATH, '//*[@id="content"]/div/section[2]/div[2]/div[2]/a')
        
        return True
    except NoSuchElementException:
        return False

  def get_older_button():
    older_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/section[2]/div[2]/div[2]/a')
    return older_button
  
  def click_older_button_and_wait():
    older_button = get_older_button()
    older_button.click()
    time.sleep(1)

  def get_page_numbers():
    page_numbers = driver.find_elements(By.XPATH, '//*[@id="content"]/div/section[2]/div[2]/div[3]/ul/li')
    
    return len(page_numbers) - 1
  
  def check_page_numbers():
    try:
        
        page_numbers = driver.find_elements(By.XPATH, '//*[@id="content"]/div/section[2]/div[2]/div[3]/ul/li')
        
        return True
    except NoSuchElementException:
        return False
  
  year_selection_button.click()
  time.sleep(1)
  selecet_year(year)
  time.sleep(1)
  hide_tv_shows()
  time.sleep(1)
  movies_table = get_movies_table()

  append_movies(movies_table)
  append_dates(movies_table)
  time.sleep(1)

  if check_page_numbers:
    number_of_pages = get_page_numbers()
    index = 0
    while index < number_of_pages: 
      if check_older_button():
        click_older_button_and_wait()
        new_movies_table = get_movies_table()
        append_movies(new_movies_table)
        append_dates(new_movies_table)
        index += 1

  driver.quit()
  return watched_movies, release_dates



  
def get_runtime(movie_name):

  options = Options()
  #options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)
  driver.get(f"https://letterboxd.com/film/{movie_name.lower()}/")
  time.sleep(1)
  runtime = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="film-page-wrapper"]/div[2]/section[2]/p'))
  )
  runtime_html = runtime.get_attribute('outerHTML')
  soup = BeautifulSoup(runtime_html, 'html.parser')
  runtime_text = soup.find('p', class_='text-link text-footer').get_text()
  runtime = "".join([char for char in runtime_text if char.isdigit()])
  driver.quit()
  return int(runtime)

def get_runtimes_list(movie_list):
  run_times_list = []
  for movie in movie_list:
    runtime = get_runtime(movie)
    run_times_list.append(runtime)
  return run_times_list
     


def get_total_time(watched_movies, release_dates):
  run_times_list = []
  total_minutes = 0
  for movie, date in zip(watched_movies, release_dates):
    if date == 0:
      params = {
      "apikey": API_KEY,  
      "t": movie, 
    }
    else:
      params = {
      "apikey": API_KEY,  
      "t": movie,
      "y":  date    
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:  
      data = response.json()
      runtime = data.get("Runtime")
      #print(f" {movie} {date} Runtime  From API: {runtime}")
      if runtime != "NA":
        if runtime == None or "S" in str(runtime):
          runtime = 0
          run_times_list.append(runtime)
        else:
          try:
            if "min" in runtime:  
              runtime = int(runtime.split(" ")[0])  
              run_times_list.append(runtime)
          except ValueError:
            print(f"Geçersiz runtime değeri: {runtime}. Bu öğe atlanıyor.")
            continue
      else:
        runtime = 0
        run_times_list.append(runtime)
    else:
      print("API isteği başarısız oldu. Durum kodu:", response.status_code)

  total_minutes = sum(run_times_list)
  total_hours = total_minutes // 60
  total_minutes_by_hours = total_minutes % 60
  return total_minutes, total_hours, total_minutes_by_hours, run_times_list






