import random
from konlpy.tag import Komoran
from konlpy.tag import Okt
from itertools import combinations, permutations
import pandas as pd


komoran = Komoran(userdic='Data_increase/user_dict(MvTitle).tsv')
okt = Okt()
def incre(text):
    data_list = komoran.morphs(text)
    stop_words = ['ㄴ','어','주','시','어요','이','야','하','아','요','세','다','?','해','습니까','에','ㄹ','수']

    data_list = [word for word in data_list if not word in stop_words]
    shflist = list(permutations(data_list,len(data_list)))
    result = []
    for i in range(len(shflist)):
        result.append(list(shflist[i]))
    return result

df = pd.read_excel('대화데이터/선정_2.xlsx')
temp = []
for i in range(len(df['s'])):
    temp.append(incre(df['s'][i]))
result = []
for i in temp:
    for j in i:
        sent = ''
        for k in j:
            sent+=k+' '
        result.append(sent)
df1 = pd.DataFrame(result)
df1.to_excel('C:/dev/3rd_test/split.xlsx')