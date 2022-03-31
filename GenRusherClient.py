import socket
import tkinter as tk
from tkinter import *
from tkinter import messagebox


allname = []
allPassword = []
otpList = []
alphabetUpper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

HEADER = 64
PORT = 5050
PORT2 = 6060
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
ADDR2 = (SERVER, PORT2)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(ADDR2)

        
def config_to_main():
    fill_email.destroy()
    fill_name.destroy()
    fill_otp.destroy()
    e_mail.destroy()
    your_name.destroy()
    otp.destroy()
    confirmPage2.destroy()

    #=======

    pass_word.pack(pady=20)
    button.pack(pady=70)
    fill.place(x=175,y=170)
    textPasscode.place(x=300,y=330, anchor=CENTER)
    textDecode.place(x=300,y=290, anchor=CENTER)


def send():
    if fill.get() == "" or fill.get() == " ":
        messagebox.showinfo("GenRusher", "No Password")
    else:
        pc = fill.get()
        data = fill.get() 
        client.send(data.encode(FORMAT))
        data = client.recv(HEADER).decode(FORMAT)
        submit(data,pc)
        print(f"Data from Server: {data}")
        delete()

def delete():
    fill.delete(0,END)


def submit(data,pc):
    textPasscode.config(text="Encode >> %s"%(data))
    textDecode.config(text="Passcode >> %s"%(pc))

#==================================================   Send OTP Page ===================================#


def email():
    global allname
    global allPassword
    global otpList
    recv_email = fill_email.get()
    name = fill_name.get()
    allname.append(name)


    client2.send(recv_email.encode(FORMAT))
    client2.send(name.encode(FORMAT))
    password = client2.recv(HEADER).decode(FORMAT)
    otp = client2.recv(HEADER).decode(FORMAT)
    otpList.append(otp)
    allPassword.append(password)
    click_confirm()


def click_confirm():
    messagebox.showinfo("GenRusher", "OTP has been send to your Email!")
    e_mail.config(text="Name")
    your_name.config(text="PW")
    otp.place(x=145,y=265)
    fill_otp.place(x=220,y=265)
    confirm.destroy()
    confirmPage2.place(x=250,y=330)
    fill_email.delete(0,END)
    fill_name.delete(0,END)

def check():
    name = fill_email.get()
    pw = fill_name.get()
    otp = fill_otp.get()
    print(allname)
    print(allPassword)
    print(otpList)
    
    if str(name) == str(allname[0]) and str(pw) == str(allPassword[0]) and str(otp) == str(otpList[0]):
        messagebox.showinfo("GenRusher", "Welcome to GenRusher")
        config_to_main()

#==================================================   GUI ===================================#

window = tk.Tk()
window.geometry("600x400")
window['bg'] = 'black'

frame = tk.Frame(master=window,
width=750, height=500, bg="black")
frame.pack()

name = Label(master=frame,text="GenRusher",fg="white",bg="black",font="consolas 40",)
name.pack(pady=15)

pass_word = Label(master=frame, text="Fill in your password",fg="white", bg="black",font = "25")

font = ('Verdana', 15)

fill = Entry(window,font=font,text="")

button = Button(window,font=('Verdana', 12),text="Submit", command = send)

textPasscode = Label(window, text="",fg="white",bg="black",font="consolas 15")


textDecode = Label(window,text="",fg="white",bg="black",font="consolas 15")


e_mail = Label(text="Email",font=('Verdana',15),fg = "white",bg="black",)
e_mail.place(x=145,y=125)


your_name = Label(text="Name",font=('Verdana',15),fg = "white",bg="black",)
your_name.place(x=145,y=195)


fill_email = Entry(text="",font=('Verdana',15),width=20)
fill_email.place(x=220,y=125)


fill_name = Entry(text="",font=('Verdana',15),width=20)
fill_name.place(x=220,y=195)

fill_otp = Entry(text="",font=('Verdana',15),width=20)


confirm = Button(text="Confirm",font=('Verdana',15),height=1, command=email)
confirm.place(x=250,y=280)

confirmPage2 = Button(text="Confirm",font=('Verdana',15),height=1, command=check)

otp = Label(text="OTP",font=('Verdana',15),fg = "white",bg="black",)


window.mainloop()