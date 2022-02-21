from msilib import sequence
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

from models.intent.IntentModel import IntentModel


# 개체명 인식 모델 모듈
class NerModel:
    def __init__(self, model_name, proprocess):

        # BIO 태그 클래스 별 레이블
        self.index_to_ner = {1: 'O', 2: 'B_GEN', 3: 'B_THR', 4: 'I', 5: 'B_MVW', 6: 'B_TTL'}
        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = proprocess


    # 개체명 클래스 예측
    def predict(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩처리
        max_len = 15
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)

        predict = self.model.predict(np.array([padded_seqs[0]]))        
        print("------ predict ------")
        print(predict)
        print("-------------------------\n")

        predict_class = tf.math.argmax(predict, axis=-1)        
        print("------ predict_class ------")
        print(predict_class)
        print("-------------------------\n")

        print("------ predict_class.numpy()[0] ------")
        print(predict_class.numpy()[0])
        print("-------------------------\n")

        tags = [self.index_to_ner[i] for i in predict_class.numpy()[0]]

        print(tags)

        return list(zip(keywords, tags))

    def predict_tags(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩처리
        max_len = 15
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)

        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = []
        for tag_idx in predict_class.numpy()[0]:
            if tag_idx == 1:
                continue
            tags.append(self.index_to_ner[tag_idx])

        if len(tags) == 0: 
            return None
        return tags

