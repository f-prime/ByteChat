import socket
import json
import time
import threading
import uuid

class Broker:
    def __init__(self):
        self.nodes = {}
        self.port = 5002
    def main(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", self.port))
        s.listen(1)
        while True:
            obj, conn = s.accept()
            print conn
            threading.Thread(target=self.handle, args=(obj, conn[0])).start()

    def handle(self, obj, ip):
        data = obj.recv(1024)
        print data
        if data:
            data = json.loads(data)
            print data
            port = data['port']
            addr = (ip, port)
            id = data['id']
            self.nodes[id] = addr
            obj.send(json.dumps(self.nodes))
            obj.close()
Broker().main()
