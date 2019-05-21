import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
from tkinter import *
import tkinter.messagebox

import threading
LB_COLOR = '#%02x%02x%02x' % (146,172,209)
BG_COLOR = '#%02x%02x%02x' % (188,169,162)

class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        self.Mes_thread = threading.Thread(target=self.p_msg)
        self.Msg_Output = threading.Thread(target=self.update)


    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)


    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        peer_msg = []
        if self.socket in read:
            peer_msg = self.recv()
        return peer_msg


# ===========================================
# 登陆信息传输 加重名辨别
# ===========================================
    def urs_login(self,usr):
        name = usr.get()
        msg = json.dumps({"action": "login", "name": name})
        self.send(msg)
        response = json.loads(self.recv())
#        if response["status"] == 'ok':
        self.name = name
        self.state = S_LOGGEDIN
        self.sm.set_state(S_LOGGEDIN)
        self.sm.set_myname(self.name)
        self.system_msg += 'Welcome to H&M Chat Room, ' + self.get_name() + '!'
        self.print_instructions()
#            return True
#        elif response["status"] == 'duplicate':
#           self.system_msg += 'Duplicate username, try again'#加弹窗
#            return False

# ===========================================
# 登陆界面设置
# ===========================================

    def login_page(self):
        global log_window
        log_window = Tk()
        log_window.title("H&M Chat Room")
        log_window.geometry("900x600")

        # welcome image
        canvas = Canvas(log_window, height=200, width=600)
        image_file = PhotoImage(file='Welcome.png')
        canvas.create_image(280, 0, anchor='n', image=image_file)
        canvas.pack(side='top')

        # log in part
        Label(log_window, text='Nick Name: ', font=("Arial", 18)).place(x=250, y=300)
#        Label(log_window, text='Password: ', font=("Arial", 18)).place(x=255, y=350)

        var_usr_name = StringVar()
        global entry_usr_nm
        entry_usr_nm = Entry(log_window, textvariable=var_usr_name)
        entry_usr_nm.place(x=400, y=300)


        def quit():
            global log_window
            log_window.destroy()

        def clear():
            global entry_usr_nm
            entry_usr_nm.delete(0,END)

        btn_login = Button(log_window, text='Login', command = lambda: [self.urs_login(entry_usr_nm),quit()])
        btn_login.place(x=310, y=420, width=90, height=30)
        btn_clear = Button(log_window, text='Clear', command=clear)
        btn_clear.place(x=450, y=420, width=90, height=30)
        mainloop()

    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu


    def update(self):
        global new_msg
        while True:
            if len(self.system_msg) > 0:
                new_msg = '\n' +self.system_msg
                self.system_msg = ''
            time.sleep(0.1)



    def p_msg(self):
        while self.sm.get_state() != S_OFFLINE:
            global peer_msg
            global my_msg
            peer_msg = self.get_msgs()
            my_msg = my_msg.strip()

            if len(my_msg) > 0 or len(peer_msg)>0:
                new = self.sm.proc(my_msg, peer_msg)
                self.system_msg += my_msg+ '\n' +new
                my_msg = ''
                peer_msg = []
            time.sleep(0.1)
        self.quit()

    def run_chat(self):

        self.init_chat()

        self.login_page()
        global my_msg
        my_msg = ''
        global new_msg
        new_msg = ''
        self.Mes_thread.setDaemon(True)
        self.Mes_thread.start()
        self.Msg_Output.setDaemon(True)
        self.Msg_Output.start()

        global main_window
        main_window = Tk()
        main_window.title('ICS Chat Room')
        main_window.geometry('900x600')

        Label(main_window, text='Welcome to H&M Chat Room', bg=LB_COLOR, font=("Arial", 30), width=90, height=3).place(x=420, y=0, anchor='n')

        text = Text(main_window, width=99, height=26, bg=BG_COLOR, font=("Arial", 16))
        text.place(x=0, y=98, anchor='nw')
        urs_msg = StringVar()
        t_in = Entry(main_window, textvariable=urs_msg, width=80, font=("Arial", 16))
        t_in.place(x=0, y=600, anchor='sw')


        def get_my_msg():
            global my_msg
            my_msg = t_in.get()
            t_in.delete(0, END)

        enter_btn = Button(main_window, text="Enter", command=get_my_msg)
        enter_btn.place(x=845, y=595, anchor="se")

        def update():
            global new_msg
            text.insert("end",new_msg)
            new_msg = ''
            main_window.after(100,update)


        update()

        mainloop()

