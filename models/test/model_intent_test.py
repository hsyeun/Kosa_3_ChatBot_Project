from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel

p = Preprocess()

intent = IntentModel(model_name = './models/intent/cnn_model.h5', proprocess=p)

query = "상영 스케쥴"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)