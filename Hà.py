# pip install openpyxl
# pip install speechrecognition pyaudio

import speech_recognition as sr
from tkinter import *
from tkinter.messagebox import showwarning, showinfo
from openpyxl import Workbook
from PIL import Image, ImageTk
import pygame
import serial
import os
import subprocess
import time
import sys
import threading
import queue
import openpyxl
import smtplib
import zipfile
from email.mime.text import MIMEText

# Initialize Pygame mixer
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm.mp3")
alarm_sound.set_volume(1.0)
click_sound = pygame.mixer.Sound('click_sound.mp3')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Initialize serial connection
try:
    s1 = serial.Serial('COM6', baudrate=9600, timeout=1)
    print("Connected to COM6")
except serial.SerialException as e:
    print(f"Failed to connect to COM6: {e}")

# Initialize notebook for logging
log_file = "home_automation_log.xlsx"


# Global states
gate_state = False
light_state = False
fan_state = False
door_state = False
garage_light_state = False
cua_cuon_state = False
current_bg_key = "Off"
fire_alert_active = False
music_playing = False
alarm_playing = False
bedroom_light_state = False
bedroom_frame_visible = False

# Background images
background_images = {
    "Off": "Ha1.png",
    "On": "lvr_light.png",
    "Fan_on": "lvr_fan.png",
    "Door_open": "lvr_door.png",
    "Garage_on": "gr_light.png",
    "Cua_len": "gr_cua_cuon.png",
    "Big_gate_open": "big_gate.png"
}

# Hàng đợi cho các lệnh thoại
command_queue = queue.Queue()


def play_sound():
    click_sound.play()

def send_fire_alert_email():
    sender_email = "smarthome.tahana@gmail.com"
    sender_password = "kdii qmjs eqlp mjth"
    receiver_email = "dinhvantan2725@gmail.com"
    subject = "Cảnh báo cháy"
    body = "Cảnh báo: Hệ thống đã phát hiện nhiệt độ quá cao, có thể có nguy cơ cháy. Vui lòng kiểm tra ngay lập tức."

    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def log_event(event, detail="", temperature=None):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        wb = openpyxl.load_workbook(log_file)
        ws = wb.active
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"File error: {e}. Creating a new log file.")
        wb = Workbook()
        ws = wb.active
        ws.title = "Logs"
        ws.append(["Thời gian", "Sự kiện", "Chi tiết", "Nhiệt độ"])
    
    ws.append([timestamp, event, detail, temperature])
    wb.save(log_file)


def change_background(option):
    global current_bg_key
    current_bg_key = option
    image_path = background_images[option]
    load_new_background(image_path)

def load_new_background(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    L1.config(image=photo)
    L1.image = photo

def update_background():
    if fire_alert_active:
        change_background("Off")
    elif light_state:
        change_background("On")
    elif fan_state:
        change_background("Fan_on")
    elif door_state:
        change_background("Door_open")
    elif garage_light_state:
        change_background("Garage_on")
    elif cua_cuon_state:
        change_background("Cua_len")
    elif gate_state:
        change_background("Big_gate_open")
    else:
        change_background("Off")

def reset_color():
    button1.config(bg='white')
    buttonx.config(bg='white')
    button2.config(bg='white')
    buttony.config(bg='white')
    button3.config(bg='white')
    buttonz.config(bg='white')
    button4.config(bg='white')
    buttonh.config(bg='white')
    button5.config(bg='white')
    buttonk.config(bg='white')
    buttona.config(bg='white')
    buttont.config(bg='white')

# In mỗi hàm, gọi hàm log_event() để ghi lại sự kiện và chi tiết.

def fan_toggle():
    global s1, fan_state
    button2.config(bg='#72AED6')
    buttony.config(bg='#72AED6')
    play_sound()
    try:
        if fan_state:
            s1.write(b"5")
            print("Turning off the fan")
            fan_state = False
            button2.config(text="Quạt tắt")
            log_event("Fan Toggle", "Turning off the fan")
        else:
            s1.write(b"4")
            print("Turning on the fan")
            fan_state = True
            button2.config(text="Quạt bật")
            log_event("Fan Toggle", "Turning on the fan")
        update_background()
    except Exception as e:
        showwarning(title="Error", message=f"Error: {str(e)}")
        log_event("Error", str(e))
    root.after(300, reset_color)

def door_toggle():
    global s1, door_state
    button3.config(bg='#72D673')
    buttonz.config(bg='#72D673')
    play_sound()
    try:
        if door_state:
            s1.write(b"7")
            print("Closing the door")
            door_state = False
            button3.config(text="Cửa đóng")
            log_event("Door Toggle", "Closing the door")
        else:
            s1.write(b"6")
            print("Opening the door")
            door_state = True
            button3.config(text="Cửa mở")
            log_event("Door Toggle", "Opening the door")
        update_background()
    except Exception as e:
        showwarning(title="Error", message=f"Error: {str(e)}")
        log_event("Error", str(e))
    root.after(300, reset_color)

def livingroom_light_toggle():
    global s1, light_state
    button1.config(bg='#FFEC6A')
    buttonx.config(bg='#FFEC6A')
    play_sound()
    try:
        if light_state:
            s1.write(b"0")
            print("Turning off the light")
            light_state = False
            button1.config(text="Đèn khách tắt")
            log_event("Light Toggle", "Turning off the living room light")
        else:
            s1.write(b"1")
            print("Turning on the light")
            light_state = True
            button1.config(text="Đèn khách bật")
            log_event("Light Toggle", "Turning on the living room light")
        update_background()
    except Exception as e:
        showwarning(title="Error", message=f"Error: {str(e)}")
        log_event("Error", str(e))
    root.after(300, reset_color)


def garage_light_toggle():
    global s1, garage_light_state
    button4.config(bg='#FFEC6A')
    buttonh.config(bg='#FFEC6A')
    play_sound()
    try:
        if garage_light_state:
            print("Turning off the garage light")
            garage_light_state = False
            button4.config(text="Đèn garage tắt")
            s1.write(b"3")
            log_event("Garage Light Toggle", "Turning off the garage light")
        else:
            print("Turning on the garage light")
            garage_light_state = True
            button4.config(text="Đèn garage bật")
            s1.write(b"2")
            log_event("Garage Light Toggle", "Turning on the garage light")
        update_background()
    except Exception as e:
        showwarning(title="Error", message=f"Error: {str(e)}")
        log_event("Error", str(e))
    root.after(300, reset_color)

def cua_cuon():
    global s1, cua_cuon_state
    button5.config(bg='#FD87B5')
    buttonk.config(bg='#FD87B5')
    play_sound()
    try:
        if cua_cuon_state:
            print("Closing the door")
            cua_cuon_state = False
            button5.config(text="Mở cửa")
            s1.write(b"9")
            log_event("Cua Cuon", "Closing the rolling door")
        else:
            print("Opening the door")
            cua_cuon_state = True
            button5.config(text="Đóng cửa")
            s1.write(b"8")
            log_event("Cua Cuon", "Opening the rolling door")
        update_background()
    except Exception as e:
        showwarning(title="Error", message=f"Error: {str(e)}")
        log_event("Error", str(e))
    root.after(300, reset_color)

def start_alarm():
    global alarm_playing
    if not alarm_playing:
        alarm_sound.play(-1)  # Play the alarm indefinitely
        alarm_playing = True
        log_event("Alarm", "Alarm started")

def stop_alarm():
    global alarm_playing
    if alarm_playing:
        alarm_sound.stop()
        alarm_playing = False
        log_event("Alarm", "Alarm stopped")


def nhietdo():
    try:
        data = s1.readline().decode('utf-8', errors='ignore').strip()
        print(f"Data received: {data}")
        if data.startswith("Temperature: "):
            try:
                temp = float(data.split(": ")[1][:-2])
            except ValueError:
                print(f"Invalid temperature value: {data}")
                return
            print(f"Nhiệt độ nhận được: {temp:.2f} C")
            temp_label.config(text=f"Nhiệt độ: {temp:.2f} C")
            handle_temperature(temp)
        elif data in ["QUẠT ĐÃ BẬT", "QUẠT ĐÃ TẮT"]:
            print(f"Received relay status: {data}")
            status_label.config(text=f"Trạng thái quạt: {data}")
    except UnicodeDecodeError:
        print("Received non-UTF-8 data, skipping...")
    root.after(1000, nhietdo)


def handle_temperature(temp):
    global fire_alert_active
    log_event("Cập nhật nhiệt độ", f"Nhiệt độ nhận được: {temp:.2f} C", temperature=temp)
    if temp > 31 and not fire_alert_active:
        start_alarm()
        send_fire_alert_email()
        showwarning(title="Cảnh báo cháy", message="Cảnh báo quá nhiệt. Các cửa đã được mở và các bạn cần chạy ra ngoài để đảm bảo sự an toàn")
        fire_alert_active = True
        change_background("Off")
    elif temp <= 30 and fire_alert_active:
        showinfo(title="An toàn", message="Đám cháy đã được kiểm soát. Bạn đã an toàn. Các cửa sẽ đóng lại sau 1 giây")
        root.after(1000, close_all_doors)
        fire_alert_active = False
        stop_alarm()
        update_background()
    elif temp > 28:
        change_background("Fan_on")
    else:
        update_background()


def close_all_doors():
    global s1
    try:
        print("Đang gửi lệnh đóng tất cả các cửa")
        s1.write(b"7")
        s1.write(b"9")
        s1.write(b"b")
        print("Tất cả các cửa và cổng đã được đóng")
    except Exception as e:
        showwarning(title="Lỗi", message=f"Lỗi: {str(e)}")

def biggate():
    global s1, gate_state
    buttona.config(bg='#FF6A6A')
    buttont.config(bg='#FF6A6A')
    play_sound()
    try:
        if gate_state:
            s1.write(b"b")
            print("Closing the gate")
            gate_state = False
            buttona.config(image=imagea)
            change_background("Off")
        else:
            s1.write(b"a")
            print("Opening the gate")
            gate_state = True
            buttona.config(image=imageb)
            change_background("Big_gate_open")
    except Exception as e:
        showwarning(title="Error", message=f"Error: {str(e)}")
    root.after(100, reset_color)

def quaylai():
    play_sound()
    root.destroy()
    subprocess.run(['python', 'login.py'])
    

def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)  # Cân chỉnh tiếng ồn xung quanh
        while True:
            try:
                audio = recognizer.listen(source, timeout=10)  # Giảm thời gian chờ
                command = recognizer.recognize_google(audio, language="vi-VN")
                print(f"Command recognized: {command}")
                command = command.lower().replace(' ', '')
                command_queue.put(command)  # Put command into the queue
            except sr.UnknownValueError:
                pass  # Không làm gì nếu không nhận diện được lệnh
            except sr.RequestError as e:
                print(f"Could not request results; {e}")


def process_command(command):
    if "đènkhách" in command:
        livingroom_light_toggle()
    elif "máylạnh" in command:
        fan_toggle()
    elif "cửachính" in command:
        door_toggle()
    elif "đèngara" in command:
        garage_light_toggle()
    elif "cửacuốn" in command:
        cua_cuon()
    elif "cổngtrước" in command:
        biggate()
    elif "quaylại" in command:
        quaylai()
    else:
        print("Command not recognized")


def command_processor_loop():
    while True:
        try:
            command = command_queue.get(timeout=0.1)  # Thay vì get_nowait, sử dụng get với timeout nhỏ
            process_command(command)
        except queue.Empty:
            continue  # Không cần sleep khi không có lệnh

# Initialize the Tkinter root
root = Tk()
root.title("Chọn nhà")
root.geometry("600x400+650+300")

# Load images for buttons and background
image1 = PhotoImage(file='idea.png')
image2 = PhotoImage(file='fan.png')
image3 = PhotoImage(file='door.png')
image4 = PhotoImage(file='gdoor.png')
imagea = PhotoImage(file='biggate.png')
imageb = PhotoImage(file='biggate2.png')
imagec = PhotoImage(file='return2.png')

initial_image_path = 'Ha1.png'
image = Image.open(initial_image_path)
photo = ImageTk.PhotoImage(image)
L1 = Label(root, image=photo)
L1.pack(pady=0)

# Create buttons and place them in the window
button1 = Button(image=image1, bg="white", activebackground="#FFEC6A", command=livingroom_light_toggle)
button1.place(x=498, y=201)
button2 = Button(image=image2, bg="white", activebackground="#72AED6", command=fan_toggle)
button2.place(x=315, y=190)
button3 = Button(image=image3, bg="white", activebackground="#72D673", command=door_toggle)
button3.place(x=347, y=310)
button4 = Button(image=image1, bg="white", activebackground="#FFEC6A", command=garage_light_toggle)
button4.place(x=315, y=115)
button5 = Button(image=image4, bg="white", activebackground="#FD87B5", command=cua_cuon)
button5.place(x=121, y=164)

buttona = Button(image=imagea, bg="white", activebackground="#FF6A6A", command=biggate)
buttona.place(x=168, y=342)
buttonb = Button(image=imagec, bd=5, bg="#FBF3E3", activebackground="#6AC0FF", command=quaylai)
buttonb.place(x=0, y=0)

buttonx = Button(bg="white", width=2)
buttonx.place(x=537, y=15)
buttony = Button(bg="white", width=2)
buttony.place(x=499, y=70)
buttonz = Button(bg="white", width=2)
buttonz.place(x=537, y=110)
buttonh = Button(bg="white", width=2)
buttonh.place(x=455, y=15)
buttonk = Button(bg="white", width=2)
buttonk.place(x=455, y=95)
buttont = Button(bg="white", width=2)
buttont.place(x=486, y=120)

label1 = Label(root, text="Hà", bg="#FFE5B0", font=("Times", 40, 'bold'))
label1.place(x=270, y=10)

temp_label = Label(root, text="Nhiệt độ: ", bg="#907760",font=("Times", 12, 'bold'))
temp_label.place(x=5, y=350)

status_label = Label(root, text="Trạng thái: ", bg="#907760",font=("Times", 12, 'bold'))
status_label.place(x=5, y=370)

# Start the temperature and relay status update loop
root.after(2000, nhietdo)

# Start listening for voice commands in a separate thread
voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
voice_thread.start()

# Start processing voice commands in a separate thread
command_processor_thread = threading.Thread(target=command_processor_loop, daemon=True)
command_processor_thread.start()

root.mainloop()

       
