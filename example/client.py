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


HOST = '10.20.10.158'
PORT = 9999

client = RPCClient(HOST, PORT)

data = client.call('test_obj.print_attr', ('vincent',))
print(f'result of test_obj.print_attr: {data}')

data = client.call('print_hello', ('vincent',))
print(f'result of print_hello: {data}')
