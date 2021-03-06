import json
import socket

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print('logger ip address:', myaddr)
port = int(input('local port:'))

BUFSIZE = 1024
client = []
storehouse = ()
ip_port = (myaddr, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ip_port)
print("start listening")

while True:
    try:
        newNode = False
        data, client_addr = server.recvfrom(BUFSIZE)
        msg = json.loads(data)
        print('server received ', msg)

        if msg["head"] == 'login' and msg["password"] == "edon":
            if client_addr not in client:
                newNode = True
                client.append(client_addr)

            reply = {"head": "Success", "content": client}
            data = json.dumps(reply)
            server.sendto(data.encode(), client_addr)

        elif msg["head"] == 'storehouse' and msg["password"] == "storehouse":
            storehouse = client_addr

        else:
            msg = "invalid operation"
            data = json.dumps(msg)
            server.sendto(data.encode(), client_addr)

        # broadcast
        if newNode:
            msg = {"head": "update", "content": client_addr}
            data = json.dumps(msg)
            #server.sendto(data.encode(), client_addr)


    except Exception as e:
        pass

server.close()
