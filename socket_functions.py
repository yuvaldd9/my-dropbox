

"""
while 1:
    data = raw_input("---->")
    if not data: break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZ)
    print data
    if data[0] == '*':
        break
tcpCliSock.close()
#login/register - end
tcpCliSock = socket(AF_INET , SOCK_STREAM)
#sock = ssl.wrap_socket(tcpCliSock)
tcpCliSock.connect(('10.0.0.5', 50011))
while 1:
    data = raw_input("---->")
    if not data: break
    req_details = data.split('^')
    if req_details[0] == 'download':
        tcpCliSock.send(data)
        tcpCliSock.send("done...")
        buff = ''
        data = tcpCliSock.recv(BUFSIZ)
        while not "done..." in data:
            print data,
            buff += data
            data = tcpCliSock.recv(BUFSIZ)
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

    elif req_details[0] =='add':
        socket_functions.send_file(tcpCliSock, req_details[2], BUFSIZ, data)
    else:
        print data 
        tcpCliSock.send(data)
        tcpCliSock.send("done...")
        data = tcpCliSock.recv(BUFSIZ)
        print 'sent'
    print data
print "done"
"""

def recive_file(sock, path, BUFFER_SIZE):
    try:
        bin_next = ''
        data = sock.recv(BUFFER_SIZE)
        f = open(filename, 'wb')
        while not "done..." in data:
            bin_next = sock.recv(BUFFER_SIZE)
            data += bin_next
        data += bin_next[:bin_next.index("done...")]
        f.write(data)
        return True
    except:
        print "failed open/write the file"
        return False