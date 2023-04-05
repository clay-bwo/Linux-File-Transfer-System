import socket
import os
import threading
import rsa

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

# Function to handle client requests
def handle_client(client_socket, client_addr):

    # Receive client's public key
    client_public_key = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))

    while True:
        # Receive file path from client
        file_path = client_socket.recv(1024).decode()

        if not file_path:
            break

        # Check if file exists
        if os.path.exists(file_path):
            # If so, open the file in binary mode
            with open(file_path, 'rb') as file:
                # Read the file contents
                file_data = file.read()

            # Encrypt file data using client's public key
            encrypted_file_data = rsa.encrypt(file_data, client_public_key)

            # Send encrypted file contents to the client
            client_socket.sendall(encrypted_file_data)
            print(f'Sent file: {file_path} to {client_addr}')
        else:
            # Send error message to client
            error_msg = f'Error: File not found: {file_path}'.encode()
            client_socket.sendall(error_msg)
            print(f'Error: File not found: {file_path} for {client_addr}')

    # Close the client socket
    client_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the host and port, and listen for incoming connections
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on [{HOST}]:{PORT}...')

    while True:
        # Accept a client connection
        client_socket, client_addr = s.accept()
        print(f'Connection from {client_addr}')

        # Start a new thread to handle client request
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()
