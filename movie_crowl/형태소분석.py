from konlpy.tag import Komoran
import pandas as pd

df = pd.read_excel('대화데이터/선정_2.xlsx')
label=df['l']
sent=df['s']
data = []
for i in range(len(label)):
    data.append([label[i],sent[i]])
komoran = Komoran(userdic='user_dict(MvTitle).tsv')
f = open('형태소분석.txt','w', encoding='UTF8')
docs = [komoran.pos(sentence[1]) for sentence in data]
for i in docs:
    for j in i:
        f.write(j[0]+'\t'+j[1]+'\n')
f.close()