import zmq
import threading

context = zmq.Context()
send_socket = context.socket(zmq.PUSH)
send_socket.connect('tcp://127.0.0.1:5557')

def print_incoming_messages():
    recv_socket = context.socket(zmq.PULL)
    recv_socket.connect('tcp://127.0.0.1:5556')
    while True:
        msg = recv_socket.recv_string()
        print(f'Message from server: {msg}')

recv_thread = threading.Thread(target=print_incoming_messages)
recv_thread.start()

while True:
    msg = input('Message to send: ')
    send_socket.send_string(msg)