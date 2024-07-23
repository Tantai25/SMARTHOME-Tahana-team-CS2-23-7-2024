import subprocess
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk  
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()
click_sound = pygame.mixer.Sound('click_sound.mp3')

def login():
    play_sound()
    root.destroy()
    subprocess.run(['python', 'login.py'])

def translate_language(event):
    selected_language = languages_combobox.get()
    showinfo(title="Thông báo", message=f"Nhóm Tahana muốn nói: {selected_language}")

def create_square_canvas(parent, x, y, size, color):
    canvas = Canvas(parent, width=size, height=size, bg='white', highlightthickness=0)
    canvas.place(x=x, y=y)
    canvas.create_rectangle(0, 0, size, size, fill=color)
    return canvas

def play_sound():
    click_sound.play()

root = Tk()
root.title("Đăng nhập")
root.geometry("600x400+650+300")  

A = Image.open('bglogin2.png')
photo = ImageTk.PhotoImage(A)

L1 = Label(root, image=photo)
L1.pack(pady=0)

image = PhotoImage(file='login.png')

title_label = Label(root, bg='White', image=image)
title_label.place(x=410, y=130)

login_button = Button(root, text="Login", bd=2, bg='#735146', fg='White', font=('Times', 15, 'bold'), activeforeground="White", activebackground="#F9C15D", command=login, width=15)
login_button.place(x=355, y=245)

# Language Combobox
languages = ["Thầy Dũng đẹp trai ‧₊✩˚ ⋅ ♱", "愛してる Thầy Dũng cute ⁺‧₊˚ ཐི⋆♱⋆ཋྀ ˚₊‧⁺", "我爱你 Thầy Dũng số 1 lòng em ˚₊‧꒰ა ☆ ໒꒱ ‧₊˚", "사랑해 Thầy Dũng oppa ≽^•༚• ྀི≼ "]

languages_combobox = ttk.Combobox(root, values=languages, height=10)
languages_combobox.place(x=380, y=210)
languages_combobox.set("Mời chọn")  

languages_combobox.bind("<<ComboboxSelected>>", translate_language)

# Update window to get accurate dimensions
root.update_idletasks()

# Create four canvases for squares
size = 20
# Adjust positions to make sure squares are flush against the window edges
create_square_canvas(root, size, size, size, '#735146')  # Top-left corner
create_square_canvas(root, root.winfo_width() - size*2, size, size, '#735146')  # Top-right corner
create_square_canvas(root, size, root.winfo_height() - size*2, size, '#735146')  # Bottom-left corner
create_square_canvas(root, root.winfo_width() - size*2, root.winfo_height() - size*2, size, '#735146')  # Bottom-right corner

root.mainloop()
