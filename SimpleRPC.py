import sys
import time
import pickle
import socket
from typing import Any, Callable


##############################
#          Handler           #
##############################
'''
A message should be in following format:
PART 1. Size of body
The size of this part is fixed: 8 bytes.
It indicates the size of the entity-body.

PART 2. Body
Body can be converted to a json format object(to be determined).
It contains following keys:  
* function_name - name of function
* function_args - args for function
* function_kwargs - kwargs for function
'''
class BaseStreamHandler:
    def __init__(self) -> None:
        pass

    @classmethod
    def send(self, conn: socket.socket, data: Any) -> None:
        '''Send data to socket connection.
        
        :param conn: a socket session.
        :param return_value: content to send.
        '''
        message = b''
        body = pickle.dumps(data)
        body_size = len(body)
        message += body_size.to_bytes(8, 'big')
        message += body
        conn.sendall(message)

    @classmethod
    def receive(self, conn: socket.socket) -> bytes:
        '''Receive data from socket connection.
        
        :param conn: a socket session.
        :return: retrieved bytes.
        '''
        data = b''
        body_size = int.from_bytes(conn.recv(8), 'big')
        while body_size > 0:
            buffer_size = min(4096, body_size)
            buffer = conn.recv(buffer_size)
            if not buffer: break
            data += buffer
            body_size -= buffer_size
        return pickle.loads(data)

    @classmethod
    def handle_stream(self) -> None:
        '''To override.

        '''
        pass


class ClientHandler(BaseStreamHandler):
    '''Default stream handler for client.

    '''
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def handle_stream(self,
                      conn: socket.socket,
                      function_name: str,
                      function_args: tuple=None,
                      function_kwargs: dict=None) -> Any:
        rpc_request = {
            'function_name': function_name,
            'function_args': function_args,
            'function_kwargs': function_kwargs
        }
        self.send(conn, rpc_request)
        while True:
            try:
                data = pickle.loads(self.receive(conn))
                return data
            except Exception:
                time.sleep(1)


class ServerHandler(BaseStreamHandler):
    '''Default stream handler for server.
    
    '''
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def handle_stream(self,
                      conn: socket.socket,
                      registered_functions: dict,
                      registered_instances: dict) -> None:
        rpc_request = self.receive(conn)

        function_name = rpc_request['function_name']
        function_args = rpc_request['function_args']
        function_kwargs = rpc_request['function_kwargs']

        if '.' in function_name:
            function_call_path = function_name.split('.')
            assert len(function_call_path) == 2

            instance_name = function_call_path[0]
            function_name = function_call_path[1]
            instance_module = sys.modules[registered_instances[instance_name]]
            method_to_call = getattr(
                instance_module.__getattribute__(instance_name),
                function_name
            )
            returned_value = method_to_call(
                *function_args,
                **function_kwargs
            )
        else:
            method_to_call = getattr(
                sys.modules[registered_functions[function_name]], 
                function_name
            )
            returned_value = method_to_call(
                *function_args,
                **function_kwargs
            )

        if returned_value is None: return
        self.send(conn, returned_value)


##############################
#           Server           #
##############################
class RPCServer:
    '''A TCP Server.

    '''
    def __init__(self, host: str, port: int) -> None:
        assert isinstance(port, int) and port > 0
        self.__s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.__s.bind((host, port))
        self.__stream_handler = ServerHandler()
        self.__functions = dict()
        self.__instances = dict()

    def set_handler(self, handler) -> None:
        '''Set stream handler.

        :param handler: stream handler.
        '''
        self.__stream_handler = handler

    def register_function(self, fun: Callable) -> None:
        '''Register a function for calling.

        :param fun: a callable object.
        '''
        if fun.__name__ in self.__functions.keys():
            raise 'function already registered.'
        self.__functions[fun.__name__] = fun.__module__

    def register_instance(self, instance: object) -> None:
        '''Register a class instance for calling.

        :param instance: a class instance.
        '''
        instance_name = get_object_name(instance.__module__, instance)
        if instance_name in self.__instances.keys():
            raise 'instance already registered.'
        self.__instances[instance_name] = instance.__module__

    def run_forever(self) -> None:
        '''Listen port and accept connection.

        '''
        self.__s.listen(1)
        print('start listening...')
        while True:
            self.__conn, _ = self.__s.accept()

            self.__stream_handler.handle_stream(
                self.__conn,
                self.__functions,
                self.__instances
            )


##############################
#           Client           #
##############################
class RPCClient:
    def __init__(self, host: str, port: int) -> None:
        assert isinstance(port, int) and port > 0
        self.__s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.__s.connect((host, port))
        self.__stream_handler = ClientHandler()

    def call(self,
             function_name: str,
             function_args: tuple=tuple(),
             function_kwargs: dict=dict()) -> Any:
        return self.__stream_handler.handle_stream(
            self.__s,
            function_name,
            function_args,
            function_kwargs
        )

##############################
#           Utils            #
##############################
def get_object_name(module_name: str, object: Any) -> str:
    '''Get name of given object.

    :param module_name: name of module where the object is defined.
    :param object: the object.
    :return: name of given object.
    '''
    object_id = id(object)
    for obj_name in dir(sys.modules[module_name]):
        if id(sys.modules[module_name].__getattribute__(obj_name)) == object_id:
            return obj_name
    return None