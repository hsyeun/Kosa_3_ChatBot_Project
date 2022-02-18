from utils.Preprocess import Preprocess
from IntentModel import IntentModel

p=Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

intent = IntentModel(model_name='intent_model.h5',proprocess=p)
while True:
    q = input('\n궁금한게 뭔가요?\n>>>')
    if q == 'q':
        print('안녕.')
        break
    else:
        predict=intent.predict_class(q)
        predict_label = intent.labels[predict]

        print(q)
        print(predict)
        print(predict_label)