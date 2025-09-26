import socket
import threading
import sys

helpmenu = """""
Options for 
"""""

def help():
	print("Options for printing:")
	return None

def myip():
	localhost = socket.gethostname()
	print("Host's IPv4 address is ", socket.gethostbyname(localhost))
	return socket.gethostbyname(localhost)

# def getuserinput():
# 	# get user command
# 	print("Running getuserinput")
# 	userinput = input("Input command: ")

# 	if type(userinput) != str:
# 		print("Invalid input, please enter a string")
# 		return
	
# 	# check input 
# 	if userinput == "help":
# 		help()

# 	if userinput == "myip":
# 		myip()

# 	if userinput == "myport":
# 		print("my ip is ", myip(), "of type", type(myip()))
# 		print("and the socket is ", socket.getsockname())
# 		print(myip().getsockname()[1])

# 	if userinput == "connect":
# 		ip = input("Enter IP address: ")
# 		port = int(input("Enter port number: "))
# 		if port < 1024 or port > 65535:
# 			print("Invalid port number, please enter a number between 1024 and 65535")
# 			return
# 		elif port == myip().getsockname()[1]:
# 			print("Cannot connect to self")
# 			return
# 		connect(ip, port)
# 		# connect("172.28.224.11")
# 	return

def connect(ip, port):
	print("Opened connection")
	s = socket.socket()  # next create a socket object
	s.connect((ip, port))  # connect to the server on local computer
	# keep getting user input
	while True:
		message = input(">")

		# encode the message to bytes and send using the socket
		s.send(message.encode())

		# print replies from server
		data = s.recv(1024)
		print(data.decode())
		
		if message == "close":
			print("Closing connection from client side")
			break

	s.close()


def handle_connection(connection_socket, address):
	"""
	actions for each connection
	"""
	while True:
		# receive data in bytes
		data = connection_socket.recv(1024)

		# decode the received data to string and print out
		message = data.decode()
		print("Got message from", address, ":", message)

		# convert it to uppercase and send back
		connection_socket.send(message.upper().encode())

		# stop checking messages and break
		if message == "close":
			break
			
	print("Closing connection from server side with", address)
	connection_socket.close()


# def handle_connection(connection_socket, address):
#     while True:
#         # receive data 
#         data = connection_socket.recv(1024)
#         message = data.decode()
#         print("Got message from", address, ":", message)

#         # convert it to uppercase
#         connection_socket.send(message.upper().encode())

#         # close if needed
#         if message == "close":
#             print("Closing connection with", address)
#             break
#         connection_socket.close()


def input_handler(sock):
	command = input("Input command: ")

	if type(command) != str:
		print("Invalid input, please enter a string")
		return

	if command == "help":
		print("Options for printing:")

	elif command == "myip":
		hostname = socket.gethostname()
		hostip = socket.gethostbyname(hostname)
		print("The IPv4 address of this process is ", hostip)
		return hostip
	
	elif command == "myport":
		portnum = sock.getsockname()[1]
		print("The listening socket of this process is ", portnum)
		return(portnum)
	
	elif command == "connect":	
		ip = input("Enter IP address: ")
		port = int(input("Enter port number: "))
		if port < 1024 or port > 65535:
			print("Invalid port number, please enter a number between 1024 and 65535")
			return
		elif port == sock.getsockname()[1]:
			print("Cannot connect to self")
			return
		connect(ip, port)
	return

def main():
	# create a listening socket
	port = int(sys.argv[1])
	s = socket.socket()
	s.bind(("", port))  # input is a tuple with address and port as elements
	print("Hello. Created new process with listening port", port)	

	s.listen(50)

	i = 0
	while i <3: 
		# getuserinput()
		print("looping", i)
		input_handler(s)
		# accept connection request
		print("Waiting for connection...")
		connection_socket, address = s.accept()
		print("Got connection from", address)
		# create a thread to handle the accepted client
		thread = threading.Thread(target=handle_connection, args=(connection_socket, address), daemon=True)
		thread.start()  # start the thread
		print("started thread", thread.name)


if __name__ == "__main__":
	main()