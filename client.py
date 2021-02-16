import socket
import threading

#enter your local wifi public ip and port
host = '127.0.0.1' #local host
port = 9999 #port

name = input("Enter your name to start the chat : ")

#creating a connection with server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.11',9999))

#creating a function to recieve the messages
def recieve_messages():
    while True:
        try:
            #recieving the message from the server
            message = client.recv(1024).decode('ascii')

            # if name then send name
            if message == "Name":
                client.send(name.encode('ascii'))

            #else sending custom messages to server
            else:
                print(message)
        #if any problem occurred then close the connection break the loop and it will stop
        except:
            print("Some error occurred !")
            client.close()
            break

def send_messages():
    while True:
        message = f'{name}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve_messages)
recieve_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
