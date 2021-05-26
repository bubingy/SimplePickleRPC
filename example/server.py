import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            __file__
        )
    )
)

from NaiveRPC import *


class Test:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def print_attr(self, message):
        time.sleep(5)
        return f'{message}: {self.x}, {self.y}'


def print_hello(name: str):
    time.sleep(5)
    return f'hello {name}!'


server = RPCServer('localhost', 8088)
server.register_function(print_hello)
test_obj = Test(4, 6)
server.register_instance(test_obj)

server.run_forever()