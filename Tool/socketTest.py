import socket

class Server:
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.cummdata = ''
    
    def waitForConnection(self):
        self.sock.listen()
        self.client, self.addr = self.sock.accept()
        print('connected by', self.addr)
        return True

    def recvMsg(self):
        data = self.client.recv(1024)
        if not data:
            self.closeSocket()
            return False
        self.client.sendall(data)
        return data.decode()
    
    def sendMsg(self, msg):
        self.sock.sendall(msg.encode())

    def closeSocket(self):
        self.sock.close()



if __name__ == '__main__':
    server = Server('127.0.0.1', 8080)
    server.waitForConnection()
    
    print('connected')
    while True:
        msg = server.recvMsg()
        if not msg:
            break
        print(f'msg: {msg}')