import zmq
import threading

context = zmq.Context()
send_socket = context.socket(zmq.PUSH)
send_socket.bind('tcp://*:5556')

def handler(msg_cmd, msg_args):
	if ((msg_cmd == "water") and (msg_args == "request;")):

		# Is the procedure started?
		proc_cmd = "procedure"
		proc_args = "req;state;"
		proc_msg = proc_cmd + '|' + proc_args
		send_socket.send_string(proc_msg)		

def print_incoming_messages():
    recv_socket = context.socket(zmq.PULL)
    recv_socket.bind('tcp://*:5557')
    while True:
        msg = recv_socket.recv_string()

        msg = msg.split('|')
        msg_cmd = msg[0]
        msg_args = msg[1]
        print(f'\n[server.py] cmd from worker: {msg_cmd}\n')
        print(f'\n[server.py] args from worker: {msg_args}\n')

        handler(msg_cmd, msg_args)

# Print incoming messages in background
recv_thread = threading.Thread(target=print_incoming_messages)
recv_thread.start()

