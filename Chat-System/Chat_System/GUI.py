from tkinter import *

#===========================================
#登陆界面设置
#===========================================
#def login_page():
# window
'''
log_window = tk.Tk()
log_window.title("H&M Chat Room")
log_window.geometry("900x600")

# welcome image
canvas = tk.Canvas(log_window, height = 200, width = 600)
image_file = tk.PhotoImage(file = 'Welcome.png')
canvas.create_image(280, 0, anchor = 'n', image = image_file)
canvas.pack(side = 'top')

#log in part
tk.Label(log_window, text = 'User Name: ', font = ("Arial",18) ).place(x = 250, y = 300)
tk.Label(log_window, text = 'Password: ', font = ("Arial",18)).place(x = 255, y = 350)

var_usr_name = tk.StringVar()
entry_usr_nm = tk.Entry(log_window, textvariable = var_usr_name)
entry_usr_nm.place(x = 400, y = 300)

var_usr_pswd = tk.StringVar()
entry_usr_pswd = tk.Entry(log_window, textvariable = var_usr_pswd, show = '*')
entry_usr_pswd.place(x = 400, y = 350)




btn_login = tk.Button(log_window, text = 'Login', command = output)
btn_login.place(x = 310, y = 420, width = 90, height = 30)
#btn_signup = tk.Button(log_window, text = 'Sign Up', command = None)
#btn_signup.place(x = 450, y = 420, width = 90, height = 30)
'''


'''label = tk.Label(log_window, text = "Welcome to ICS Chat System", bg = "blue", font = ("Arial",18), width = 60, height = 2)
label.pack()

user_name = tk.Entry(log_window,show = None)
user_name.pack()
password = tk.Entry(log_window, show = '*')
password.pack()

def log_in():
    new_user = user_name.get()
    user_password = password.get()
    print(new_user,user_password)

log_btn = tk.Button(log_window, text = 'Log In', width = 20 , height = 2, command = log_in)
log_btn.pack()
'''

#log_window.mainloop()

#===========================================
#Chat_System 界面设置
#===========================================
'''
chat_window = tk.Tk()
chat_window.title("Chat Room")
chat_window.geometry("900x600")

fun = tk.StringVar()
label = tk.Label(chat_window, text = 'What do you want to do?', bg = "yellow", font = ("Arial",18), width = 40, height = 2)
label.pack()

def print_selection():
    label.config(text = 'Go ' + fun.get())

chat_btn = tk.Radiobutton(chat_window,text = "chat", variable = fun, value = 'Chat', command = print_selection)
chat_btn.pack()
game_btn= tk.Radiobutton(chat_window,text = "game", variable = fun, value = 'Play Game', command = print_selection)
game_btn.pack()

def enter_in():
    value = fun.get()
    print(value)

choose_btn = tk.Button(chat_window, text = 'Choose it', width = 20, height = 2, command = enter_in)
choose_btn.pack()

chat_window.mainloop()
'''
#===========================================
#Chat_System Frame 设置
#===========================================
'''main_window = tk.Tk()
main_window.title('ICS Chat Room')
main_window.geometry('900x600')

tk.Label(main_window, text = 'Welcome to H&M Chat Room', bg = "blue", font = ("Arial",18), width = 90, height = 3).pack()

frame = tk.Frame(main_window, width = 900, height = 600)
frame.pack()
frm_rt = tk.Frame(frame, bg = 'green', width = 275, height = 600)
frm_rt.pack(side = 'right')
frm_lf = tk.Frame(frame, bg = 'yellow', width = 900-275, height = 600)
frm_lf.pack(side = 'left')
'''
'''
frm_top = tk.Frame(frm_lf, bd = 10)
frm_botton = tk.Frame(frm_lf, bd = 10)
frm_top.pack(side = "top")
frm_bottom.pack(side = "bottom")
'''



#main_window.mainloop()
def input():
    global t_in
    msg = t_in.get()
    return msg

def output(msg):
    global main_window
    global t_out
    t_out.insert("end",msg)
    mainloop()
    return


main_window = Tk()
main_window.title('ICS Chat Room')
main_window.geometry('900x600')

Label(main_window, text = 'Welcome to H&M Chat Room', bg = "blue", font = ("Arial",18), width = 90, height = 3).place(x=450,y=0,anchor = 'n')


#frm_rt = Frame(main_window, width = 300, height = 530,bg = 'green')
#frm_rt.pack(side=RIGHT)
t_out = Text(main_window,width = 127, height = 26)
t_out.place(x=0, y=70, anchor='nw')

t_in = Text(main_window,width = 127, height = 9,bg = 'yellow')
t_in.place(x=0,y=600,anchor='sw')


#frm_lf = Frame(main_window, width =600, height = 530)
#frm_lf.pack(side=LEFT)
#t = Text(frm_lf,width = 90, height = 30,bg = 'yellow')
#t.pack(side=BOTTOM)

"""
frm_top = tk.Frame(frm_lf, width = 10, height = 10)
frm_top.pack(side = "top")
frm_bottom = tk.Frame(frm_lf, width=10, height=10)
frm_top.pack(side="bottom")
text = tk.Text(frm_top, height = 10, width = 10)
text.pack(side = "top")

command = tk.Text(frm_bottom, height = 10, width = 10)
command.pack(side = "bottom")
"""

mainloop()

