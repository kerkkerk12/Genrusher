import socket
import threading
import string
import random
import smtplib
import array


HEADER = 64
PORT = 5050
PORT2 = 6060
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
ADDR2 = (SERVER, PORT2)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
changeInt = 0
changeStr = ""
total = 0
passcode = []
encodeList = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(FAMILY, TYPE)
server.bind(ADDR)
server.listen(1)
server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(FAMILY, TYPE)
server1.bind(ADDR2)
server1.listen(1)

def handle_client(conn2, addr2): #run in each client
    print(f"[NEW CONNECTION] {addr2} connected." )
    while True:
        #รับข้อมูลจาก Client
        data = conn2.recv(1024).decode('utf-8')
        addPassword(data.lower())

        if not data:
            print("No Data!")
            break
        
        print("Message From Client :", data)

        encode(passcode,conn2)
        passcode.clear()
        encodeList.clear()
    conn2.close()

def encode(passcode, client):
    code55 = ""
    for i in range(len(passcode)):
        if passcode[i] in number:
            changeInt = int(passcode[i])
            if changeInt % 2 == 0:  #Even
                total = changeInt * random.randint(5,9)
            else:                   #Odd
                total = changeInt + random.randint(0,4)
            changeStr = str(total)
            encodeList.append(changeStr)
            ranNum = random.randint(1,3)
            if ranNum == 3:
                ranAl = random.choice(string.ascii_letters)
                encodeList.append(ranAl)
            total *= 0
            changeInt *= 0
            changeStr = ""
            
        elif passcode[i] in alphabet:
            ran_alphabetU = random.choice(string.ascii_letters)
            ran_alphabetL = ran_alphabetU.lower()
            ranNum = random.randint(0,2)
            ranNumV2 = random.randint(0,5)
            if ranNumV2 == 2:
                x = ran_alphabetL.upper() 
                encodeList.append(x)
            elif ranNum == 1:
                encodeList.append(str(random.randint(0,9)))
            elif True:
                encodeList.append(ran_alphabetL)
        
    for i in encodeList:
        code55 += i
    
    print(*encodeList,sep="")
    client.send(code55.encode('utf-8')) #ส่งข้อมูลกลับไปที่ Client

def addPassword(data):
    for i in data:
        passcode.append(i)

#===========================================================

def email(conn1, addr1):
    print(f"[NEW CONNECTION] {addr1} connected." )

    while True:
        #รับข้อมูลจาก Client
        recv_email = conn1.recv(1024).decode('utf-8')
        name = conn1.recv(1024).decode('utf-8')

        if not recv_email:
            if not name:
                print("No Data!")
                break
        global allName
        sender_email = "authenticatec@gmail.com"
        sender_password = "aabbcc112233"

        otp = ''.join([str(random.randint(0,9)) for i in range(4)])
        returned_password = password(conn1)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        subject = "OTP Authentication (GenRusher)"
        body = f"Authentication OTP of {str(name)} is {str(otp)}\n and your password is {str(returned_password)} "
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(sender_email, recv_email, message)
        print("Email has been sent to ", recv_email)
        conn1.send(otp.encode('utf-8'))
        
    conn1.close()
    return otp

def password(conn1):
    global allPassword
    MAX_LEN = 12
 

    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    

        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    password = ""
    for x in temp_pass_list:
            password = password + x
            

    conn1.send(password.encode('utf-8'))
    return password

#====================================================




def start():
    server.listen()
    server1.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn2, addr2 = server.accept()
    conn1, addr1 = server1.accept()
    thread1 = threading.Thread(target=email, args=(conn1, addr1))
    thread2 = threading.Thread(target=handle_client, args=(conn2, addr2,))
    thread1.start()
    thread2.start()



print("[STARTING] server is starting...")
start()
