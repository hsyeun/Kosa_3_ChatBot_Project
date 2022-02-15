import socket

class botServer:
      def __init__(self, srv_port, listen_num):
            self.port = srv_port  # 소켓 서버의 포트 번호
            self.listen = listen_num  # 동시 연결할 클라이언트 수
            self.mySock = None

      # sock 생성
      def create_sock(self):
            self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP/IP 소켓 생성
            self.mySock.bind(("0.0.0.0", int(self.port)))  # 서버 포트 지정
            self.mySock.listen(int(self.listen))  # 클라이언트 연결 수 지정
            return self.mySock

      # client 대기
      def ready_for_client(self):
            return self.mySock.accept()

      # sock 반환
      def get_sock(self):
            return self.mySock