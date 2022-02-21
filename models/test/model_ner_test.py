from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict.bin',
               userdic='./utils/user_dict.tsv')

ner = NerModel(model_name='./ner_model_hd.h5', proprocess=p)
query = '가까운 영화관 알려줘'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)
