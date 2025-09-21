import socket
import threading

num = 33333


helpmenu = """""
Options for 
"""""

def help():
    print("Options for printing:" /n)

def myip():
    localhost = socket.gethostname()
    print("Host's IPv4 address is ", socket.gethostbyname(localhost))

# port = 1234
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setup_server(port_num):
    s = socket.socket()  # next create a socket object      
    s.bind(('', port_num))  # bind to the listening port
    print("bound to port", port_num)

    def capitalize_message(input_str):
        return input_str.upper()

    # # keep listening
    s.listen(1)  # maximum pending connections is 5 
    print("listening done")
    
    connection_socket, address = s.accept()  # establish connection socket
    print("cs and address are", connection_socket, "and ", address)
    thread = threading.Thread(target=capitalize_message, 
                            args=(connection_socket, address),
                            daemon=True)
    print("made it to thread")
    connection_socket.send('Thank you for connecting'.encode()) 
    connection_socket.close()  # close connection


def connect(dest, port):
    setup_server(num)
    print("a")
    s = socket.socket()
    print("b")
    # connect to the server on local computer 
    s.connect((dest, port)) 
    print("c")
    while True:
        message = input(">")
        s.send(message.encode())
        # receive data from the server and decoding to get the string.
        # print (s.recv(1024).decode())
        break
    # close the connection 
    s.close()


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
        print(socket1.getsockname()[1])

    if userinput == "connect":
        connect("172.28.224.11", num)

def main():
    print("hello")
    getuserinput()

if __name__ == "__main__":
    main()