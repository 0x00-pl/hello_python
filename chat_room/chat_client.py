import socket
import struct
import threading
import sys


def sending_thread(sock):
    while True:
        text = input('>: ').encode('utf-8')
        text_size = struct.pack('I', len(text))
        s.send(text_size)
        s.send(text)

if __name__ == '__main__':
    addr = "localhost" if len(sys.argv)<2 else sys.argv[1]
    s = socket.socket();
    s.connect((addr,8081))
    threading.Thread(target=sending_thread, args=(s,)).start()
    
    
    while True:
        text_size_data = s.recv(4)
        text_size = struct.unpack('I', text_size_data)[0]
        text = s.recv(text_size)
        print('<: ', text.decode('utf-8', errors='ignore'))
    