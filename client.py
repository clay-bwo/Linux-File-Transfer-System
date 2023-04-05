import socket
import rsa

HOST = '127.0.0.1' # The server's IP address
PORT = 65432 # The port used by the server

# Generate set of keys
client_public_key, private_key = rsa.newkeys(512)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Send client's public key to server
    s.sendall(client_public_key.save_pkcs1())

    while True:
        # Get file path from user
        file_path = input('Enter file path (or "exit" to quit): ')
        if file_path == 'exit':
            break

        # Send inputted file path to server
        s.sendall(file_path.encode())

        # Receive encrypted file data from server
        encrypted_file_data = s.recv(1024)

        # Check for error message
        if encrypted_file_data.startswith(b'Error'):
            print(encrypted_file_data.decode())
        else:
            # Decrypt file data using private key
            file_data = rsa.decrypt(encrypted_file_data, private_key)

        # Get file name from file path
        file_name = file_path.split('/')[-1]

        # Write the decrypted file data to a new file
        with open("received_file.txt", 'wb') as file:
            file.write(file_data)

        print(f'Received file: {file_name} from server')

    # Close the client socket
    s.close()
