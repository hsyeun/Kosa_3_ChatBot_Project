from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict1.bin',
               userdic='./utils/user_dict.tsv')

ner = NerModel(model_name='./models/ner/ner_model.h5', proprocess=p)
query = 'CGV 상영시간표 알려줘'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)
