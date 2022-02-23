import threading
import json

from Config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from utils.FindAnswer import FindAnswer
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel


# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict1.bin',
               userdic='utils/user_dict.tsv')

# 의도 파악 모델
intent = IntentModel(model_name='./intent_model.h5', proprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name='./ner_model_hd.h5', proprocess=p)


def to_client(conn, addr, params):
    db = params['db']

    try:
        db.connect()  # 디비 연결

        # 데이터 수신
        read = conn.recv(2048)  # 수신 데이터가 있을 때 까지 블로킹
        print('===========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)


        # json 데이터로 변환
        recv_json_data = read.decode()
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data

        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]
        print("의도 파악 완료"+intent_name)

        # 개체명 파악
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)
        print("개체명 파악 완료")
        print(ner_predicts)


        # 답변 검색
        try:
            f = FindAnswer(db)
            answer_text = f.search(intent_name, ner_tags)
            if intent_name == '영화문의':
                title = [s for s in ner_predicts if 'B_TER' in s][0][0]
                mvinfo = f.find_mvw_info(title)
                print('제목 : '+mvinfo[0])
                print('감독 : '+mvinfo[1])
                print('장르 : '+mvinfo[2])
                print('배우 : '+mvinfo[3])
                answer = '제목 : '+mvinfo[0] + '\n감독 : '+mvinfo[1] + '\n장르 : '+mvinfo[2] + '\n배우 : '+mvinfo[3]
            elif intent_name == '영화관문의':
                thr_name = [s for s in ner_predicts if 'B_TER' in s][0][0]
                thr_info = f.find_thr_info(thr_name)
                answer = '영화관이름 : '+thr_info[0] + '\n주소 : '+thr_info[1] + '\n전화번호 : '+thr_info[2]

        except:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."

        send_json_data_str = {
            "query" : query,
            "Answer": answer,
            "Intent": intent_name,
            "NER": str(ner_predicts)
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())

    except Exception as ex:
        print(ex)

    finally:
        if db is not None: # db 연결 끊기
            db.close()
        conn.close()


if __name__ == '__main__':

    # 질문/답변 학습 디비 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")

    port = 5050
    listen = 100

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }

        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            params
        ))
        client.start()
