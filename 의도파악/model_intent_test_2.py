from utils.Preprocess import Preprocess
from 의도파악.IntentModel import IntentModel
from konlpy.tag import Komoran
komoran = Komoran(userdic='Data_Increase/user_dict(MvTitle).tsv')
p=Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

intent = IntentModel(model_name='intent_model.h5',proprocess=p)
while True:
    q = input('\n궁금한게 뭔가요?\n>>>')
    if q == 'q':
        print('안녕.')
        break
    else:
        q = komoran.morphs(q)
        stop_words = ['ㄴ','어','주','시','어요','이','야','하','아','요','세','다','?','해','습니까','에','ㄹ','수']
        a = [word for word in q if not word in stop_words]
        b=''
        for i in a:
            b += i+' '
        predict=intent.predict_class(b)
        predict_label = intent.labels[predict]

        print(b)
        print(predict)
        print(predict_label)