import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            __file__
        )
    )
)

from NaiveRPC import RPCClient


HOST = 'localhost'
PORT = 8088

client = RPCClient(HOST, PORT)

data = client.call('test_obj.print_attr', ('vincent',), dict())
print(f'result of test_obj.print_attr: {data}')

data = client.call('print_hello', ('vincent',), dict())
print(f'result of print_hello: {data}')
