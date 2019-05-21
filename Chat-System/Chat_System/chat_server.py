"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
GAME = [[1,2,3],[4,5,6],[7,8,9]]

class Server:
    def __init__(self):
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        # sonnet
        # self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        # self.sonnet = pkl.load(self.sonnet_f)
        # self.sonnet_f.close()
        self.sonnet = indexer.PIndex("AllSonnets.txt")
    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def check(self,graph):
        if graph[0][0] == graph[0][1] == graph[0][2]:
            return 1
        elif graph[1][0] == graph[1][1] == graph[1][2]:
            return 1
        elif graph[2][0] == graph[2][1] == graph[2][2]:
            return 1
        elif graph[0][0] == graph[0][1] == graph[0][2]:
            return 1
        elif graph[1][0] == graph[1][1] == graph[1][2]:
            return 1
        elif graph[2][0] == graph[2][1] == graph[2][2]:
            return 1
        elif graph[0][0] == graph[1][1] == graph[2][2]:
            return 1
        elif graph[0][2] == graph[1][1] == graph[2][0]:
            return 1
        else:
            for i in range(3):
                for j in range(3):
                    if type(graph[i][j]) == int:
                        return 3
            return 2

    def login(self, sock):
        #read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        #move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        #add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        #load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name]=pkl.load(open(name+'.idx','rb'))
                            except IOError: #chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps({"action":"login", "status":"ok"}))
                    else: #a client under this name has already logged in
                        mysend(sock, json.dumps({"action":"login", "status":"duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print ('wrong code received')
            else: #client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
#==============================================================================
# handle connect request
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action":"connect", "status":"self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps({"action":"connect", "status":"success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"connect", "status":"request", "from":from_name}))
                else:
                    msg = json.dumps({"action":"connect", "status":"no-user"})
                mysend(from_sock, msg)
# ==============================================================================
# handle game request
# ==============================================================================
            elif msg["action"] == "game_request":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action": "game_request", "status": "self"})
                # play game with the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    status = self.group.game(from_name, to_name)
                    if status == 'success':
                        msg = json.dumps({"action": "game_request", "status": status, "from": from_name,"game_grf":GAME,"order":"Wait for another player","color":'H'})
                        mysend(to_sock, json.dumps({"action": "game_request", "status": status, "from": from_name,"game_grf":GAME,"order":"Now its your turn","color":'M'}))
                    else:
                        msg = json.dumps({"action":"game_request","status":status,"from":from_name})

                else:
                    msg = json.dumps({"action": "connect", "status": "no-user"})
                mysend(from_sock, msg)

#==============================================================================
# handle game process
#==============================================================================
            elif msg["action"] == "game_exchange":
                from_name = self.logged_sock2name[from_sock]
                finish = self.check(msg["game_grf"]) #1 win 2 tie 3 not finish
                #said = msg["from"]+msg["message"]
                the_guys = self.group.list_me(from_name)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    if finish == 1:
                        msg_to = json.dumps({"action":"game_exchange","game_grf":msg["game_grf"],"message":"Sorry, you lose\n","status":'finish'})
                        mysend(to_sock, msg_to)
                        msg_from = json.dumps({"action":"game_exchange","game_grf":msg["game_grf"],"message":"Congratulation! You win!\n","status":'finish'})
                        mysend(from_sock,msg_from)
                    elif finish == 2:
                        msg_to = json.dumps({"action": "game_exchange", "game_grf": msg["game_grf"], "message": "Tied\n","status": 'finish'})
                        mysend(to_sock, msg_to)
                        msg_from = json.dumps({"action": "game_exchange", "game_grf": msg["game_grf"],"message": "Tied\n", "status": 'finish'})
                        mysend(from_sock, msg_from)
                    else :
                        msg_to = json.dumps({"action": "game_exchange", "game_grf": msg["game_grf"], "message": "Now its your turn\n","status": 'continue'})
                        mysend(to_sock, msg_to)
                        msg_from = json.dumps({"action": "game_exchange", "game_grf": msg["game_grf"], "message": "Wait for another player\n","status": 'continue'})
                        mysend(from_sock, msg_from)

                    # ---- end of your code --- #

#==============================================================================
# handle messeage exchange: one peer for now. will need multicast later
#==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                #said = msg["from"]+msg["message"]
                said = text_proc(msg["message"], from_name)
                self.indices[from_name].add_msg_and_index(said)
                the_guys = self.group.list_me(from_name)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    # IMPLEMENTATION
                    # ---- start your code ---- #

                    msg_send = json.dumps({"action":"exchange","from":from_name,"message":msg["message"]})
                    mysend(to_sock, msg_send)

                    # ---- end of your code --- #
#==============================================================================
#                 listing available peers
#==============================================================================
            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                # IMPLEMENTATION
                # ---- start your code ---- #

                msg = self.group.list_all(from_name)

                # ---- end of your code --- #
                mysend(from_sock, json.dumps({"action":"list", "results":msg}))
#==============================================================================
#             retrieve a sonnet
#==============================================================================
            elif msg["action"] == "poem":
                # IMPLEMENTATION
                # ---- start your code ---- #
                target = msg["target"]
                poem = ''
                for l in self.sonnet.get_poem(int(target)):
                    poem += l
                print('here:\n', poem)

                # ---- end of your code --- #
                mysend(from_sock, json.dumps({"action":"poem", "results":poem}))
#==============================================================================
#                 time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))
#==============================================================================
#                 search
#==============================================================================
            elif msg["action"] == "search":
                # IMPLEMENTATION
                # ---- start your code ---- #

                term = msg["target"]
                search_rslt = ''
                for p in list(self.group.members.keys()):
                    for m in self.indices[p].msgs:
                        if term in m:
                            search_rslt += m + '\n'
                print('server side search:\n' + search_rslt)

                # ---- end of your code --- #
                mysend(from_sock, json.dumps({"action":"search", "results":search_rslt}))
#==============================================================================
#  leave the game
#==============================================================================
            elif msg["action"] == "leave_game":
                from_name = self.logged_sock2name[from_sock]
                peer = msg["peer"]
                self.group.disconnect(from_name)
                to_sock = self.logged_name2sock[peer]
                mysend(to_sock, json.dumps({"action":"leave_game"}))
#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action":"disconnect"}))

#==============================================================================
#                 the "from" guy really, really has had enough
#==============================================================================


        else:
            #client died unexpectedly
            self.logout(from_sock)

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)

def main():
    server=Server()
    server.run()

main()
