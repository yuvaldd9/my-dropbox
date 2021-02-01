"""
register/ login server

premision = seqments
"""
from socket import *
import ssl
import os, sys
import thread 
import database_handler as db

def create_db(dir_name, admin_username, admin_password,admin_directory):
    """
    create the users database and write the admin details
    """
    global MAIN_HOST
    if not os.path.isfile(dir_name):
        table_str = ''' CREATE TABLE users(id INTEGER PRIMARY KEY,
                     username TEXT, password TEXT, ip TEXT , isActive INTEGER , premissions TEXT, directory_folder TEXT)'''
        f = open(dir_name, 'w')
        db.create_table(dir_name, table_str)
        f.close()
        db.register(dir_name, admin_username, hash(admin_password), 'ALL', MAIN_HOST ,admin_directory)

def login(clientsock, data_login, dir_name , MAIN_ADDR):
    """
    manage login
    """
    global admin_username
    try:
        username, password = collect_msg_data(data_login , False)
        password = hash(password)
        return db.login(dir_name, username, password)
    except:
        return False
def collect_msg_data(msg ,is_registeration):
    values = msg.split('^')
    if is_registeration:
        print values
        return values[0] , values[1] , values[2],values[3]
    return values[0] , values[1]
def register(clientsock, data_register,dir_name , ip ,MAIN_ADDR):
    """
    manage register
    """
    username, password, premisions, directory_folder = collect_msg_data(data_register , True)
    password = hash(password)
    if not db.check_username(dir_name , username):
        return 0
    return db.register(dir_name, username, password, premisions, ip,directory_folder)
def handler(clientsock,addr, MAIN_ADDR, dir_name):
    #data: r/l + username + ^ + password + ^ + premisions(only for registeration)
    global admin_username
    while 1:
        data = clientsock.recv(BUFSIZ)
        if not data:
            print "ending communication with", addr
            break
        if data[0] == 'r':
            is_registerd = register(clientsock, data[1:],dir_name ,addr[0], MAIN_ADDR)
            if is_registerd == 1:
                clientsock.send('*'+str(MAIN_ADDR))
                break
            elif is_registerd == 0:
                clientsock.send('resend, the name is taken')
            else:
                clientsock.send("try again")
        elif data[0] == 'l':
            is_logged = login(clientsock, data[1:]  ,dir_name, MAIN_ADDR)
            if is_logged == 1:
                #print collect_msg_data(data[1:],False)[0]
                char_code = '%' if collect_msg_data(data[1:],False)[0] == admin_username else '*'
                clientsock.send(char_code+str(MAIN_ADDR))
                break
            elif is_logged == 0:
                clientsock.send('wrong values!!!!')
            else:
                clientsock.send("try again")
        else:
            clientsock.send('resend')

        
    clientsock.close()

dir_name = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\UserPassword.db"
BUFSIZ = 1024
HOST = '10.0.0.5'
MAIN_HOST = '10.0.0.5'
PORT = 50010
MAIN_HOST_PORT = 50011
ADDR = (HOST, PORT)
MAIN_ADDR = (MAIN_HOST, MAIN_HOST_PORT)

admin_username = "Eran"
admin_password = "Binet"
admin_directory = 'C:/Users/yuval/Desktop'
create_db(dir_name,admin_username, admin_password, admin_directory)

serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(2)


while 1:
    print 'waiting for connection...'
    clientsock, addr = serversock.accept()
    print 'connected from:   ', addr
    thread.start_new_thread(handler, (clientsock, addr, MAIN_ADDR, dir_name))

serversock.close()
main_server_sock.close()