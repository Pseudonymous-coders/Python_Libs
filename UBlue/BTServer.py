import bluetooth, subprocess, sys
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
data = "Blank"
port = bluetooth.PORT_ANY


def query(command):
    try:
        output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  shell=True, executable='/bin/bash', close_fds=True).communicate()
        standard = output[0]
        output = standard
    except Exception:
        output = "Unknown"
    return output

server_sock.bind(("", port))
server_sock.listen(1)
print "listening on port %d" % port

bluetooth.advertise_service(server_sock, "FooBar", uuid)
client_sock, address = server_sock.accept()
print "Accepted connection from ", address

while 1:
    try:
        while data:
            print "Command: "+data
            data = client_sock.recv(4096)
            if data == "q":
                client_sock.send("%%EXIT%%")
#            if data[:3] is "cd":

            else:
                output = query(data)
                print "Output: "+output
                print "Sending output"
                client_sock.send("\n"+output)


    except Exception:
        print "Closing connection with ", address
        print "\nlistening on port %d" % port
        data = "Blank"
        client_sock, address = server_sock.accept()
        print "Accepted connection from ", address


client_sock.close()
server_sock.close()
