from base64 import encode
from quopri import decodestring
from flask import Flask, render_template, request, jsonify, abort, make_response
# from app import create_app, socketio  # 웹소켓
import socket
import json
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, abort
# from app import create_app, socketio  # 웹소켓
import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"
port = 5050

# Flask 애플리케이션
# app = create_app(debug=True)  # 웹소켓
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app)

# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
      # 챗봇 엔진 서버 연결
      mySocket = socket.socket()
      mySocket.connect((host, port))

      # 챗봇 엔진 질의 요청
      json_data = {
            'Query' : query,
            'BotType' : bottype
      }
      message = json.dumps(json_data)
      mySocket.send(message.encode())

      # 챗봇엔진 답변 출력
      data = mySocket.recv(2048).decode()
      ret_data = json.loads(data)

      # 챗봇엔진 서버연결 소켓 닫기
      mySocket.close()

      return ret_data

@app.route('/', methods=["GET", "POST"])
def open():
      return render_template("index.html", **locals())

@app.route('/<bot_type>', methods=["GET", "POST"])
@app.route('/query/<bot_type>', methods=["POST"])
def query(bot_type):
      body = request.get_json()

      try:
            if bot_type == 'MOVIIN':
                  body = request.get_json()
                  utterance = body['userRequest']['utterance']
                  ret = get_answer_from_engine(bottype=bot_type, query=utterance)
                  ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
                  return jsonify(ret)
            else:
                  abort(404)
            
      except Exception as ex:
            abort(500)

@app.route('/message', methods=["POST"])
def send_answer():
      question = request.get_json()['message']
      
      question += '를 서버에서 로직으로 처리'
      
      return make_response(question)

if __name__ == '__main__':
      # socketio.run(app)  # 웹소켓
      app.run(host='0.0.0.0', debug=True)