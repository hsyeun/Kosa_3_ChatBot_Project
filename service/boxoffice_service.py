import config
import json

from datetime import datetime, timedelta
from urllib.request import urlopen
import pandas as pd

# 영화목록 받아오기
class Boxoffice(object):
    def __init__(self, movie_list_key):
        self.movie_list_key = movie_list_key

    @property
    def get_movies(self):
        targetDt = datetime.now() - timedelta(days=1)
        targetDt_str = targetDt.strftime('%Y%m%d')
        print(targetDt_str)
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
        key = 'f5eef3421c602c6cb7ea224104795888'

        api = url + '?key=' + key + '&targetDt=' + targetDt_str

        with urlopen(api) as fin:
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        # print(result.get('boxOfficeResult').get('dailyBoxOfficeList'))
        return [
            {
                'rank': entry.get('rank'),
                'name': entry.get('movieNm'),
                'sales': entry.get('salesAcc'),
                'audi' : entry.get('audiCnt')
            }
            for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList')
        ]


box = Boxoffice(config.KOFIC_API_KEY)
movie = box.get_movies
movies = box.simplify(movie)
df = pd.DataFrame(movies)
print(df[['rank','name']])



