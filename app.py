from flask import Flask, render_template, request, jsonify, abort
import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"
port = 5050

# Flask 애플리케이션
app = Flask(__name__)

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

@app.route('/')
def open():
      return render_template("index.html")

@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
      body = request.get_json()

      try:
            if bot_type == 'TEST':
                  # API 테스트
                  ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
                  return jsonify(ret)
            else:
                  abort(404)
            
      except Exception as ex:
            abort(500)


if __name__ == '__main__':
      app.run(host='0.0.0.0', debug=True)