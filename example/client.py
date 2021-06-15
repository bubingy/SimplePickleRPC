import pickle
import socket
from typing import Any

class Client:
    def __init__(self, host, port) -> None:
        self.host, self.port = host, port
        self.conn = socket.socket()
        self.conn.connect((self.host, self.port))

    def send(self, data: Any) -> None:
        message = b''
        try:
            body = pickle.dumps(data)
        except Exception as e:
            print(f'fail to dump message: {e}')
            return
        body_size = len(body)
        message += body_size.to_bytes(8, 'big')
        message += body
        self.conn.send(message)

    def receive(self) -> bytes:
        data = b''
        try:
            body_size = int.from_bytes(self.conn.recv(8), 'big')
        except Exception as e:
            print(e)
            return None
        while body_size > 0:
            buffer_size = min(4096, body_size)
            buffer = self.conn.recv(buffer_size)
            data += buffer
            body_size -= buffer_size
        return data

    def remote_call(self,
                    function_name: str,
                    function_args: tuple=tuple(),
                    function_kwargs: dict=dict()):
        call_request = {
            'function_name': function_name,
            'function_args': function_args,
            'function_kwargs': function_kwargs
        }
        self.send(call_request)
        result = self.receive()
        print(pickle.loads(result))

host = '10.20.10.78'
port = 8088

client = Client(host, port)
client.remote_call('print_hello', ('Vincent',))
