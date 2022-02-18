from konlpy.tag import Komoran
import pandas as pd
from gensim.models import Word2Vec
from pyparsing import line_end
import time


start = time.time()

print('1) 말뭉치 데이터 읽기 시작')
df = pd.read_excel('대화데이터/선정_2.xlsx')
label=df['l']
sent=df['s']
data = []
for i in range(len(label)):
    data.append([label[i],sent[i]])
print(time.time()-start)

print('2) 형태소에서 명사만 추출 시작')
komoran = Komoran(userdic='user_dict(MvTitle).tsv')
docs = [komoran.nouns(sentence[1]) for sentence in data]
docs = [komoran.nouns(sentence[1]) for sentence in data]
print(docs)
print(time.time()-start)

print('3) 학습 시작')
model = Word2Vec(sentences=docs, window=4,hs=1,min_count=2,sg=1)
print(time.time() - start)

print('4) 모델 저장')
model.save('Embedding/nvmc.model')
print(time.time() - start)

print(model.corpus_count)
print(model.corpus_total_words)
