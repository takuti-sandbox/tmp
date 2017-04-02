import time
import socket
import threading


def worker_thread(server_socket):
    while True:
        # block until client is connected
        # worker threads try to get the client's connection
        client_socket, (client_addr, client_port) = server_socket.accept()
        print('New client `%s:%d` is connected' % (client_addr, client_port))

        while True:
            # continuously receive 1024-byte chunks
            try:
                msg = client_socket.recv(1024)
                print('[%s:%d] > %s' % (client_addr, client_port, msg))
            except OSError:
                break

            # end of chunk series
            if len(msg) == 0:
                break

            sent_msg = msg
            while True:
                # echo the received message to the client
                sent_len = client_socket.send(sent_msg)

                # check if the entire message has been sent
                if sent_len == len(sent_msg):
                    break

                # resend remaining message
                sent_msg = msg[sent_len:]
            print('[%s:%d] < %s' % (client_addr, client_port, msg))

        client_socket.close()
        print('Client `%s:%d` is disconnected' % (client_addr, client_port))


def main():
    # create IPv4 TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = 'localhost'
    port = 37564
    server_socket.bind((host, port))

    server_socket.listen(128)  # queue 128 clients

    # number of worker threads in a thread pool
    NUM_THREAD = 10
    for _ in range(NUM_THREAD):
        # create a worker thread which wait new client connection
        thread = threading.Thread(target=worker_thread, args=(server_socket,))
        thread.daemon = True
        thread.start()

    while True:
        # main thread just sleeps
        time.sleep(1)


if __name__ == '__main__':
    main()
