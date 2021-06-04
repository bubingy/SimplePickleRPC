import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            __file__
        )
    )
)

from SimpleRPC import *


class MyClientStreamHandler(BaseClientStreamHandler):
    async def communicate_with_server(self) -> None:
        message = {
            'function_name': 'print_hello',
            'function_args': ('vincent',),
            'function_kwargs': dict()
        }
        for _ in range(10):
            await asyncio.sleep(2)
            self.send(self.writer, message)


host = '10.20.10.78'
port = 8088

handler = MyClientStreamHandler()
client = RPCClient(handler)
client.start_communicate(host, port)
