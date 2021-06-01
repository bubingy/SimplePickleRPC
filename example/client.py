import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            __file__
        )
    )
)

from SimpleRPC import RPCClient


HOST = '127.0.0.1'
PORT = 8088

client = RPCClient(HOST, PORT)

data = client.call('test_obj.print_attr', ('vincent',))
print(f'result of test_obj.print_attr: {data}')

data = client.call('print_hello', ('vincent',))
print(f'result of print_hello: {data}')
