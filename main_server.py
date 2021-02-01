from socket import *
import thread
import database_handler as db
from classes import *
import pickle

def translate_protocol(data):
    """
    split the values from the string
    """
    return data.split('^')

def handler(clientsock,cloud,user,addr, dir_name_cloud):
    """
    handle and response to the client requests
    """
    while clientsock:
        req = clientsock.recv(BUFSIZ)
        if not req:
            print "ending communication with", addr
            break
        next_bin = ""
        while not "done..." in next_bin and not "done..." in next_bin:
            print next_bin,
            req += next_bin
            next_bin = clientsock.recv(BUFSIZ)
        req += next_bin
        req = req.replace("done...", "")
        data = translate_protocol(req)
        print len(req)
        print len(data)
        if data[0] == 'open':
            if cloud.createNewSegment(data[1],data[2], data[3]):
                clientsock.send("opened")
                cloud.refresh_users()
            else:
                clientsock.send("failed")
        elif data[0] == 'add':
            print 'adding...'
            seg = cloud.get_seg_object(data[1])
            if seg:
                print 'adding...'
                if seg.add(user.get_name(), data[2],"^".join(data[3:])):
                    print 'adding...'
                    clientsock.send("file uploaded")
                else:
                    clientsock.send("failed - upload")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'download':
            seg = cloud.get_seg_object(data[1])
            if seg:
                details = seg.download(user.get_name(), data[2], user.get_directory_folder())
                if len(details) > 0:
                    download_str = str(details[1]) + "~" +str(details[0])
                    print len(download_str)
                    clientsock.send(download_str)
                    clientsock.send("done...")
                else:
                    clientsock.send("failed - check your premissions")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'changeUserName':
            print 'changing'
            has_done , new_user = cloud.set_user_name(user.get_name(),data[1] )
            if has_done:
                user = new_user
                clientsock.send("changed")
            else:
                clientsock.send("failed - check values")
        elif data[0] == 'changePassword':
            print "password changing"
            if user.change_password(data[1], data[2]):
                print 'done'
                clientsock.send("changed")
                
            else:
                print 'failed'
                clientsock.send("failed - check values")
        elif data[0] == 'changeSegName':
            seg = cloud.get_seg_object(data[1])
            if seg:
                if cloud.change_seg_name(seg,user.get_name(),data[2],data[3]):
                    clientsock.send("changed")
                else:
                    clientsock.send("failed - check values")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'joinSeg':
            if cloud.add_user_to_seg(user, data[1], data[2]):
                clientsock.send("added")
            else:
                clientsock.send("failed - check values")
        elif data[0] == 'exitSeg':
            seg = cloud.get_seg_object(data[1])
            if seg:
                print 'start'
                if cloud.delete_user_from_seg(user, seg):
                    clientsock.send("you left")
                else:
                    clientsock.send("failed - check values")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'upgradePremission':
            seg = cloud.get_seg_object(data[1])
            if seg:
                print 'start'
                if seg.add_change_premission(user.get_name(), data[2]):
                    clientsock.send("you upgraded")
                else:
                    clientsock.send("failed - check values")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'changeFileName':
            seg = cloud.get_seg_object(data[1])
            if seg:
                print 'start changing'
                if seg.change_name_file(user.get_name(), data[2], data[3]):
                    clientsock.send("changed")
                else:
                    clientsock.send("failed - check values")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'loadDataCloud':
            print 'loading data....'
            try:
                data = cloud.load_data_client(user, data[1])
                #data = pickle.dumps(list(data))
                print data
                clientsock.send(str(data))
            except:
                clientsock.send("failed - check values")
        elif data[0] == 'moveFile':
            curr_seg = cloud.get_seg_object(data[1])
            next_seg = cloud.get_seg_object(data[3])
            if curr_seg and next_seg:
                print 'start moving'
                #move_file(self, user,curr_seg,file_name, next_seg)
                if cloud.move_file(user, curr_seg, data[2],next_seg):
                    clientsock.send("moved")
                else:
                    clientsock.send("failed - check values")
            else:
                clientsock.send("failed - check name/premissions")
        elif data[0] == 'exit':
            clientsock.close()
            break
        else:
            clientsock.send("failed - check name/premissions")
        print user
    #set the user as offline
    user.setCondition(0)
    

#databases dirs
dir_name_cloud = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\Cloud.db"
dir_name_login = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\UserPassword.db"
files_data_dir = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\Files"

#admin details
admin_username = "Eran"
admin_password = "Binet"
admin_directory = 'C:/Users/yuval/Desktop'

#communication consts
BUFSIZ = 1024
HOST = '10.0.0.5'
PORT = 50011
ADDR = (HOST, PORT)

#create the socket
serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(2)

#create the cloud object
main_cloud = Cloud(dir_name_cloud, dir_name_login, admin_username)


while 1:
    print 'waiting for connection...'
    clientsock, addr = serversock.accept()
    #loading all the online clients
    USERS_IPS = dict(map(lambda user: (user.get_ip(), user.get_name()), main_cloud.get_active_users())) #dictionary ip :username - for the online users
    
    #approve connection according to the ip - in order identify the user
    if not addr[0] in USERS_IPS.keys():
        clientsock.close()
    else:
        print USERS_IPS
        print 'connected from:   ', addr
        thread.start_new_thread(handler, (clientsock,main_cloud, main_cloud.get_user(USERS_IPS[addr[0]]),addr,dir_name_cloud))
