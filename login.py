import subprocess
from tkinter import *
from tkinter.messagebox import showwarning
from PIL import Image, ImageTk
import pygame
import smtplib
from email.mime.text import MIMEText

# Initialize Pygame for sound effects
pygame.mixer.init()
click_sound = pygame.mixer.Sound('click_sound.mp3')

# Create the main window
root = Tk()
root.title("Login")
root.geometry("600x400+650+300")

# Load and display background image
A = Image.open('login2.png')
photo = ImageTk.PhotoImage(A)
L1 = Label(root, image=photo)
L1.pack(pady=0)

# Load and set the return button image
image3 = PhotoImage(file='return.png')

failed_attempts = 0

def login():
    global failed_attempts
    uid = En1.get()
    pw = En2.get()
    play_sound()
    if uid not in acc:
        showwarning(title="Warning", message="Username does not exist")
        failed_attempts += 1
    else:
        if pw == acc[uid]:
            root.destroy()
            if uid == "Tai":
                subprocess.run(['python', 'Tài.py'])
            elif uid == "Ha":
                subprocess.run(['python', 'Hà.py'])
            else:
                subprocess.run(['python', 'Nam.py'])
            failed_attempts = 0  # Reset failed attempts on successful login
        else:
            showwarning(title="Warning", message="Incorrect password")
            failed_attempts += 1

    if failed_attempts >= 2:
        send_email_alert()
        root.after(2000, root.destroy)  # Automatically close the window after 2 seconds
        showwarning(title="Warning", message="Bạn đã đăng nhập sai quá nhiều lần.\n Ứng dụng sẽ tự tắt sau 2 giây.")
        
def play_sound():
    click_sound.play()

def quay_lai():
    play_sound()
    root.destroy()
    subprocess.run(['python', 'home.py'])

def send_email_alert():
    # Email configuration
    sender_email = "smarthome.tahana@gmail.com"
    sender_password = "kdii qmjs eqlp mjth"
    receiver_email = "dinhvantan2725@gmail.com"
    subject = "Cảnh báo bảo mật: Nhiều lần đăng nhập thất bại"
    body = "Cảnh báo: Đã có nhiều lần đăng nhập thất bại trên hệ thống của bạn. Vui lòng kiểm tra để phát hiện bất kỳ truy cập trái phép nào."

    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

acc = {"Tai": "1", "Ha": "1", "Nam": "1"}

# Create and place the entry fields
En1 = Entry(font='Times 17', justify='center')
En1.place(x=189, y=185)
En2 = Entry(font='Times 17', show="*", justify='center')
En2.place(x=189, y=237)

# Create and place the login button
B1 = Button(root, text="Login", bg='#3B3A3C', bd=5, fg='White', activeforeground="#3B3A3C",
            activebackground="white", font=('Times', 14, 'bold'), command=login, width=13)
B1.place(x=225, y=285)

# Create and place the return button
B2 = Button(image=image3, bg="White", command=quay_lai)
B2.place(x=0, y=0)

# Function to create tooltip
def create_tooltip(widget, text):
    tooltip = Label(root, text=text, background="lightyellow", relief="solid", borderwidth=1, padx=5, pady=5)
    tooltip.place_forget()

    def enter(event):
        tooltip.place(x=widget.winfo_x() + widget.winfo_width() // 2 - tooltip.winfo_width() // 2,
                      y=widget.winfo_y() + widget.winfo_height() + 10)

    def leave(event):
        tooltip.place_forget()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# Create tooltips for entry fields
create_tooltip(En1, "Nhập tên tài khoản vào đây")
create_tooltip(En2, "Nhập mật khẩu vào đây")

root.bind("<Return>", lambda dummy: login())

root.mainloop()
