import sqlite3 as lite
def add_seg_to_data(dir_name, seg_name,users_premissions,password):
    """
    add to the segments data table the seg info
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return 2
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO segments_data(segment_name,password,users_premissions)
                        VALUES(?,?,?)''', (seg_name,password,users_premissions))
            conn.commit()
            conn.close()
    return 1    
def create_table(dir_name, table_str):
    """
    create table in the data base according to the given str
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        sys.exit(1)
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute(table_str)
            print "Created successfully"
            conn.commit()
            conn.close()
def setActive(dir_name ,username, condition):
    """
    set the user condition
    online/offline
    1/0
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return False
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users SET isActive = ? WHERE username = ? ''' ,(condition, username))
            conn.commit()
            conn.close()
def change_user_password(dir_name, username ,new_pass):
    """
    update user password
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return False
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users SET password = ? WHERE username = ? ''' ,(hash(new_pass), username))
            print "changed"
            conn.commit()
            conn.close()
            return True
        return False
def rename_user(dir_name, username, new_username):
    """
    change username in the users database
    """
    if not check_username(dir_name , new_username):
        return False

    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return False
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users SET username = ? WHERE username = ? ''' ,(new_username, username))
            conn.commit()
            conn.close()
            return True
def update_users_premissions(dir_name, last_seg_name, new_name, users):
    """
    update user premission in the database
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return False
    finally:
        if conn:
            cursor = conn.cursor()
            for username in users:
                print 'changing...' , username
                cursor.execute('''SELECT premissions FROM users WHERE username=?''', (username,))
                curr_premissions = cursor.fetchone()[0]
                print curr_premissions
                new_premission_str = curr_premissions.replace("^"+last_seg_name+"^","^"+new_name+"^")
                if new_premission_str == curr_premissions:
                    new_premission_str = curr_premissions.replace("^"+last_seg_name,"^"+new_name)
                cursor.execute('''UPDATE users SET premissions = ?  WHERE username=?''', (new_premission_str , username))
                print 'changed ' , new_premission_str
            conn.commit()
            conn.close()
            return True
def change_name_segment(dir_name, dir_name_login,seg_name, new_name,users):
    """
    change the seg name in the segments data table and then
    update all the seg's users premission according the name change
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return False
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''ALTER TABLE '''+ seg_name +''' RENAME TO ''' + new_name)
            cursor.execute('''UPDATE segments_data SET segment_name = ? WHERE segment_name = ? ''' ,(new_name, seg_name))
            conn.commit()
            conn.close()
            return update_users_premissions(dir_name_login, seg_name, new_name, users)
        return False
def login(dir_name, username, password):
    """
    manage login
    """
    #username, password = collect_msg_data(data_login , False)
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return 2
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT password FROM users WHERE username=?''', (username,))
            password_db = str(cursor.fetchone()[0])
            print (password), password_db
            if password_db != str((password)):
                conn.close()
                return 0
            conn.close()
    setActive(dir_name ,username,1)
    print "%s %s %s login in successfully", (username, password)
    return 1
def check_username(dir_name , username):
    """
    check if the username is exist in the database
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return False
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT id FROM users WHERE username=?''', (username,))
            if (cursor.fetchall()):
                conn.close()
                return False
            conn.close()
            return True
def register(dir_name , username, password, premissions, ip, directory_folder):
    """
    manage register
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return 2
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users(username, password, ip,isActive, premissions, directory_folder)
                        VALUES(?,?,?,1,?,?)''', (username,(password), ip ,premissions, directory_folder))
            print "%s - %s - %s - %s registered in successfully", (username, (password), ip, premissions)
            conn.commit()
            conn.close()
    return 1
def get_seg_files(dir_name, seg_name):
    """
    get list of all the files in the seg
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT file_name, file_extension,size FROM '''+ seg_name)
            files = cursor.fetchall()            
            print "Files of ", seg_name, " ", files
            conn.commit()
            conn.close()
    return files
def add_file(dir_name, file_name, file_extention, file_binary, file_path,seg_name):
    """
    add to the seg the file details
    and write the file in the server folder
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            with open(file_path + file_extention, "wb") as f:
                f.write(file_binary)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO '''+ seg_name +''' (file_name, file_extension, file_directory,size)
                        VALUES(?,?,?,?)''', (file_name, file_extention, file_path, len(file_binary)))
            conn.commit()
            conn.close()
    return True
def delete_file(dir_name, seg_name, file_name):
    """
    delete file from the seg table
    not in the server folder
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM '''+ seg_name +''' WHERE file_name = ?''', (file_name,))
            conn.commit()
            conn.close()
    return True    
def change_name_file(dir_name, seg_name, last_name,new_file_name):
    """
    change file name in the seg table not in the server folder
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE '''+ seg_name +''' SET file_name = ? WHERE file_name = ?''', (new_file_name, last_name))
            conn.commit()
            conn.close()
    return True    
def move_file_to_another_seg(dir_name, curr_seg, next_seg, file_name):
    """
    delete and save the file data in another seg
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO '''+ next_seg +''' SELECT * FROM '''+ curr_seg +''' WHERE file_name = ?''', (file_name,))
            cursor.execute('''DELETE FROM '''+ curr_seg +''' WHERE file_name = ?''', (file_name,))
            conn.commit()
            conn.close()
    return True
def loadSegmentsNames(dir_name):
    """
    load all the segs names
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        sys.exit(1)
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT name FROM sqlite_master WHERE type = "table"''')
            segments_names = cursor.fetchall()
            print segments_names
            print "Created successfully"
            conn.close()
    return segments_names
def getDataFromCloud(dir_name , command):
    """
    according the command, it return the data from the database
    """
    print command
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute(command)
            data = cursor.fetchall()
            conn.close()
    print data
    return data
def loadAllUsers(dir_name_login):
    """
    load from the database all the users data
    """
    try:
        conn = lite.connect(dir_name_login)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return []
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT username, isActive,premissions, directory_folder, ip FROM users''')
            all_users = (cursor.fetchall())
            conn.close()
            return all_users
        return [] 
def update_premissions(dir_name , premisions_str, seg_name):
    """
    update the segments users premissions
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE segments_data SET users_premissions = ? WHERE segment_name = ?''', (premisions_str,seg_name))
            conn.commit()
            conn.close()
    return True    
def add_user_premission(dir_name ,username, seg_name):
    """
    add seg to the user premissions
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT premissions From users WHERE username = ?''',(username,))
            premission_str = cursor.fetchall()[0][0]
            if premission_str != 'ALL':
                new_premission_str = premission_str + "^"+seg_name
                print new_premission_str
                cursor.execute('''UPDATE users SET premissions = ? WHERE username = ?''', (new_premission_str,username))
            conn.commit()
            conn.close()
def update_user_premission(dir_name ,username, new_premission_str):
    """
    update the user premission
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        return False
        print "Error %s:" % dir_name
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users SET premissions = ? WHERE username = ?''', (new_premission_str,username))
            conn.commit()
            conn.close()
            return True
    return False
def delete_seg(dir_name, seg_name):
    """
    delete the seg from the database
    """
    try:
        conn = lite.connect(dir_name)
    except lite.Error, e:
        print "Error %s:" % dir_name
        return None
    finally:
        if conn:
            cursor = conn.cursor()
            cursor.execute('''DROP TABLE ''' +(seg_name))
            cursor.execute('''DELETE FROM segments_data WHERE segment_name = ?''', (seg_name,))
            conn.commit()
            conn.close()
    return True        
def write_in_log(event_log_dir, event):
    """
    write the event in the events log file
    """
    with open(event_log_dir, 'ab') as f:
        f.write(event +'\n')