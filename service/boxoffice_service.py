import config
import json

from datetime import datetime, timedelta
from urllib.request import urlopen
import pandas as pd
import tensorflow as tf

from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate

# 영화목록 받아오기
class Boxoffice(object):
    def __init__(self, movie_list_key):
        self.movie_list_key = movie_list_key

    @property
    def get_movies(self):
        targetDt = datetime.now() - timedelta(days=1)
        targetDt_str = targetDt.strftime('%Y%m%d')
        query_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=f5eef3421c602c6cb7ea224104795888&targetDt=20220202'
        print(query_url)
        with urlopen(query_url) as fin:
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        # print(result.get('boxOfficeResult').get('weeklyBoxOfficeList'))
        return [
            {
                'rank': entry.get('rank'),
                'name': entry.get('movieNm'),
                'audi': entry.get('audiAcc')
            }
            for entry in result.get('boxOfficeResult').get('weeklyBoxOfficeList')
        ]

box = Boxoffice(config.KOFIC_API_KEY)
movie = box.get_movies
movies = box.simplify(movie)
df = pd.DataFrame(movies)
print(df.head(10))

rank = df['rank'].tolist()
name = df['name'].tolist()


# 단어 인덱스 시퀀스 벡터
corpus = [preprocessing.text.text_to_word_sequence(df) for text in name]
print(corpus)

#tokenizer = preprocessing.text.Tokenizer()
#tokenizer.fit_on_texts(corpus)

#sequences = tokenizer.texts_to_sequences(corpus)

#word_index = tokenizer.word_index # vocab

#MAX_SEQ_LEN = 15  # 단어 시퀀스 벡터 크기
#padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')


