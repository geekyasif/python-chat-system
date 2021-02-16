import socket
import threading

host = '192.168.1.11' #localhost
port = 9999       # port

#iniatilizing the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creating a server with host and port
server.bind((host,port))

#server is ready to connect with clients
server.listen()

clients = []
names = []

#creating a function to broadcast the message to all client
def broadcast(message):

    #sending message to all the clients
    for client in clients:
        client.send(message)


#creating a function to handle the clients
def handle_client(client):
    while True:
        try:
            #trying to receive a message and broadcast to all the client
            message = client.recv(1024)
            broadcast(message)
        except:
            # if client will not connect for some reason then we close the connection remove the client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left the chat !'.encode('ascii'))
            names.remove(name)
            break

def recieve():
    while True:
        #accepting the client request
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        #asking the client to enter the name
        client.send("Name".encode('ascii'))
        #revcieving the name and storing into the names list
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        print(f"Name of the client is {name}")

        #sending the message to all the client
        broadcast(f"{name} joined the chat !".encode('ascii'))

        #sending the message to client for successfull connected
        client.send('Successfully connected to the server.'.encode('ascii'))

        #using multithreading to handle all the function to run at same time
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



if __name__ == '__main__':
    print("Server is listening....")
    recieve()



