import socket
import threading
import sys

helpmenu = """""
Options for 
"""""

def help():
    print("Options for printing:")
    return


def myip():
    localhost = socket.gethostname()
    print("Host's IPv4 address is ", socket.gethostbyname(localhost))

# port = 1234
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# def setup_server(port_num):
#     s = socket.socket()  # next create a socket object      
#     s.bind(('', port_num))  # bind to the listening port
#     print("bound to port", port_num)

#     def capitalize_message(input_str):
#         return input_str.upper()

#     # # keep listening
#     s.listen(1)  # maximum pending connections is 5 
#     print("listening done")
    
#     connection_socket, address = s.accept()  # establish connection socket
#     print("cs and address are", connection_socket, "and ", address)
#     thread = threading.Thread(target=capitalize_message, 
#                             args=(connection_socket, address),
#                             daemon=True)
#     print("made it to thread")
#     connection_socket.send('Thank you for connecting'.encode()) 
#     connection_socket.close()  # close connection


# def connect(dest, port):
#     setup_server(num)
#     print("a")
#     s = socket.socket()
#     print("b")
#     # connect to the server on local computer 
#     s.connect((dest, port)) 
#     print("c")
#     while True:
#         message = input(">")
#         s.send(message.encode())
#         # receive data from the server and decoding to get the string.
#         # print (s.recv(1024).decode())
#         break
#     # close the connection 
#     s.close()


#socket1 = setup_server(portnumber)
#print("Listening socket's number is", socket1.getsockname()[1])

userinput = ""
def getuserinput():
    # get user command
    userinput = input("Input command: ")
    
    # check input 
    if userinput == "help":
        help()

    if userinput == "myip":
        myip()

    if userinput == "myport":
        print(myip().getsockname()[1])

    if userinput == "connect":
        ip = input("Enter IP address: ")
        port = int(input("Enter port number: "))
        connect(ip, port)
        # connect("172.28.224.11")

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

def main():
    # create a listening socket
    port = int(sys.argv[1])
    print("port is", port, type(port))

    s = socket.socket()
    s.bind(("", port))  # input is a tuple with address and port as elements
    print("hello")
    

    s.listen(50)

    i = 0
    while i <3: 
        getuserinput()
        # accept connection request
        print("do we hit this line")
        connection_socket, address = s.accept()
        print("Got connection from", address)
        # create a thread to handle the accepted client
        thread = threading.Thread(target=handle_connection, args=(connection_socket, address), daemon=True)
        thread.start()  # start the thread



# # keep listening
# s.listen(5)  # maximum pending connections is 5 
# while True: 
#   connection_socket, address = s.accept()  # establish connection socket
#   thread = threading.Thread(target=capitalize_message, 
#                             args=(connection_socket, address),
#                             daemon=True)
#   connection_socket.send('Thank you for connecting'.encode()) 
#   connection_socket.close()  # close connection
#   break


if __name__ == "__main__":
    main()