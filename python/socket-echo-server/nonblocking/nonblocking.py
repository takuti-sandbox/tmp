import socket
import select


read_waiters = {}
write_waiters = {}
connections = {}


def accept_handler(server_socket):
    """called when a server socket is readable"""

    # accept() immediately
    client_socket, (client_addr, client_port) = server_socket.accept()

    # make client socket nonblocking
    client_socket.setblocking(False)

    print('New client `%s:%d` is connected' % (client_addr, client_port))

    # key is client socket's file descriptor
    connections[client_socket.fileno()] = (client_socket, client_addr, client_port)

    # client socket waits until it will be readable
    read_waiters[client_socket.fileno()] = (recv_handler, (client_socket.fileno(),))

    # server socket waits next client's connection
    read_waiters[server_socket.fileno()] = (accept_handler, (server_socket,))


def recv_handler(client_socket_fd):
    """Called when a client socket is readable"""

    def terminate():
        """When the client is disconnected"""
        del connections[client_socket.fileno()]
        client_socket.close()
        print('Client `%s:%d` is disconnected' % (client_addr, client_port))

    client_socket, client_addr, client_port = connections[client_socket_fd]

    # continuously receive 1024-byte chunks
    try:
        msg = client_socket.recv(1024)
    except OSError:
        terminate()
        return

    # end of chunk series
    if len(msg) == 0:
        terminate()
        return

    print('[%s:%d] > %s' % (client_addr, client_port, msg))

    # wait until client socket is writable
    write_waiters[client_socket_fd] = (send_handler, (client_socket_fd, msg))


def send_handler(client_socket_fd, msg):
    """Called when a client socket is writable"""

    client_socket, client_addr, client_port = connections[client_socket_fd]

    # echo the received message to the client
    sent_len = client_socket.send(msg)
    print('[%s:%d] > %s' % (client_addr, client_port, msg[:sent_len]))

    # check if the entire message has been sent
    if sent_len == len(msg):
        # wait again until the client is readable
        read_waiters[client_socket_fd] = (recv_handler, (client_socket_fd, ))
    else:
        # wait again until being writable for the remaining message
        write_waiters[client_socket_fd] = (send_handler, (client_socket_fd, msg[sent_len:]))


def main():
    # create IPv4 TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # socket makes non-blocking mode
    server_socket.setblocking(False)

    host = 'localhost'
    port = 37564
    server_socket.bind((host, port))

    server_socket.listen(128)  # queue 128 clients

    # wait new client connection
    read_waiters[server_socket.fileno()] = (accept_handler, (server_socket,))

    while True:
        # wait until the readable/writable states has been changed
        readable_fds, writable_fds, _ = select.select(read_waiters.keys(),
                                                      write_waiters.keys(),
                                                      [],
                                                      60)

        # call the readable handlers
        for fd in readable_fds:
            handler, args = read_waiters.pop(fd)
            handler(*args)

        # call the writable handlers
        for fd in writable_fds:
            handler, args = write_waiters.pop(fd)
            handler(*args)


if __name__ == '__main__':
    main()
