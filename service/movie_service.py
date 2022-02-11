import pandas as pd
import config
import json

from datetime import datetime, timedelta
from urllib.request import urlopen
from urllib.parse import urlencode

# 영화목록 받아오기
class MovieList(object):
    def __init__(self, movie_list_key):
        self.movie_list_key = movie_list_key

    @property
    def serch_movies(self):
        # targetDt = datetime.now() - timedelta(days=1)
        # targetDt_str = targetDt.strftime('%Y%m%d')
        query_url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=f5eef3421c602c6cb7ea224104795888'
        print(query_url)
        with urlopen(query_url) as fin:
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        # print(result.get('movieListResult').get('movieList'))
        return [
            {   'name': entry.get('movieNm'),
                'genre': entry.get('genreAlt'),
                'director': entry.get('directors')
            }
            for entry in result.get('movieListResult').get('movieList')
        ]

box = MovieList(config.KOFIC_API_KEY)
movie = box.serch_movies
movies = box.simplify(movie)
df = pd.DataFrame(movies)
print(df)

