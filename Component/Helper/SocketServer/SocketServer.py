import socket                   # Import socket module
port = 63342                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()             # Create a socket object
host = socket.gethostbyname(socket.gethostname()) #"127.0.0.1"   # Get local machine name
print(host)
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from ', addr)
    data=conn.recv(1024)
    print('receiving data...')
    print('type of data: ', data)

print('Successfully get the file')
print('connection closed')

# def listen_port():
#
# def receive():