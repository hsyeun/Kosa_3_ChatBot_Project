from utils.Preprocess import Preprocess
from IntentModel import IntentModel
from konlpy.tag import Komoran
komoran = Komoran(userdic='Data_Increase/user_dict(MvTitle).tsv')
p=Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dict.tsv')

intent = IntentModel(model_name='intent_model.h5',proprocess=p)
while True:
    loc,thr,mvt=[],[],[]
    q = input('\n궁금한게 뭔가요?\n>>>')
    if q == 'q' or q == 'ㅂ':
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
    if predict == 0:
        print("요청하신 영화 정보입니다.")
    elif predict == 1:
        if len(loc) == 0:
            loc = input('현재 위치를 알려주세요.\n>>>')
        print(f'{loc}의 영화관 입니다.')
    elif predict == 2:
        print("비슷한 장르의 영화입니다.")
    elif predict == 3:
        if len(loc) == 0:
            loc = input('위치를 말해주세요.\n>>>')
        if len(thr) == 0:
            thr = input('어느 영화관에서 보실래요?\n>>>')
        if len(mvt) == 0:
            mvt = input('원하는 영화를 입력하세요.\n>>>')
        print(f'{loc} {thr}의 {mvt} 상영시간표 입니다.') 