<<<<<<< HEAD
from msilib import sequence
=======
>>>>>>> d5dd420241fb34fedabd8bf69b5b576c627a15a3
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

<<<<<<< HEAD
class IntentModel:
  def __init__(self, model_name, proprocess):
    self.labels = {0 : '영화정보', 1 : '영화관', 2 : '영화추천', 3 : '상영표'}

    self.model = load_model(model_name)
    
    self.p = proprocess

  def predict_class(self, query):
    pos = self.p.pos(query)

    keywords = self.p.get_keywords(pos, without_tag=True)
    sequences = [self.p.get_wordidx_sequence(keywords)]

    MAX_SEQ_LEN = 40

    padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

    predict = self.model.predict(padded_seqs)
    predict_class = tf.math.argmax(predict, axis=1)
    return predict_class.numpy()[0]
=======

# 의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, proprocess):

        # 의도 클래스 별 레이블
        self.labels = {0: "인사", 1: "욕설", 2: "주문", 3: "예약", 4: "기타"}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = proprocess


    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기
        from config.GlobalParams import MAX_SEQ_LEN

        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]
>>>>>>> d5dd420241fb34fedabd8bf69b5b576c627a15a3
