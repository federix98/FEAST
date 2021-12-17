import socket

from Connector import Connector

class SocketConnector(Connector):
    def __init__(self, HOST, PORT, tp="CLIENT"):
        super().__init__()
        self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.tp = tp
        print("Socket", self.tp, "created")

    def __bind__(self):
        self.sock.bind((self.HOST, self.PORT))
        print("BINDING\nTrying to eshablish a connection with ", self.HOST)
        self.sock.listen()
        self.conn, self.addr = self.sock.accept()

    def __connect__(self):
        self.sock.connect((self.HOST, self.PORT))

    def connect(self):
        if self.tp == "SERVER":
            self.__bind__()
        elif self.tp == "CLIENT":
            self.__connect__()

    def send(self, message):
        _toSend = str.encode(message + " END")
        self.sock.sendall(_toSend)
        ack = ''
        while ack != 'RCV':
            ack = self.sock.recv(1024).decode()
        print("ACK RECEIVED - CONTINUING")

    def receive(self):
        if self.conn == None:
            print("Socket is not connected")
            return
        rcvd_string = ""
        while True:
            data = self.conn.recv(1024).decode()
            if not data:
                break
            rcvd_string += data
            if "END" in rcvd_string:
                self.conn.sendall(b'RCV')
                rcvd_string = rcvd_string.replace(" END", "")
                return rcvd_string
