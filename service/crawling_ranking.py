from bs4 import BeautifulSoup
from urllib.request import urlopen
from matplotlib.pyplot import title
import openpyxl
import ssl

url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur'

page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")

# print(soup)

""" titles = soup.find_all('td', 'title')

points = soup.find_all('td', 'point')

rank = 1

for title in titles:
  print(str(rank) + "위 : " + title.find('a').text + ' 평점 : ' + title.find('a'))
  rank += 1

 """

movies = soup.select("#old_content > table > tbody > tr") 
 
ranking = 1; 
 
for movie in movies: 
  movie_name = movie.select_one("td.title > div > a")
  movie_point = movie.select_one("td.point") 
  if movie_name is not None: 
    print(str(ranking) + "위 : " + movie_name.text, '평점 : ' + movie_point.text) 
    ranking += 1


