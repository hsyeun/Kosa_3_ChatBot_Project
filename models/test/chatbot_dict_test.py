import pickle
from utils.Preprocess import Preprocess

f = open("./train_tools/dict/chatbot_dict1.bin", "rb")
word_index = pickle.load(f)
f.close()

sent = "언차티드 상영 시간표 알려줘"

p = Preprocess(userdic='./utils/user_dict.tsv')

pos = p.pos(sent)

keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
  try:
    print(word, word_index[word])
  except KeyError:
    print(word, word_index['OOV'])