from Config.DatabaseConfig import *
from utils.Database import Database
from utils.Preprocess import Preprocess

p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dict.tsv')

db = Database(
  host=DB_HOST,
  user=DB_USER,
  password=DB_PASSWORD,
  db_name=DB_NAME)

db.connect()

query = input()

from models.intent.IntentModel import IntentModel
intent = IntentModel(model_name='./intent_model.h5', preprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

from models.ner.NerModel import NerModel
ner = NerModel(model_name='./ner_model_hd.h5', preprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : " + query)
print("=" * 40)
print("의도파악 : " + intent_name)
print("=" * 40)
print("개체명 인식")
print(predicts)
print("=" * 40)
print("답변 검색에 필요한 NER 태그 : ")
print(ner_tags)
print("=" * 40)

from utils.FindAnswer import FindAnswer

try:
  f = FindAnswer(db)
  answer_text = f.search(intent_name, ner_tags)
  print(answer_text)
  answer = f.tag_to_word(predicts, answer_text)
  print(answer)

except:
  answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."

print("답변 : " + answer)

db.close()