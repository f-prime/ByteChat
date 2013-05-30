import socket
import threading
import uuid
import time
import json

__version__ = 0.0.1

class ByteChat:

    nodes = {}
    id_ = ""

    def __init__(self):
        self.cmds = {
                "checkin":self.checkin,
                "msg":self.msg
                }
        self.port = 27017
        self.nick = "Max00355"
        self.room = "HF"
        self.sock = socket.socket()
        self.broker_ip = "5.44.233.7"
        self.broker_port = 5002
        self.broker = (self.broker_ip, self.broker_port)

    def main(self):
        global id_
        id_ = uuid.uuid4().hex
        self.get_nodes()
        self.send_checkin()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(5)
        while True:
            obj, conn = self.sock.accept()
            threading.Thread(target=self.handle, args=(obj,conn[0])).start()
    def get_nodes(self):
        global nodes
        global id_
        sock = socket.socket()
        try:
            sock.settimeout(2)
            sock.connect((self.broker))
            sock.send(json.dumps({"port":self.port, "id":id_}))
            data = sock.recv(102400)
            if data:
                nodes = json.loads(data)
        except Exception, error:
            print "Couldn't connect to broker, trying again"
            time.sleep(1)
            self.get_nodes()
    def send_checkin(self):
        global nodes
        global id_
        for x in nodes:
            sock = socket.socket()
            try:
                sock.settimeout(2)
                sock.connect(tuple(nodes[x]))
                sock.send(json.dumps({"cmd":"checkin", "port":self.port, "id":id_}))
                sock.close()
            except Exception, error:
                continue
    def checkin(self, data, ip):
        global nodes
        id_ = data['id']
        port = data['port']
        nodes['id'] = (ip, port)
        print id_, "checked in"

    def handle(self, obj, ip):
        data = obj.recv(1024)
        if data:
            data = json.loads(data)
            if 'cmd' in data:
                self.cmds[data['cmd']](data, ip)
    
    def prompt(self):
        while True:
            msg = raw_input(self.nick+": ")
            if msg == "":
                continue
            self.send(msg)

    def send(self, msg):
        global nodes
        global id_
        for x in nodes:
            sock = socket.socket()
            try:
                sock.settimeout(2)
                sock.connect(tuple(nodes[x]))
                sock.send(json.dumps({"cmd":"msg", "message":msg, "from":self.nick, "room":self.room, "id":id_}))
                sock.close()
            except Exception, error:
                pass
    def msg(self, data, ip):
        global id_
        try:
            if data['id'] != id_ and data['room'] == self.room:
                print data['from']+": "+data['message']
        except Exception, error:
            pass

if __name__ == "__main__":
    threading.Thread(target=ByteChat().prompt).start()
    ByteChat().main()
