from bs4 import BeautifulSoup
from urllib.request import urlopen
from matplotlib.pyplot import title
import openpyxl
import ssl
import json

def make_top_10_list():
  url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur'

  page = urlopen(url)
  soup = BeautifulSoup(page, "html.parser")

  movies = soup.select("#old_content > table > tbody > tr") 
  
  ranking = 1; 

  top10list = []
  
  for movie in movies:   
    movie_name = movie.select_one("td.title > div > a")
    # movie_point = movie.select_one("td.point")
    if movie_name is not None: 
      # print(str(ranking) + "위 : " + movie_name.text, '평점 : ' + movie_point.text + movie_name['href']) 
      data = {
        'name' : movie_name.text,
        'url' : 'https://movie.naver.com'+ movie_name['href']
      } 
      
      top10list.append(data)

      if ranking == 10:
        break
      ranking += 1
  return top10list

# make_top_10_list()


