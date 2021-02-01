from socket import * 
from Tkinter import *
from functools import partial
import tkFileDialog as filedialog
import pickle
import tkMessageBox as messagebox
import os
#tkinter functions - start


def send_to_log_reg_server(sock, username, password, status_label, login_form):
    """
    send to the login/reg server the user details
    """
    global USER_PASSWORD
    global IS_ADMIN
    name = username.get()
    password_txt = password.get()
    print str('l'+name+'^'+ password_txt)
    sock.send('l'+name+'^'+ password_txt)
    data = tcpCliSock.recv(BUFSIZ)
    print data
    if data[0] == '*' or data[0] == '%':
        #move to the main server, connect to the main server
        IS_ADMIN = (data[0] == '%')
        print 'is admin: ', IS_ADMIN
        sock.close()
        USER_PASSWORD = password_txt
        main_server_sock = socket(AF_INET , SOCK_STREAM)
        main_server_sock.connect(('10.0.0.5', 50011))
        login_form.destroy()
        main_tab(main_server_sock, name)
    else:
        status_label.config(text=data)
def send_registeration_to_server(sock, username, password,status_label, register_form):
    """
    send to the login/reg server the user details
    """
    global DIRECTORY_FOLDER
    global USER_PASSWORD
    name = username.get()
    password_txt = password.get()
    print str('r'+name+'^'+ password_txt+"^^"+DIRECTORY_FOLDER)
    sock.send('r'+name+'^'+ password_txt+"^^"+DIRECTORY_FOLDER)
    data = tcpCliSock.recv(BUFSIZ)
    print data
    if data[0] == '*':
        #move to the main server, connect to the main server
        sock.close()
        USER_PASSWORD = password_txt
        main_server_sock = socket(AF_INET , SOCK_STREAM)
        main_server_sock.connect(('10.0.0.5', 50011))
        register_form.destroy()
        main_tab(main_server_sock,name )
    else:
        status_label.config(text=data)
def open_login_form(root,tcpCliSock):
    """
    create the login form
    """
    root.destroy()

    login_form = Tk()
    
    login_form.geometry("500x400+100+100")
    login_form.title("Login")
    login_form.resizable(width=FALSE, height=FALSE)
    login_form["background"]= 'blue'
    """img = PhotoImage(file="C:\Users\yuval\Desktop\School\Cyber\Final_Project\MAXIMUM media.png")
    lb1 = Label(login_form,image=img, background = 'blue')
    lb1.pack()"""

    top_label = Label(login_form, pady = 10 ,text = "--LOGIN US--", relief = "flat", font = "Helvetica 50 bold italic", background = 'blue' )
    top_label.pack(side = TOP, fill = 'x')
    input_frame = Frame(login_form, background = 'blue',padx = 10 ,pady = 10)
    status_label = Label(input_frame, pady = 10 ,text = "INSERT THE DATA", relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    
    username_label = Label(input_frame, pady = 10 ,text = "USERNAME:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    password_label = Label(input_frame, pady = 10 ,text = "PASSWORD:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    input_username = Entry(input_frame,text = "Enter Username")
    input_password = Entry(input_frame,show="*",text = "Password")
    
    login_btn = Button(input_frame, text= 'LOGIN', command = partial(send_to_log_reg_server,tcpCliSock,input_username, input_password, status_label,login_form),padx = 10 ,pady = 10)
    username_label.pack(side = TOP, fill = 'both')
    input_username.pack(side = TOP, fill = 'both')
    password_label.pack(side = TOP, fill = 'both')
    input_password.pack(side = TOP, fill = 'both')    
    status_label.pack(side = TOP)
    login_btn.pack(side = BOTTOM, fill = 'both')
    
    input_frame.pack(fill = 'both')
    login_form.mainloop()
def get_directory_folder():
    """
    get the download path of the user 
    """
    global DIRECTORY_FOLDER
    DIRECTORY_FOLDER = filedialog.askdirectory()
    print DIRECTORY_FOLDER
def open_register_form(root,tcpCliSock):
    """
    create the registeration form
    """
    global DIRECTORY_FOLDER
    root.destroy()

    register_form = Tk()
    
    register_form.geometry("500x500+100+100")
    #register_form.minsize(1200,500)
    register_form.title("Register")
    register_form.resizable(width=FALSE, height=FALSE)
    register_form["background"]= 'blue'
    top_label = Label(register_form, pady = 10 ,text = "--JOIN US--", relief = "flat", font = "Helvetica 50 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(register_form, background = 'blue',padx = 10 ,pady = 10)
    status_label = Label(input_frame, pady = 10 ,text = "", relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    username_label = Label(input_frame, pady = 10 ,text = "USERNAME:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    password_label = Label(input_frame, pady = 10 ,text = "PASSWORD:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    directory_label = Label(input_frame, pady = 10 ,text = "YOUR FOLDER:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    input_username = Entry(input_frame,text = "Enter Username")
    input_password = Entry(input_frame,show="*",text = "Password")
    direct_btn = Button(input_frame, text= 'choose directory', command = get_directory_folder ,padx = 10 ,pady = 10)
    register_btn = Button(input_frame, text= 'REGISTER', command = partial(send_registeration_to_server,tcpCliSock,input_username, input_password, status_label,register_form),padx = 10 ,pady = 10)
    
    username_label.pack(side = TOP, fill = 'both')
    input_username.pack(side = TOP, fill = 'both')
    password_label.pack(side = TOP, fill = 'both')
    input_password.pack(side = TOP, fill = 'both') 
    directory_label.pack(side = TOP, fill = 'both') 
    direct_btn.pack(side = TOP, fill = 'both')   
    status_label.pack(side = TOP)    
    register_btn.pack(side = TOP, fill = 'both')

    input_frame.pack(fill = 'both')
    register_form.mainloop()
def create_login_register_tab(tcpCliSock):
    """
    create the openning window
    """
    root = Tk()
    root.geometry("1200x500+100+100")
    root.minsize(1200,500)
    root.title("WELCOME TO DDRIVE")
    #root.resizable(width=FALSE, height=FALSE)
    root["background"]= 'blue'

    welcome_label = Label(root, pady = 10 ,text = "WELCOME TO DDrive!!!\n--LOGIN OR REGISTER US--", relief = "flat", font = "Helvetica 50 bold italic", background = 'blue' )
    welcome_label.pack(side = TOP)
    btn_frame = Frame(root, background = 'blue',padx = 10 ,pady = 100)
    login_btn = Button(btn_frame, text= 'LOGIN US', command = partial(open_login_form, root, tcpCliSock),width = 50 ,height = 70, padx = 50)
    login_btn.pack(expand="YES",side = LEFT )
    register_btn = Button(btn_frame, text= 'REGISTER TO US', command = partial(open_register_form, root, tcpCliSock),width = 50,  height = 70, padx = 50)
    register_btn.pack(expand="YES",side = RIGHT )
    
    about_label = Label(btn_frame, text = "BY DD GROUP", relief = "flat", font = "Helvetica 11 bold italic", background = 'blue' )
    about_label.pack(expand="YES", side = BOTTOM)
    btn_frame.pack( side = TOP,fill = 'both')
    root.mainloop()
def get_info_from_cloud(sock, req):
    """
    function which require from the main server data about the user
    """
    print 'send request: ', req
    sock.send('loadDataCloud^' + req)
    sock.send("done...")
    data = sock.recv(BUFSIZ)
    print 'recieved', data, eval(data)
    return eval((data))
def on_select_seg(event):
    """
    segs_list event manager
    """
    #, segs_list,files_list, segs_and_files, segs_and_premissions
    global segs_list
    global files_list
    global segs_and_files
    global segs_and_premissions
    global CURR_SEG
    global CURR_FILE
    global IS_ADMIN
    CURR_FILE = 0    
    try:
        index = segs_list.curselection()[0]
        seg_name = segs_list.get(index)
        CURR_SEG = seg_name
        print CURR_SEG
        files_list.delete(0,END)
        files_list.insert(END, "Your Premission in "+seg_name+" is: " + segs_and_premissions[seg_name])
        IS_ADMIN = segs_and_premissions[seg_name] == 'A'
        for file in segs_and_files[seg_name]:
            #str(file)
            files_list.insert(END, ('Name: '+str(file[0])+'--Type: '+str(file[1])+'--size: '+str(file[2])+" kb"))
    except:
        print CURR_SEG
def send_create_req(seg_form,sock, seg_name, password, username):
    """
    send to the main server, request to create new segment
    """
    seg_name_str = seg_name.get()
    password_str = password.get()

    sock.send('open^'+seg_name_str+"^"+username+":A^"+password_str)
    sock.send('done...')
    data = sock.recv(BUFSIZ)
    if data != "opened":
        messagebox.showwarning(title="Failed", message=data)
    seg_form.destroy()
    main_tab(sock, username)
def create_new_seg(root, sock, username):
    """
    create new segment form - all the details about it are collected here
    """
    root.destroy()

    seg_form = Tk()
    seg_form.geometry("900x400+100+100")
    seg_form.resizable(width=FALSE, height=FALSE)
    seg_form.title("CREATE SEG")
    seg_form["background"]= 'blue'

    top_label = Label(seg_form, pady = 10 ,text = "--CREATE YOUR NEW SEGMENT WITH US--", relief = "flat", font = "Helvetica 30 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(seg_form, background = 'blue',padx = 10)
    
    status_label = Label(input_frame, pady = 10 ,text = "TO CREATE:", relief = "flat", font = "Helvetica 50 bold italic", background = 'blue' )
    username_label = Label(input_frame, pady = 10 ,text = "SEG NAME:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    password_label = Label(input_frame, pady = 10 ,text = "PASSWORD:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    input_seg_name = Entry(input_frame,text = "Enter SEG NAME")
    input_password = Entry(input_frame,show="*",text = "Password")

    login_btn = Button(input_frame, text= 'CREATE', command = partial(send_create_req, seg_form,sock, input_seg_name, input_password, username), pady = 10)
    
    username_label.pack(side = TOP, fill ='both')
    input_seg_name.pack(side = TOP, fill ='both')
    password_label.pack(side = TOP, fill ='both')
    input_password.pack(side = TOP, fill ='both') 
    status_label.pack(side = TOP, fill ='both') 
    login_btn.pack(side = TOP, fill ='both') 

    input_frame.pack()
    seg_form.mainloop()
def send_file_to_seg(sock, file_path, BUFFER_SIZE, msg):
    """
    uploading the file - send all the binary data of the file while reading
    """
    try:
        f = open(file_path, 'rb')
        print 'opened file'
        print msg
        l = msg
        while (l):
            sock.send((l))
            #print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        sock.send("done...")
        f.close()
        data = sock.recv(BUFFER_SIZE)
        return data == "file uploaded"
    except:
        return False
def send_file(sock, file_path):
    """
    create the msg to server for
    uploading the file
    """
    global CURR_SEG
    req_msg = 'add^' + CURR_SEG+'^'+file_path+'^'
    return send_file_to_seg(sock, file_path, BUFSIZ, req_msg)
def add_file_to_seg(root,sock,username):
    """
    get the file path for
    uploading the file
    """
    file_path = filedialog.askopenfile().name
    print file_path
    if not send_file(sock, file_path):
        print 'failed'
        messagebox.showwarning(title="Failed", message='there was an unexcepted error')
    else:
        refresh(root,sock, username)
def on_select_file(event):
    """
    choose file handler
    """
    global CURR_FILE
    global files_list
    print CURR_SEG,",,,,,", CURR_FILE
    CURR_FILE = files_list.curselection()[0]
def download_file_from_seg(sock):
    """
    recieve from the main server the binary of the file and writes it in the user's directory
    when all the data recieved
    """
    global CURR_FILE
    global CURR_SEG
    global files_list
    global segs_and_files
    print CURR_SEG,",,,,,", CURR_FILE
    print segs_and_files[CURR_SEG]
    print segs_and_files[CURR_SEG][CURR_FILE-1]
    msg = 'download^'+CURR_SEG+"^"+ segs_and_files[CURR_SEG][CURR_FILE-1][0]
    try:
        sock.send(msg)
        sock.send("done...")
        buff = ''
        data = sock.recv(BUFSIZ)
        while not "done..." in data:
            print data,
            buff += data
            data = sock.recv(BUFSIZ)
        buff += data[:data.index('done...')]
        splited_data = buff.split('~')
        print splited_data
        file_path, file_binary  = splited_data[0] , '~'.join(splited_data[1:])
        with open(file_path, 'wb') as new_file:
            new_file.write((file_binary))
        print "-111111111111111111111----------------11111111111"
        with open(file_path,'rb') as f:
            print f.read()
        print "downloaded in", file_path
    except:
        messagebox.showwarning(title="Failed", message='there was an unexcepted error')
def download_folder_from_seg(sock):
    """
    recieve from the main server the binary of the file and writes it in the user's directory
    when all the data recieved - do it for all the files in it
    """
    global CURR_SEG
    global files_list
    global segs_and_files
    print CURR_SEG,",,,,,", CURR_FILE
    print segs_and_files[CURR_SEG]
    print segs_and_files[CURR_SEG][CURR_FILE-1]
    for file_name in segs_and_files[CURR_SEG]:
        msg = 'download^'+CURR_SEG+"^"+ file_name[0]
        try:
            sock.send(msg)
            sock.send("done...")
            buff = ''
            data = sock.recv(BUFSIZ)
            while not "done..." in data:
                print data,
                buff += data
                data = sock.recv(BUFSIZ)
            buff += data[:data.index('done...')]
            splited_data = buff.split('~')
            print splited_data
            file_path, file_binary  = splited_data[0] , '~'.join(splited_data[1:])
            with open(file_path, 'wb') as new_file:
                new_file.write((file_binary))
            print "-111111111111111111111----------------11111111111"
            with open(file_path,'rb') as f:
                print f.read()
            print "downloaded in", file_path
        except:
            messagebox.showwarning(title="Failed", message='there was an unexcepted error')
def send_file_name_req(username, new_name_form,sock, input_file_name):
    """
    sends the change_filename_req to the server
    """
    global segs_and_files
    global CURR_SEG
    global CURR_FILE

    sock.send("changeFileName^"+CURR_SEG+"^"+str(segs_and_files[CURR_SEG][CURR_FILE-1][0])+"^"+input_file_name.get())
    sock.send("done...")
    data = sock.recv(BUFSIZ)

    if data == "changed":
        segs_and_files[CURR_SEG][CURR_FILE-1] = (input_file_name.get(),segs_and_files[CURR_SEG][CURR_FILE-1][1], segs_and_files[CURR_SEG][CURR_FILE-1][2] )
        new_name_form.destroy()
        main_tab(sock, username)
    else:
        messagebox.showwarning(title="Failed", message=data)
def change_file_name(root ,sock, username):
    """
    create the change_filename_req form for sending it to the server
    """
    global segs_and_files
    global CURR_SEG
    global CURR_FILE
    root.destroy()
    
    new_name_form = Tk()
    new_name_form.geometry("700x200+100+100")

    new_name_form.resizable(width=FALSE, height=FALSE)
    new_name_form.title("SET NEW NAME")
    new_name_form["background"]= 'blue'
    top_label = Label(new_name_form, pady = 10 ,text = ("--CHOOSE THE NEW NAME OF "+str(segs_and_files[CURR_SEG][CURR_FILE-1][0])+"--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(new_name_form, background = 'blue',padx = 10 ,pady = 10)
    f_label = Label(input_frame, pady = 10 ,text = "NEW FILE NAME:", relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    input_file_name = Entry(input_frame,text = "Enter NEW NAME")
    change_btn = Button(input_frame, text= 'Change', pady = 10 ,command = partial(send_file_name_req,username, new_name_form,sock, input_file_name))
    
    f_label.pack(side = TOP, fill = 'both')
    input_file_name.pack(side = TOP, fill = 'both')
    change_btn.pack(side = TOP, fill = 'both')
    
    input_frame.pack(fill = 'both')
    new_name_form.mainloop()
def refresh(root,sock, username):
    """
    load again the root(can be also another windows)
    """
    root.destroy()
    main_tab(sock, username)
def leave_seg(sock,root,username):
    """
    sends the leave_seg_req to the main server
    """
    global segs_and_files
    global segs_and_premissions
    global CURR_SEG 

    if len(CURR_SEG) > 0:
        sock.send('exitSeg^'+CURR_SEG)
        sock.send('done...')
        data = sock.recv(BUFSIZ)
        if data == "you left":
            del segs_and_premissions[CURR_SEG]
            del segs_and_files[CURR_SEG]
            refresh(root, sock, username)
        else:
            messagebox.showwarning(title="Failed", message=data)
def join_new_seg(root, sock,username):
    """
    create the seg login form
    """
    root.destroy()
    
    join_form = Tk()
    join_form.geometry("500x500+100+100")
    join_form.resizable(width=FALSE, height=FALSE)
    join_form.title("JOIN NEW SEG")
    join_form["background"]= 'blue'

    top_label = Label(join_form, pady = 10 ,text = ("--JOIN THE NEW SEG--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(join_form, background = 'blue',padx = 10 ,pady = 10)
    
    name_label = Label(input_frame, pady = 10 ,text = "SEG NAME:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    password_label = Label(input_frame, pady = 10 ,text = "PASSWORD:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )

    input_seg_name = Entry(input_frame,text = "Enter NEW NAME")
    input_password = Entry(input_frame,show="*",text = "Password")

    join_btn = Button(input_frame, text= 'Change', command = partial(send_join_req,username, join_form,sock, input_seg_name,input_password))
    
    name_label.pack(side = TOP, fill = 'both')
    input_seg_name.pack(side = TOP, fill = 'both')
    password_label.pack(side = TOP, fill = 'both')
    input_password.pack(side = TOP, fill = 'both')
    join_btn.pack(side = TOP, fill = 'both')
    
    
    input_frame.pack()
    join_form.mainloop()
def send_join_req(username, join_form,sock, input_seg_name,input_password):
    """
    send and handle the join_seg_req to the main server
    """
    msg = 'joinSeg^'+input_seg_name.get() +"^"+input_password.get()
    sock.send(msg)
    sock.send("done...")
    data = sock.recv(BUFSIZ)
    if data != "added":
        messagebox.showwarning(title="Failed", message=data)
    join_form.destroy()
    main_tab(sock,username)
def send_upgrade_req(username, upgrade_form,sock,input_password):
    """
    send and handle the upgrade_premission to the main server
    this req is for changing the premission in the seg
    from R to W
    """
    global CURR_SEG
    msg = 'upgradePremission^'+CURR_SEG+"^"+input_password.get()
    sock.send(msg)
    sock.send("done...")
    data = sock.recv(BUFSIZ)
    if data != "you upgraded":
        messagebox.showwarning(title="Failed", message=data)
    upgrade_form.destroy()
    main_tab(sock,username)
def open_upgrade_form(root, sock,username):
    """
    create the upgrade_premission_req form
    """
    global CURR_SEG
    root.destroy()
    upgrade_form = Tk()
    upgrade_form.geometry("500x200+100+100")
    upgrade_form.resizable(width=FALSE, height=FALSE)
    upgrade_form.title("UPGRADE YOUR PREMISSION")
    upgrade_form["background"]= 'blue'

    top_label = Label(upgrade_form, pady = 10 ,text = ("--UPGRADE YOUR PREMISSION IN SEG: "+CURR_SEG+"--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(upgrade_form, background = 'blue',padx = 10 ,pady = 10)
    password_label = Label(input_frame, pady = 10 ,text = "ENTER SEG PASSWORD", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue')
    input_password = Entry(input_frame,show="*",text = "Password")
    join_btn = Button(input_frame, text= 'Upgrade', command = partial(send_upgrade_req,username, upgrade_form,sock,input_password))

    password_label.pack(side = TOP, fill = 'both')
    input_password.pack(side = TOP, fill = 'both')
    join_btn.pack(side = TOP, fill = 'both')

    input_frame.pack(side = TOP, fill = 'both')
    upgrade_form.mainloop()
def send_seg_name_req(username, new_name_form,sock, input_file_name,input_password):
    """
    sends seg rename req to the server and handle it
    """
    global segs_and_files
    global CURR_SEG
    global CURR_FILE

    sock.send("changeSegName^"+CURR_SEG+"^"+input_password.get()+"^"+input_file_name.get())
    sock.send("done...")
    data = sock.recv(BUFSIZ)

    if data != "changed":
        messagebox.showwarning(title="Failed", message=data)
    new_name_form.destroy()
    main_tab(sock, username)
def change_seg_name(root ,sock, username):
    """
    create the seg rename form
    """
    global segs_and_files
    global CURR_SEG
    global CURR_FILE
    root.destroy()
    
    new_name_form = Tk()
    new_name_form.geometry("500x250+100+100")
    new_name_form.resizable(width=FALSE, height=FALSE)
    new_name_form.title("SET NEW NAME")
    new_name_form["background"]= 'blue'
    top_label = Label(new_name_form, pady = 10 ,text = ("--CHOOSE THE NEW NAME OF "+CURR_SEG+"--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)

    input_frame = Frame(new_name_form, background = 'blue',padx = 10 ,pady = 10)
    name_label = Label(input_frame, pady = 10 ,text = "NEW NAME:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    password_label = Label(input_frame, pady = 10 ,text = "PASSWORD:", relief = "flat", font = "Helvetica 10 bold italic", background = 'blue' )
    input_file_name = Entry(input_frame,text = "Enter NEW NAME")
    input_password = Entry(input_frame,show="*",text = "Password")
    change_btn = Button(input_frame, text= 'Change', command = partial(send_seg_name_req,username, new_name_form,sock, input_file_name,input_password))
    
    name_label.pack(side = TOP, fill = 'both')
    input_file_name.pack(side = TOP, fill = 'both')
    password_label.pack(side = TOP, fill = 'both')
    input_password.pack(side = TOP, fill = 'both')
    change_btn.pack(side = TOP, fill = 'both')

    input_frame.pack(side = TOP, fill = 'both')
    new_name_form.mainloop()
def send_seg_move_req(username, move_form,sock, last_seg):
    """
    sends and handle changing file's seg
    """
    global segs_and_files
    global CURR_SEG
    global CURR_FILE

    file_name = str(segs_and_files[last_seg][CURR_FILE-1][0])
    sock.send("moveFile^"+last_seg+"^"+file_name+"^"+CURR_SEG)
    sock.send("done...")
    data = sock.recv(BUFSIZ)

    if data == "moved":
        move_form.destroy()
        main_tab(sock, username)
    else:
        messagebox.showwarning(title="Failed", message=data)
def open_move_form(root, sock,username):
    """
    create the moving file form
    the user select the new seg to the chosen file
    """

    global segs_list
    global files_list
    global segs_and_files
    global segs_and_premissions
    global CURR_FILE
    global CURR_SEG

    last_seg = CURR_SEG

    root.destroy()
    
    move_form = Tk()
    move_form.geometry("600x400+100+100")
    move_form.resizable(width=FALSE, height=FALSE)
    move_form.title("MOVE FILE")
    move_form["background"]= 'blue'

    top_label = Label(move_form, pady = 10 ,text = ("--CHOOSE THE NEW SEG OF "+str(segs_and_files[CURR_SEG][CURR_FILE-1][0]) +"--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(move_form, background = 'blue',padx = 10 ,pady = 10)
    segs_label = Label(input_frame, pady = 10 ,text = "YOUR SEGS:", relief = "flat", font = "Helvetica 12 bold italic", background = 'blue' )
    change_btn = Button(move_form, text= 'MOVE', command = partial(send_seg_move_req,username, move_form,sock, last_seg),width = 50 ,height = 70)
    segs_list = Listbox(input_frame,)
    for seg_name in segs_and_files.keys():
        if seg_name != CURR_SEG:
            segs_list.insert(END, seg_name)

    scrollbar = Scrollbar(input_frame, orient="vertical")
    scrollbar.config(command=segs_list.yview)
    scrollbar.pack(side="right", fill="y")
    segs_list.config(yscrollcommand=scrollbar.set)
    
    segs_list.bind('<<ListboxSelect>>', on_select_seg)
    
    segs_label.pack(side = TOP, fill = 'both')
    segs_list.pack(side = TOP, expand="YES",fill = 'both')
    input_frame.pack(fill = 'both')
    change_btn.pack(fill = 'both')
    move_form.mainloop()
def send_change_name_req(sock,username,new_name):
    """
    sends and handle rename_req to the main server
    """
    msg = 'changeUserName^'+new_name
    sock.send(msg)
    sock.send('done...')

    data = sock.recv(BUFSIZ)
    if data == "changed":
        username = new_name
        return True
    else:
        messagebox.showwarning(title="Failed", message=data)
        return False
def send_change_password_req(sock,last_password,new_password):
    """
    sends and handle change_password_req to the main server
    """
    global USER_PASSWORD
    msg = 'changePassword^'+last_password+'^'+new_password
    sock.send(msg)
    sock.send('done...')

    data = sock.recv(BUFSIZ)
    if data == "changed":
        USER_PASSWORD = new_password
        return True
    else:
        messagebox.showwarning(title="Failed", message=data)
        return False
def send_change_reqs(username, user_form,sock, input_name, input_password):
    """
    handle the changes in the user setting form
    """
    global USER_PASSWORD
    was_name_changed = input_name.get() != ''
    was_password_changed = input_password.get() != ''
    name_done , password_done = True, True
    if was_name_changed:
        name_done = send_change_name_req(sock,username,input_name.get())
        username = input_name.get()
    if was_password_changed:
        password_done = send_change_password_req(sock,USER_PASSWORD,input_password.get())
        USER_PASSWORD = input_password.get()
    if not password_done and name_done:
        messagebox.showwarning(title="Failed", message="something went wrong")
    user_form.destroy()
    main_tab(sock, username)
def open_user_form(root, sock,username):
    """
    create the user setting form, it's for changing the username, password - not for admin(change manualy)
    """
    global USER_PASSWORD

    root.destroy()
    
    user_form = Tk()
    user_form.geometry("1200x500+100+100")
    user_form.minsize(1200,500)
    user_form.title("USER SETTINGS")
    user_form["background"]= 'blue'

    top_label = Label(user_form, pady = 10 ,text = ("--USER SETTINGS--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(user_form, background = 'blue',padx = 10 ,pady = 10)
    username_label = Label(input_frame, pady = 10 ,text = "ENTER THE NEW NAME - null -> no change", relief = "flat", font = "Helvetica 12 bold italic", background = 'blue' )
    password_label = Label(input_frame, pady = 10 ,text = "ENTER THE NEW PASSWORD - null -> no change", relief = "flat", font = "Helvetica 12 bold italic", background = 'blue' )
    input_name = Entry(input_frame,text = "NEW USERNAME")
    input_password = Entry(input_frame,show="*",text = "NEW PASSWORD")
    
    reset_btn = Button(input_frame, text= 'RESET', command = partial(send_change_reqs,username, user_form,sock, input_name, input_password),width = 50 ,height = 10)
    

    username_label.pack(side = TOP, fill = 'both')
    input_name.pack(side = TOP, fill = 'both')
    password_label.pack(side = TOP, fill = 'both')
    input_password.pack(side = TOP, fill = 'both')
    reset_btn.pack(side = TOP, fill = 'both')

    input_frame.pack()
    user_form.mainloop()
def open_event_log(root, sock,username):
    """
    only for admins

    loading the event_log_file 
    and display all the events in the server
    """
    root.destroy()
 
    log_dir = get_info_from_cloud(sock, 'getEventLog')[0]
    with open(log_dir, 'r') as f:
        events = f.readlines()

    event_form = Tk()
    event_form.geometry("600x400+100+100")
    event_form.resizable(width=FALSE, height=FALSE)
    event_form.title("EVENT LOG")
    event_form["background"]= 'blue'

    top_label = Label(event_form, pady = 10 ,text = ("--EVENT LOG--"), relief = "flat", font = "Helvetica 20 bold italic", background = 'blue' )
    top_label.pack(side = TOP)
    input_frame = Frame(event_form, background = 'blue',padx = 10 ,pady = 10)
    segs_label = Label(input_frame, pady = 10 ,text = "Events:", relief = "flat", font = "Helvetica 12 bold italic", background = 'blue' )
    change_btn = Button(event_form, text= 'BACK', command = partial(refresh,event_form,sock, username), width = 50 ,height = 70)
    segs_list = Listbox(input_frame,)
    
    for event in events:
        segs_list.insert(END, event)

    scrollbar = Scrollbar(input_frame, orient="vertical")
    scrollbar.config(command=segs_list.yview)
    scrollbar.pack(side="right", fill="y")
    segs_list.config(yscrollcommand=scrollbar.set)
    
    segs_list.bind('<<ListboxSelect>>', on_select_seg)
    
    segs_label.pack(side = TOP, fill = 'both')
    segs_list.pack(side = TOP, expand="YES",fill = 'both')
    input_frame.pack(fill = 'both')
    change_btn.pack(fill = 'both')
    event_form.mainloop()
def main_tab(sock, username):
    """
    the cloud window
    change according the premission (admin or not)
    """
    global segs_list
    global files_list
    global segs_and_files
    global segs_and_premissions
    global IS_ADMIN

    root = Tk()
    root.geometry("1200x500+100+100")
    root.minsize(1200,500)
    root.title("DDRIVE")
    
    head_frame = Frame(root,background = 'blue',padx = 10 ,pady = 10)
    """img = PhotoImage(file="C:\Users\yuval\Desktop\School\Cyber\Final_Project\MAXIMUM media.png")
    lb1 = Label(root,image=img, background = 'blue')
    lb1.pack()"""
    
    print 'loaded'
    welcome_label = Label(head_frame, pady = 10 ,text = ("HELLO " +username), relief = "flat", font = "Helvetica 50 bold italic", background = 'blue' )
    welcome_label.pack(side = LEFT)
    
    segs_and_files = dict(get_info_from_cloud(sock, 'Segments'))
    segs_and_premissions = dict(get_info_from_cloud(sock, 'Premissions'))

    lists_frame = Frame(root,background = 'blue',padx = 10 ,pady = 10)
    segs_list = Listbox(lists_frame,)
    files_list = Listbox(lists_frame,)

    for seg_name in segs_and_files.keys():
        segs_list.insert(END, seg_name)

    segs_list.bind('<<ListboxSelect>>', on_select_seg)
    segs_list.pack(side = LEFT, expand="YES",fill = 'both')
    files_list.bind('<<ListboxSelect>>', on_select_file)
    files_list.pack(side = LEFT, expand="YES",fill = 'both')



    seg_btns_frame = Frame(root,background = 'blue',padx = 5 ,pady = 10)

    add_btn = Button(seg_btns_frame, text= 'ADD FILE', command = partial(add_file_to_seg, root,sock,username),width =20 ,height = 2)
    add_btn.pack(expand="YES", side = TOP )

    download_btn = Button(seg_btns_frame, text= 'DOWNLOAD FILE', command = partial(download_file_from_seg, sock),width = 20 ,height = 2)
    download_btn.pack(expand="YES", side = TOP )
    
    download_folder_btn = Button(seg_btns_frame, text= 'DOWNLOAD FOLDER', command = partial(download_folder_from_seg, sock),width = 20 ,height = 2)
    download_folder_btn.pack(expand="YES", side = TOP )

    change_file_name_btn = Button(seg_btns_frame, text= 'CHANGE FILE NAME', command = partial(change_file_name, root ,sock, username),width = 20 ,height = 2)
    change_file_name_btn.pack(expand="YES",  side = TOP )

    change_seg_name_btn = Button(seg_btns_frame, text= 'CHANGE SEG NAME', command = partial(change_seg_name, root, sock, username),width = 20, height = 2)
    change_seg_name_btn.pack(expand="YES",  side = TOP )

    if not IS_ADMIN:
        upgrade_premission_btn = Button(seg_btns_frame, text= 'UPGRADE PREMISSION', command = partial(open_upgrade_form, root, sock, username),width = 20 ,height = 2)
        upgrade_premission_btn.pack(expand="YES" , side = TOP )
    
    move_file_btn = Button(seg_btns_frame, text= 'MOVE FILE', command = partial(open_move_form, root, sock,username),width = 20 ,height = 2)
    move_file_btn.pack(expand="YES" , side = TOP )

    if not IS_ADMIN:
        exit_seg_btn = Button(seg_btns_frame, text= 'LEAVE SEG', command = partial(leave_seg, sock, root,username),width = 20 ,height = 2)
        exit_seg_btn.pack(expand="YES",  side = TOP)
    
    cloud_btns_frame = Frame(root,background = 'blue',padx = 10 ,pady = 10)
    
    if not IS_ADMIN:
        join_btn = Button(cloud_btns_frame, text= 'JOIN SEG', command = partial(join_new_seg, root, sock,username),width = 10 ,height = 10)
        join_btn.pack(expand="YES", side = LEFT )

    create_seg_btn = Button(cloud_btns_frame, text= 'CREATE SEG', command = partial(create_new_seg,root, sock, username),width = 10 ,height = 10)
    create_seg_btn.pack(expand="YES", side = LEFT )
    
    if not IS_ADMIN:
        user_setting_btn = Button(cloud_btns_frame, text= 'USER SETTING', command = partial(open_user_form, root, sock,username),width = 10 ,height = 10)
        user_setting_btn.pack(expand="YES", side = LEFT )
    else:
        event_log_btn = Button(cloud_btns_frame, text= 'EVENT LOG', command = partial(open_event_log, root, sock,username),width = 10 ,height = 10)
        event_log_btn.pack(expand="YES", side = LEFT )       
    
    refresh_btn = Button(cloud_btns_frame, text= 'REFRESH', command = partial(refresh,root,sock, username),width = 10 ,height = 10)
    refresh_btn.pack(expand="YES", side = LEFT )

    head_frame.pack(expand="YES",fill = 'both', side = TOP)
    seg_btns_frame.pack(expand="YES",fill = 'both',side = LEFT)
    lists_frame.pack(expand="YES",fill = 'both',side = LEFT)
    cloud_btns_frame.pack(expand="YES",fill = 'both',side = BOTTOM)
    
    
    root.mainloop()
    
#tkinter functions - END








#public consts variables
HOST = '10.0.0.5'
PORT = 50010
BUFSIZ = 1024
ADDR = (HOST, PORT)
DIRECTORY_FOLDER = ''
CURR_SEG = ''
CURR_FILE = 0
IS_ADMIN = False
USER_PASSWORD = ''
segs_and_files = {}
segs_and_premissions = {}

#create the connection to the log-reg server
tcpCliSock = socket(AF_INET , SOCK_STREAM)
tcpCliSock.connect(ADDR)
#start display
create_login_register_tab(tcpCliSock)
