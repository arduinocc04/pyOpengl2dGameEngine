import socket
class Client:
    def __init__(self, serverAddress, serverPort):
        self.host = serverAddress
        self.hostPort = serverPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        self.sock.connect((self.host, self.hostPort))
    def sendMsg(self, msg):
        self.sock.sendall(msg.encode())
    def recvMsg(self):
        data = self.sock.recv(1024)
        return data.decode()
    def close(self):
        self.sock.close()
    
if __name__ == '__main__':
    client = Client('127.0.0.1', 8080)
    client.connect()
    while True:
        a = input('send MSG(:q to quit): ')

        if a == ':q':
            client.close()
            break
        else:
            client.sendMsg(a)
        msg = client.recvMsg()
        print(f'Msg from server: {msg}')
        
