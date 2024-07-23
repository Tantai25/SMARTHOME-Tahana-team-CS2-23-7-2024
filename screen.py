import subprocess
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import pygame
import os
global s1
import serial
# try:
#     s1 = serial.Serial('COM6', baudrate=9600, timeout=1)
#     print("Connected to COM6")
# except serial.SerialException as e:
#     print(f"Failed to connect to COM6: {e}")

music_playing = False

pygame.mixer.init()
click_sound = pygame.mixer.Sound('click_sound.mp3')

def play_sound():
    click_sound.play()

def home():
    play_sound()
    showinfo(title="Thông báo bé nhỏ dành cho bạn", message="⋆⭒˚.⋆お帰りなさいいい☆⋆｡𖦹°‧★")
    update_music_state()
    root.destroy()
    subprocess.run(['python', 'home.py'])

def start_music():
    global music_playing
    if not music_playing:
        pygame.mixer.music.play(-1)  # Play the music indefinitely
        music_playing = True

def stop_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False

def update_music_state():
    with open("cafe.txt", "w") as file:
        file.write("playing" if music_playing else "stopped")

def check_music_state():
    global music_playing
    if os.path.exists("cafe.txt"):
        with open("cafe.txt", "r") as file:
            state = file.read()
            if state == "playing":
                start_music()
            else:
                stop_music()

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("cafe.mp3")

root = Tk()
root.title("HI")
root.geometry("600x400+650+300")

A = Image.open('bg1.png')
photo = ImageTk.PhotoImage(A)

login_button = Button(root, image=photo, command=home, width=600, height=400)
login_button.place(x=0, y=0)

check_music_state()
start_music()  # Start the music automatically
root.mainloop()
