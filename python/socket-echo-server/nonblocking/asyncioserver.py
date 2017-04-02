import asyncio


class EchoServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

        client_addr, client_port = self.transport.get_extra_info('peername')
        print('New client `%s:%d` is connected' % (client_addr, client_port))

    def data_received(self, data):
        client_addr, client_port = self.transport.get_extra_info('peername')
        print('[%s:%d] > %s' % (client_addr, client_port, data))

        self.transport.write(data)
        print('[%s:%d] < %s' % (client_addr, client_port, data))

    def connection_lost(self, exc):
        client_addr, client_port = self.transport.get_extra_info('peername')
        self.transport.close()
        print('Client `%s:%d` is disconnected' % (client_addr, client_port))


def main():
    host = 'localhost'
    port = 37564

    # create event loop
    ev_loop = asyncio.get_event_loop()

    # create a server
    factory = ev_loop.create_server(EchoServer, host, port)

    # launch the server
    server = ev_loop.run_until_complete(factory)

    try:
        # launch the event loop
        ev_loop.run_forever()
    finally:
        server.close()
        ev_loop.run_until_complete(server.wait_closed())
        ev_loop.close()


if __name__ == '__main__':
    main()
