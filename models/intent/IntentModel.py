from msilib import sequence
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

class IntentModel:
  def __init__(self, model_name, proprocess):
    self.labels = {0 : '영화정보', 1 : '영화관', 2 : '영화추천', 3 : '상영표'}

    self.model = load_model(model_name)
    
    self.p = proprocess

  def predict_class(self, query):
    pos = self.p.pos(query)

    keywords = self.p.get_keywords(pos, without_tag=True)
    sequences = [self.p.get_wordidx_sequence(keywords)]

    MAX_SEQ_LEN = 40

    padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

    predict = self.model.predict(padded_seqs)
    predict_class = tf.math.argmax(predict, axis=1)
    return predict_class.numpy()[0]