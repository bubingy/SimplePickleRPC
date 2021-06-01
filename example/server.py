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


class Test:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def print_attr(self, message):
        return f'{message}: {self.x}, {self.y}'


def print_hello(name: str):
    return f'hello {name}!'


server = RPCServer('0.0.0.0', 9999)
server.register_function(print_hello)
test_obj = Test(4, 6)
server.register_instance(test_obj)

server.run_forever()