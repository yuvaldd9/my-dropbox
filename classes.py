import sqlite3 as lite
import database_handler as db
import os, sys
import re
import datetime



class Client:
    """
    client functions, details
    """
    dir_name_login = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\UserPassword.db"
    idClient = 0
    def __init__(self , username, segments, isActive, directory_folder, ip):
        self.username = username
        #self.segments = Cloud.get_segements_by_premissions(premissions, username)
        self.segments = segments
        self.isActive = isActive
        self.ip = ip
        self.directory_folder = directory_folder
    def  __str__(self):
        return ('user details '+self.get_name()+ ' his segs: ' + str(self.getSegments()))
    def change_password(self, curr_pass, new_pass):
        """
        change the client object password and in the database
        """
        password = db.getDataFromCloud(Client.dir_name_login, '''SELECT password FROM users WHERE username = "'''+self.username+'''"''')
        print hash(curr_pass)
        print password[0][0]
        if str(hash(curr_pass)) == password[0][0]:
            print "changing..."
            db.change_user_password(Client.dir_name_login, self.username ,new_pass)
            return True
        return False
    def add_seg(self, seg):
        """
        add seg to the segments list of the client object
        """
        self.segments.append(seg)
        return True
    def delete_seg(self, seg):
        """
        add seg to the segments list of the client object
        """
        self.segments.remove(seg)
        if self.segments:
            premissions_str = '^'+'^'.join(map(lambda seg: seg.get_name() , self.segments))
        else:
            premissions_str = ''
        return db.update_user_premission(Client.dir_name_login, self.username, premissions_str)
    def get_ip(self):
        """
        return the ip of the client
        """
        return self.ip
    def getSegments(self):
        """
        return the segments of the client
        """
        return self.segments
    def get_directory_folder(self):
        """
        return the directory_folder of the client
        """
        return self.directory_folder
    def setCondition(self, value = 2):
        """
        set the client condition + in the database
        """
        if value == 2:
            self.isActive = 0 if self.isActive == 1 else 1
            db.setActive(Client.dir_name_login ,self.username, self.isActive)      
        else:
            db.setActive(Client.dir_name_login ,self.username, value)      
    def set_segments(self, new_segments):
        """
        set the client segments
        """
        self.segments = new_segments
    def set_directory_folder(self, path):
        """
        set the directory folder
        """
        self.directory_folder = path    
    def getCondition(self):
        """
        get the condition of the client - offline/online
        """
        return self.isActive
    def get_name(self):
        """
        get the name of the client
        """
        return self.username
    def set_name(self, new_username):
        """
        rename the client
        """
        self.username = new_username
    @staticmethod
    def getNumOfUsers():
        print "online right now: ",Client.idClient,"users."
        return Client.idClient
class Segment:
    login_db_dir = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\UserPassword.db"
    def __init__(self, cloud_dir ,name, users_and_premissions, password, is_exist):
        self.cloud_dir = cloud_dir
        self.name = name
        self.password = password
        self.users_and_premissions = users_and_premissions
        if not is_exist:
            self.table_str = ''' CREATE TABLE '''+str(name)+''' (id INTEGER PRIMARY KEY, file_name TEXT ,file_extension TEXT , file_directory TEXT, size INTEGER)'''
            self.files = []
            db.add_seg_to_data(self.cloud_dir, self.name, self.__convert_dict_to_premission_str__(users_and_premissions), self.password)
            self.__cloud_add_segment_(self.table_str)
            db.update_premissions(self.cloud_dir , self.__convert_dict_to_premission_str__(self.users_and_premissions), self.name)
            self.__add_seg_to_users_premissions__(self.users_and_premissions)
        else:
            self.files = db.get_seg_files(self.cloud_dir , self.name)             
    def update_username(self,username, new_username):
        """
        update the seg's users
        """
        self.users_and_premissions[new_username] = self.users_and_premissions[username]
        del self.users_and_premissions[username]
        return db.update_premissions(self.cloud_dir , self.__convert_dict_to_premission_str__(self.users_and_premissions), self.name)   
    def add_user(self, user, password):
        """
        manage adding new user to the seg - premissions
        """
        if user.get_name() in self.users_and_premissions.keys():
            return False
        db.add_user_premission(Segment.login_db_dir, user.get_name(), self.name)
        print "added", user, "to", self.name, " premissions"
        db.write_in_log(Cloud.event_log_dir, str(datetime.datetime.now()) +"added"+ user.get_name(), "to", self.name)
        return self.add_new_premission(user.get_name(), password)          
    def __add_seg_to_users_premissions__(self, users_and_premissions):
        """
        PRIVATE
        add the seg to the user premissions in the database
        """
        for username in users_and_premissions:
            db.add_user_premission(Segment.login_db_dir, username, self.name)
    def __load_users__(self, users_and_premissions):
        """
        PRIVATE
        loading the users objects 
        """
        users  = {}
        for username in users_and_premissions.keys():
            users[username] = Cloud.get_user(username)
        return users
    def __cloud_add_segment_(self, table_str):
        """
        create the table in the database
        """
        db.create_table(self.cloud_dir, table_str)
    def add(self, user, file_path, file_binary):
        """
        create and save the file data in the server folder and in the database
        """
        premission = self.users_and_premissions[user]
        print user , "pre: ", premission, "uploading:  ", file_path, "file binary: ", len(file_binary)
        if premission == 'W' or premission == 'A':
            #file_data = (file_path.split('\\')[-1]).split('.')
            file_data = os.path.splitext(os.path.basename(file_path))
            file_name, file_extention = file_data[0], file_data[1]
            file_name = self.name_management(file_name)
            saved_file_path = os.path.join(Cloud.files_data_dir,file_name)
            
            if db.add_file(self.cloud_dir, file_name, file_extention, file_binary, saved_file_path , self.name):  
                self.files.append((file_name, file_extention, len(file_binary)))
            print self.name, " files: ", self.files
            db.write_in_log(Cloud.event_log_dir, user +"file added "+ str(datetime.datetime.now()) +"seg: "+ self.name +' file data: ' + str((file_name, file_extention, len(file_binary))))
            return True
        else:
            return False
    def add_file(self, username, file_data):
        """
        add file details to the seg lists
        """
        if self.__can_change__(username):
            self.files.append(file_data)
            db.write_in_log(Cloud.event_log_dir,username +"file added "+ str(datetime.datetime.now()) +"seg: "+ self.name +' file data: ' + str(file_data))
            return True
        return False
    def name_management(self, file_name):
        """
        check and handle same name events
        """
        files_names = map(lambda file_details: file_details[0], self.files)
        if file_name in files_names:
            return file_name +"("+ str(len(filter(lambda name: name == file_name, files_names)))+ ")"
        return file_name
    def get_seg_files(self):
        return self.files
    def download(self, user, file_name,directory_folder):
        """
        return the download path of the user, the file binary
        according the Premission
        """
        premission = self.users_and_premissions[user]
        if premission == 'R' or premission == 'A':
            command = '''SELECT file_directory,file_extension  FROM '''+str(self.name)+''' WHERE file_name= "'''+ (file_name)+'''"'''
            path = os.path.join(directory_folder , file_name)
            file_data = db.getDataFromCloud(self.cloud_dir , command)
            server_file_path ,file_extension = str(file_data[0][0]) , file_data[0][1]
            #
            print server_file_path
            with open((server_file_path + file_extension), "rb") as f:
                file_binary = f.read()
            db.write_in_log(Cloud.event_log_dir, user +"downloaded file "+ str(datetime.datetime.now()) + 'file name: ' + file_name)
            return file_binary, path+file_extension
        else:
            return None
    def is_in_the_seg(self, username):
        return username in self.users_and_premissions.keys()
    def get_user_premission(self, username):
        print username, 'req premission'
        return self.users_and_premissions[username]
    def has_access(self, username):
        """
        check if the the user is in the seg premissions
        """
        if username in self.users_and_premissions.keys():
            return True
        return False
    def get_name(self):
        return self.name
    def get_file_id(self, file_name):
        return self.files[file_name]
    def delete_file(self, user, file_name):
        """
        delete file in the database
        according the user premissions
        """
        premission = self.users_and_premissions[user]
        if  premission == 'W' or premission == 'A':
            if db.delete_file(self.cloud_dir, self.name, file_name):
                data = filter(lambda file_data: file_data[0] == file_name, self.files)[0]
                self.files.remove(data)
                db.write_in_log(Cloud.event_log_dir, str(datetime.datetime.now()) + 'removed from' + self.name+" : " +str(data))
                print 'removed from', self.name," : " ,data
                return data
        else:
            return False
    def change_name_file(self, user, file_name, new_name):
        """
        change file name: seg_object + database
        """
        premission = self.users_and_premissions[user]
        if  premission == 'W' or premission == 'A':
            if db.change_name_file(self.cloud_dir, self.name, file_name, new_name):
                last_file_details = filter(lambda file_data: file_data[0] == file_name, self.files)[0]
                self.files[self.files.index(last_file_details)] = (new_name, last_file_details[1], last_file_details[2])
                db.write_in_log(Cloud.event_log_dir, "file name changed--" +str(datetime.datetime.now()) +"--seg: "+ str(self.name)+" file: "+ str(file_name)+" to: "+ new_name)
                return True
            return False
        else:
            return False
    def add_change_premission(self, user, password, premission = 'W'):
        """
        change premissions
        """
        last_premission = self.users_and_premissions[user]
        if password == self.password and last_premission != 'A' and last_premission != 'W':
            self.users_and_premissions[user] = premission
            db.write_in_log(Cloud.event_log_dir, "seg premissions changed--" +str(datetime.datetime.now()) +"--seg: "+ str(self.name)+" -- "+ str(self.users_and_premissions))
            return db.update_premissions(self.cloud_dir , self.__convert_dict_to_premission_str__(self.users_and_premissions), self.name)
        return False
    def add_new_premission(self, user, password):
        """
        add to the seg's premissions the new user
        """
        self.users_and_premissions[user] = 'R'
        return db.update_premissions(self.cloud_dir , self.__convert_dict_to_premission_str__(self.users_and_premissions), self.name)
    def __convert_dict_to_premission_str__(self, premissions_dict):
        """
        convert the dictionary of the users premissions to str according our protocol
        --explanations in the word file--
        """
        premissions_str = ""
        for user_name in premissions_dict.keys():
            premissions_str += str(user_name + ":" + premissions_dict[user_name])
            premissions_str += "#"
        return premissions_str[:len(premissions_str)-1]
    def change_table_name(self, username,seg_password,new_name):
        """
        change table name in the object + database
        """
        print self.users_and_premissions.keys()
        last_name = self.name
        if self.password == seg_password and self.__can_change__(username):
            result = db.change_name_segment(self.cloud_dir, Segment.login_db_dir  ,self.name, new_name, self.users_and_premissions.keys())
            if result:
                self.name = new_name
                db.write_in_log(Cloud.event_log_dir, "seg name changed--" +str(datetime.datetime.now()) +"--from: "+ str(last_name)+" to: "+ str(self.name))
            return result
        return False
    def __can_change__(self, username):
        """
        check according the user premissions if the user can change details in the seg
        """
        user_pre = self.users_and_premissions[username]
        return user_pre == 'W' or user_pre == 'A'
    def __del__(self):
        """
        delete the seg
        """
        db.write_in_log(Cloud.event_log_dir, "seg deleted--" +str(datetime.datetime.now()) +"--seg name: "+ str(self.name))
        return db.delete_seg(self.cloud_dir, self.name)
    def manage_premissions(self, premission):
        """
        handle the premissions when user leave the seg
        """
        if premission == 'A':
            writers = filter(lambda user_premission: user_premission[1] == 'W', list(self.users_and_premissions))
            if writers != []:
                self.users_and_premissions[writers[0][0]] = 'A'
                return db.update_premissions(self.cloud_dir , __convert_dict_to_premission_str__(self.users_and_premissions))
            elif len(self.users_and_premissions.keys()) != 0:
                self.users_and_premissions[self.users_and_premissions.keys()[0]] = 'A'
                return True
            else:
                return self.__del__()
        else:
            if len(self.users_and_premissions.keys()) == 0:
                return self.__del__()    
    def delete_user(self, username):
        """
        delte the user from the seg premission in the object and the database
        """
        deleted_user_premission = self.users_and_premissions[username]
        del self.users_and_premissions[username]
        new_premission_str = self.__convert_dict_to_premission_str__(self.users_and_premissions)
        if db.update_premissions(self.cloud_dir , self.__convert_dict_to_premission_str__(self.users_and_premissions), self.name):
            return self.manage_premissions(deleted_user_premission)
        return False

class Cloud:   
    files_data_dir = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\Files"
    event_log_dir = r"C:\Users\yuval\Desktop\School\Cyber\Final_Project\Event_Log.txt"
    def __init__(self, cloud_dir,dir_name_login,admin_username):
        self.admin_username = admin_username
        self.__create_cloud__(cloud_dir)
        self.cloud_dir = cloud_dir
        self.dir_name_login = dir_name_login
        self.segments_names = db.loadSegmentsNames(cloud_dir)
        self.segments = self.__load_segments_from_cloud__(cloud_dir)
        self.all_users = self.__convertDataToObject_USER__(db.loadAllUsers(self.dir_name_login))
        self.__create_event_log__(Cloud.event_log_dir)        
    def __convertDataToObject_USER__(self,list_of_data):
        """
        create all the users objects
        """
        users_list = {}
        for data in list_of_data:
            if data[0] == self.admin_username:
                users_list[data[0]] = (Client(data[0] , self.segments.values() , data[1], data[3], data[4]))
            else:
                users_list[data[0]] = (Client(data[0] , self.get_segements_by_premissions(data[2], data[0]) , data[1], data[3], data[4]))
        print users_list
        db.write_in_log(Cloud.event_log_dir, "users loaded -" +str(datetime.datetime.now()) +"--"+ str(users_list))
        return users_list
    def __handle_users_premissions_protocol__(self, users_and_premissions):
        """
        convert the premission string to dictionary
        explanation in the word file
        """
        users_and_premissions_dict = {}
        usernames_premissions = users_and_premissions.split('#')
        print usernames_premissions
        for username_premission in usernames_premissions:
            data_user_premission = (username_premission.split(':'))
            username, premission = data_user_premission[0], data_user_premission[1]
            users_and_premissions_dict[username] = (premission)
        users_and_premissions_dict[self.admin_username] = 'A'
        return users_and_premissions_dict
    def get_segements_by_premissions(self,premissions, username):
        """
        according to the user premission -> returns his segs
        """
        print 'loading...', username
        print username, 'premissions are: ', premissions
        segments_names_users = premissions.split('^')
        user_segments = []
        for seg_name in segments_names_users:
            if seg_name in self.segments.keys() and self.segments[seg_name].has_access(username):
                user_segments.append(self.segments[seg_name])
        return user_segments
    def get_seg_dict(self):
        return self.segments
    def getSegments(self, user):
        """
        return the user's segments
        """
        user_segments = [] 
        username = user.get_name()
        for name in self.segments_names:
            command = ('''SELECT users_premissions FROM segments_data WHERE segment_name='''+name[0])
            if [(str(username+":A"),str(username+":W"), str(username+":R"))] in db.getDataFromCloud(self.cloud_dir , command):
                user_segments.append(name)
        return user_segments
    def __create_cloud__(self, dir_name):
        """
        create the database and create the table in it
        """
        if not os.path.isfile(dir_name):
            f = open(dir_name, 'w')
            table_str = ''' CREATE TABLE segments_data(id INTEGER PRIMARY KEY, segment_name TEXT,
                        password TEXT, users_premissions TEXT)'''
            db.create_table(dir_name, table_str)
            f.close()
    def __create_event_log__(self, dir_name):
        """
        create the event_log file
        """
        if not os.path.isfile(dir_name):
            with open(dir_name, 'w') as f:
                db.write_in_log(Cloud.event_log_dir, "cloud created" +str(datetime.datetime.now()))
    def createNewSegment(self, name, users_and_premissions,password):
        """
        add to the database and the objects(cloud, the relevant users) the seg
        """
        new_seg = Segment(self.cloud_dir,name,self.__handle_users_premissions_protocol__(users_and_premissions), password, False)
        self.segments_names.append(name)
        self.segments[name] = (new_seg)
        self.add_seg_to_users(self.__handle_users_premissions_protocol__(users_and_premissions), new_seg)
        db.write_in_log(Cloud.event_log_dir, "seg created--" +str(datetime.datetime.now()) +"--seg name: "+ str(name)+" premissions: "+ str(users_and_premissions))
        return new_seg
        #return None
    def add_seg_to_users(self, users_and_premissions, new_seg):
        """
        add for each user the given seg
        """
        for username in users_and_premissions.keys():
            self.all_users[username].add_seg(new_seg)
    def __load_segments_from_cloud__(self, cloud_dir):
        """
        load from the database all the segments
        """
        segments = {}
        for name in self.segments_names:
            print name
            if name[0] != "segments_data":
                command = ('''SELECT password,users_premissions FROM segments_data WHERE segment_name= "'''+name[0]+ '''"''')
                print command
                password, users_and_premissions = (db.getDataFromCloud(cloud_dir, command)[0])
                users_and_premissions = self.__handle_users_premissions_protocol__(users_and_premissions)
                segments[name[0]] = (Segment(self.cloud_dir,name[0], users_and_premissions, password, True))
        print segments
        db.write_in_log(Cloud.event_log_dir, "segs loaded -" +str(datetime.datetime.now()) +"--"+ str(segments))
        return segments
    def refresh_users(self):
        """
        reload the users data
        """
        new_users = self.__convertDataToObject_USER__(db.loadAllUsers(self.dir_name_login))
        for username in new_users:
            if username in self.all_users.keys():
                self.all_users[username].set_segments(new_users[username].getSegments())
                self.all_users[username].setCondition(new_users[username].getCondition())
            else:
                self.all_users[username] = new_users[username]
        del new_users
    def get_seg_object(self, seg_name):
        """
        return the seg object according his name
        """
        print 'getting seg object'
        if seg_name in self.segments.keys():
            
            return self.segments[seg_name]
        return False
    def move_file(self, user,curr_seg,file_name, next_seg):
        """
        handle moving files to other segs
        """
        try:
            print curr_seg.get_user_premission(user.get_name())
            if curr_seg.__can_change__(user.get_name()) and next_seg.__can_change__(user.get_name()):
                print 'movingggg'
                db.write_in_log(Cloud.event_log_dir, "moving file: " +str(datetime.datetime.now()) +"--"+ file_name+':'+curr_seg.get_name()+'->'+next_seg.get_name())
                #file_id = self.segments[curr_seg.get_name()].get_file_id(file_name)
                if db.move_file_to_another_seg(self.cloud_dir , curr_seg.get_name(), next_seg.get_name(), file_name):
                    next_seg.add_file(user.get_name(),(curr_seg.delete_file(user.get_name(), file_name)))
                    return True
            return False
        except:
            print "failed"
            return False
    def get_user(self, username):
        return self.all_users[username]
    def get_active_users(self):
        self.refresh_users()
        return filter(lambda user: user.getCondition() == 1 , self.all_users.values())
    def get_client(self, username):
        return self.all_users[username]
    def add_user_to_seg(self, username, seg_name, password):
        """
        join the user to the seg
        """
        seg = self.get_seg_object(seg_name)
        if seg:
            print 'adding to seg........'
            if seg.add_user(username, password) and username.add_seg(seg):
                db.write_in_log(Cloud.event_log_dir, "user joined -"+str(user.get_name())+"---"+str(datetime.datetime.now()) +"-- from: "+seg.get_name())
                return True
        return False
    def delete_user_from_seg(self, user, seg):
        """
        delete the user to the seg
        """
        print seg
        print user.getSegments()
        if seg in user.getSegments():
            print 'deletingggg'
            if (seg.delete_user(user.get_name()) and user.delete_seg(seg)):
                db.write_in_log(Cloud.event_log_dir, "user exited -" +str(user.get_name())+"---"+str(datetime.datetime.now()) +"-- from: "+seg.get_name())
                return True
        return False
    def set_user_name(self, username, new_username):
        """
        rename the username
        """
        if db.rename_user(self.dir_name_login ,username, new_username):
            self.all_users[username].set_name(new_username)
            user_segments = self.all_users[username].getSegments()
            for seg in user_segments:
                seg.update_username(username, new_username)
            self.all_users[new_username] = self.all_users[username]
            del self.all_users[username]
            db.write_in_log(Cloud.event_log_dir, "username changed -" +str(user.get_name())+"---"+str(datetime.datetime.now()) +"-- from: "+username+" to: "+new_username)
            return (True, self.all_users[new_username])
        return False
    def change_seg_name(self, seg_object ,username ,password ,new_name):
        """
        handle renaming segments
        """
        last_name = seg_object.get_name()
        if seg_object.change_table_name(username,password,new_name):
            #self.segments_names.remove(last_name)
            #self.segments_names.append(new_name)
            print self.segments_names
            self.segments[new_name] = self.segments[last_name]
            del self.segments[last_name]
            db.write_in_log(Cloud.event_log_dir, "seg name changed--" +str(datetime.datetime.now()) +"--from: "+ str(last_name)+"to: "+ new_name)
            return True
        return False
    def load_data_client(self, user, req):
        """
        return data according the user, req
        """
        print 'sending' , req
        if req == 'Segments':
            print "aaaaaaaaaaa", map(lambda seg: (seg.get_name(),seg.get_seg_files()), user.getSegments())
            return map(lambda seg: (seg.get_name(),seg.get_seg_files()), user.getSegments())
        elif req == 'Premissions':
            #print "yyyyyyyyyyyyyyy", user.getSegments()[0].get_user_premission(user.get_name())
            print map(lambda seg: (seg.get_name(),seg.get_user_premission(user.get_name())), user.getSegments())
            for seg in user.getSegments():
                print seg.get_user_premission(user.get_name())
            return map(lambda seg: (seg.get_name(),seg.get_user_premission(user.get_name())), user.getSegments())
        elif req == 'getEventLog' and user.get_name() == self.admin_username:
            return [Cloud.event_log_dir]
        else:
            return []
    def get_event_log(self,username):
        """
        write the events in the event_log_file
        """
        if username == self.admin_username:
            print 'sending'
            with open(Cloud.event_log_dir, 'r') as f:
                events = f.readlines()
            return events
        else:
            return []
