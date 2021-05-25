from NaiveRPC import *


class Test:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def print_attr(self, message):
        print(f'{message}: {self.x}, {self.y}')


def print_hello(name: str):
    print(f'hello {name}!')


server = RPCServer('localhost', 8088)
server.register_function(print_hello)
test_obj = Test(4, 6)
server.register_instance(test_obj)

server.run_forever()