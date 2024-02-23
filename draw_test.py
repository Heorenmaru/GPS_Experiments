import math
import threading
import time
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import random

# Создание изображения
width = 200
height = 200

image1 = Image.new("RGB", (width, height), "black")
draw1 = ImageDraw.Draw(image1)

image2 = Image.new("RGB", (width, height), "black")
draw2 = ImageDraw.Draw(image2)

image3 = Image.new("RGB", (width, height), "black")
draw3 = ImageDraw.Draw(image3)


# Функция для рисования точки по углу и радиусу от центра
def draw_point(image, draw, angle, radius, r,g,b):
    angl = math.radians(angle)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    current_color = image.getpixel((x, y))
    draw.point((x, y), tuple([r,g,b]))

def draw_point2(image, angle, radius, brightness_factor):
    angl = math.radians(angle)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    current_color = image.getpixel((x, y))
    new_color = tuple(min(255, int(value * brightness_factor)) for value in current_color)
    image.putpixel((x, y), new_color)

# Функция для обновления изображения
def update_image():
    an = 0
    rad = 90 
    cr = 255
    cg = 255
    cb = 255
    while True:
        if an>360:
            an = 0
            rad = rad - 1
            if rad <0:
                rad = 90
        # Рисование точки на случайных координатах
        #angle = random.randint(0,359)
        #radius = random.randint(0,90)
        an +=.5
        angle = an
        radius = rad
        draw_point(image1,draw1,angle, radius ,cr,cg,cb)
        draw_point(image2,draw2,angle, radius ,cr,cg,cb)
        draw_point(image3,draw3,angle, radius ,cr,cg,cb)

        # Обновление изображения в окне Tkinter
        img_tk1 = ImageTk.PhotoImage(image1)
        canvas1.itemconfig(canvas_image1, image=img_tk1)
        canvas1.image = img_tk1


        img_tk2 = ImageTk.PhotoImage(image2)
        canvas2.itemconfig(canvas_image2, image=img_tk2)
        canvas2.image = img_tk2

        img_tk3 = ImageTk.PhotoImage(image3)
        canvas3.itemconfig(canvas_image3, image=img_tk3)
        canvas3.image = img_tk3
        
        

        
        

        
        # Задержка на 1 секунду
        time.sleep(.0001)

# Создание окна Tkinter
root = tk.Tk()
root.title("Рисование точек")
canvas1 = tk.Canvas(root, width=width, height=height)
canvas2 = tk.Canvas(root, width=width, height=height)
canvas3 = tk.Canvas(root, width=width, height=height)
canvas1.pack()
canvas2.pack()
canvas3.pack()

# Отображение изображения в окне Tkinter
img_tk1 = ImageTk.PhotoImage(image1)
canvas_image1 = canvas1.create_image(0, 0, anchor="nw", image=img_tk1)

img_tk2 = ImageTk.PhotoImage(image2)
canvas_image2 = canvas2.create_image(0, 0, anchor="nw", image=img_tk2)

img_tk3 = ImageTk.PhotoImage(image3)
canvas_image3 = canvas3.create_image(0, 0, anchor="nw", image=img_tk3)

# Запуск потока для обновления изображения
thread = threading.Thread(target=update_image)
thread.daemon = True
thread.start()

# Запуск главного цикла Tkinter
root.mainloop()
