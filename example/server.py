import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            __file__
        )
    )
)

from PickleRPC import *

class MyServerStreamHandler(BaseServerStreamHandler):
    def __init__(self) -> None:
        super().__init__()
        
        self._registered_functions = dict()
        self._registered_instances = dict()

    async def client_connected_cb(self,
                                  reader: StreamReader,
                                  writer: StreamWriter) -> Any:
        addr = writer.get_extra_info('peername')
        message = pickle.loads(await self.receive(reader))
        function_name = message['function_name']
        function_args = message['function_args']
        function_kwargs = message['function_kwargs']
        result = self.call(function_name, function_args, function_kwargs)
        print(f'get rpc request from {addr}, get result: {result}')
        if result is not None: self.send(writer, result)


handler = MyServerStreamHandler()

def print_hello(name: str):
    return f'hello {name}!'


server = RPCServer(handler)
handler.register_function(print_hello)
server.serve_forever('0.0.0.0', 8088)