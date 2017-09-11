import struct
import socket
import select
import errno

POLL_NULL = 0x00
POLL_IN = 0x01
POLL_OUT = 0x04
POLL_ERR = 0x08
POLL_HUP = 0x10
POLL_NVAL = 0x20

EVENT_NAMES = {
    POLL_NULL: 'POLL_NULL',
    POLL_IN: 'POLL_IN',
    POLL_OUT: 'POLL_OUT',
    POLL_ERR: 'POLL_ERR',
    POLL_HUP: 'POLL_HUP',
    POLL_NVAL: 'POLL_NVAL',
}
class EpollLoop(object):
    def __init__(self):
        self._epoll = select.epoll()

    def poll(self, timeout):
        return self._epoll.poll(timeout)

    def add_fd(self, fd, mode):
        self._epoll.register(fd, mode)

    def remove_fd(self, fd):
        self._epoll.unregister(fd)

    def modify_fd(self, fd, mode):
        self._epoll.modify(fd, mode)

class Server(object):
    def __init__(self, listen_addr, listen_port):
        addrs = socket.getaddrinfo(listen_addr, listen_port, 0,
                                    socket.SOCK_STREAM, socket.SOL_TCP)
        if len(addrs) == 0:
            raise Exception("can't get addrinfo for %s:%d" % (listen_addr, listen_port))
        
        af, socktype, proto, canonname, sa = addrs[0]
        
        self.server_socket = socket.socket(af, socktype, proto)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(sa)
        self.server_socket.setblocking(False)
        
        self.server_socket.listen(1024)
        
        self.poll_obj = EpollLoop();
        self.poll_obj.add_fd(self.server_socket, POLL_IN | POLL_ERR)
        
        self.client = {}
        
    def fd_error(self, fd):
        print('fd', fd, 'error.')
        try:
            self.poll_obj.remove_fd(fd)
            self.client[fd].close()
            self.client.remove(fd)
        except:
            pass
        
        
    def poll_loop(self):
        while(1):
            fds = self.poll_obj.poll(1);
            for fd,event in fds:
                if event & POLL_ERR == POLL_ERR:
                    self.fd_error(fd)
                elif event & POLL_IN == POLL_IN:
                    if fd == self.server_socket.fileno():
                        conn,info = self.server_socket.accept();
                        self.server_socket.setblocking(False)
                        self.poll_obj.add_fd(conn.fileno(), POLL_IN | POLL_ERR)
                        self.client[conn.fileno()] = conn
                        print('add client', conn.fileno())
                    else:
                        print('getting client', fd)
                        sock = self.client[fd]
                        msg_size_data = sock.recv(4);
                        if(len(msg_size_data) != 4):
                            print('recv data size error.', fd, event)
                            self.fd_error(fd)
                            continue
                        msg_size = struct.unpack('I', msg_size_data)[0]
                        msg = sock.recv(msg_size)
                        if len(msg) != msg_size:
                            self.fd_error(fd)
                        else:
                            print('[recv]:', msg)
                            for fd,conn in self.client.items():
                                conn.send(msg_size_data)
                                conn.send(msg)
                else:
                    print('unknow event.', event)
                    print(EVENT_NAMES[event])
                    raise 'unknow event.'
                
                
if __name__ == '__main__':
    server = Server("0.0.0.0", 8081)
    print('start in 8081')
    server.poll_loop()
    