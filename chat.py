import socket
import threading
import sys

connection_dict = {}
connection_counter = 0

helpmenu = """""
Command Manual: \n

myip - Display the IP address of this process \n
myport - Display the port on which this process is listening for connections \n
connect <destination> <port no> - Establish a new TCP connection to the specified destination \n
								  at the specified port number. \n
list - Display a numbered list of all the connections this process is part of. \n
terminate <connection id> - Terminate the connection listed under the specified connection id. \n
send <connection id> <message> - Send the message to the host on the connection specified by \n
								 the connection id. \n
exit - Close all connections and terminate this process. \n

"""""

# def myip():
# 	localhost = socket.gethostname()
# 	print("Host's IPv4 address is ", socket.gethostbyname(localhost))
# 	return socket.gethostbyname(localhost)

def connect(ip, port):
	print("Opened connection")
	s = socket.socket()  # next create a socket object
	s.connect((ip, port))  # connect to the server on local computer
	global connection_counter
	connection_dict[connection_counter] = s
	connection_counter += 1
	# keep getting user input


def send_message(connection_socket, message):
	s = connection_socket

	# encode the message to bytes and send using the socket
	s.send(message.encode())

	# print replies from server
	data = s.recv(1024)
	print(data.decode())
	
	# if message == "close":
	# 	print("Closing connection from client side")
	# 	s.close()
	return

def handle_connection(connection_socket, address):
	"""
	actions for each connection
	"""
	while True:
		# receive data in bytes
		data = connection_socket.recv(1024)

		# decode the received data to string and print out
		message = data.decode()

		# stop checking messages and break
		if message == "close":
			break

		# else print the message received
		print("Got message from", address, ":", message)

		# convert it to uppercase and send back
		connection_socket.send(message.upper().encode())

	print("Closing connection from server side with", address)

	connection_socket.close()

def terminate_connection(connection_id):
	conn = connection_dict[connection_id]
	send_message(conn, "close")
	del connection_dict[connection_id]
	global connection_counter
	connection_counter -= 1
	print("Terminated connection", connection_id)
	return

def input_handler(sock):
	command = input("Input command: ")

	if type(command) != str:
		print("Invalid input, please enter a string")
		return

	if command == "help":
		print(helpmenu)
		return

	elif command == "myip":
		hostname = socket.gethostname()
		hostip = socket.gethostbyname(hostname)
		print("The IPv4 address of this process is ", hostip)
		return(hostip)
	
	elif command == "list":
		print("Current connections: ")
		if len(connection_dict) == 0:
			print("No current connections")
		for conn_id in connection_dict.keys():
			conn = connection_dict[conn_id]
			print("Connection ID:", conn_id, " | IP Address:", conn.getsockname()[0], " | Port:", conn.getsockname()[1])
			# print("Connection ID:", conn_id, " | Address:", conn.getpeername())

	elif command == "myport":
		portnum = sock.getsockname()[1]
		print("The listening socket of this process is ", portnum)
		return(portnum)
	
	elif command[0:7] == "connect":	
		# split input to get <destination> and <port> arguments
		args = command.split()

		# input validation
		if (len(args) < 3):
			print("Invalid arguments: Must provide IP address and port number.")
			return
		ip = args[1]
		port = int(args[2])

		# validate inputted port number
		if port < 1024 or port > 65535:
			print("Invalid port number, please enter a number between 1024 and 65535")
			return
		elif port == sock.getsockname()[1]:
			print("Cannot connect to self")
			return
		connect(ip, port)

	elif command[0:4] == "send":
		# split input to get <connection id> and <message> arguments
		args = command.split()

		# input validation
		if (len(args) < 3): 
			print("Invalid arguments: Must provide connection id and message.")
			return
		
		connection_id = int(args[1])
		message = " ".join(args[2:])

		# connection_id = input("Enter connection ID: ")
		# message = input("Enter message: ")

		conn = connection_dict[int(connection_id)]
		if conn.getsockname()[0] == socket.gethostbyname(socket.gethostname()) and conn.getsockname()[1] == sock.getsockname()[1]:
			print("Cannot send message to self")
			return

		send_message(conn, message)
		return
	
	elif command[0:9] == "terminate":
		# split input to get <connection id> argument
		args = command.split()
		connection_id = int(args[1])

		# connection_id = input("Enter connection ID: ")
		if connection_id not in connection_dict.keys():
			print("Invalid connection ID, please try again")
			return
		
		terminate_connection(connection_id)
		return
		
	elif command == "exit":
		
		exit

	else:
		print("Invalid command, please try again")
		return
	return

def input_loop(sock):
	while True:
		# print("There are currently", threading.active_count(), " active threads")	
		# print(threading.enumerate())
		input_handler(sock)
	
# def listen_loop(sock):
# 	i = 0
# 	while i <3: 
# 		# accept connection request
# 		print("Waiting for connection...", end="\n")
# 		connection_socket, address = sock.accept()
# 		print("Got connection from", address, end="\n")
# 		# create a thread to handle the accepted client
# 		thread = threading.Thread(target=handle_connection, args=(connection_socket, address), daemon=True)
# 		thread.start()  # start the thread
# 		print("Started new connection thread", thread.name)
# 		print("There are currently", threading.active_count(), " active threads")
# 		i+=1

def main():
	# input validation
	if int(sys.argv[1]) not in range(1023,49152):
		raise ValueError("Invalid port number, please enter a number between 0 and 12345")

	# create a listening socket
	port = int(sys.argv[1])
	s = socket.socket()
	s.bind(("", port))  # input is a tuple with address and port as elements
	print("Hello. Created new process with listening port", port)



	# listen_thread = threading.Thread(target=listen_loop, name="listen_loop_thread", args=(s,), daemon=True)
	# listen_thread.start()  # start the thread
	# print("Started thread", listen_thread.name)
	# print("There are currently", threading.active_count(), " active threads")
	

	input_thread = threading.Thread(target=input_loop, name="input_handler_thread", args=(s,), daemon=True)
	input_thread.start()  # start the thread
	print("Started thread", input_thread.name)
	

	s.listen(50)

	while True:
		# accept connection request
		connection_socket, address = s.accept()

		global connection_counter
		connection_dict[connection_counter] = connection_socket
		connection_counter += 1
		print("Got connection from", address)

		# create a thread to handle the accepted client
		thread = threading.Thread(target=handle_connection, args=(connection_socket, address), daemon=True)
		thread.start()  # start the thread


if __name__ == "__main__":
	main()