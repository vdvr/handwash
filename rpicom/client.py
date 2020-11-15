import zmq
import threading

context = zmq.Context()

def print_incoming_messages():
    recv_socket = context.socket(zmq.PULL)
    recv_socket.connect('tcp://127.0.0.1:5557')
    while True:
        msg = recv_socket.recv()
        print(f'Message from server: {msg}')

recv_thread = threading.Thread(target=print_incoming_messages)
recv_thread.start()
