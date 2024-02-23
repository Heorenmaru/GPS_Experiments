import math
import threading
import time
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import random
# Создание изображения
width = 200
height = 200
image = Image.new("RGB", (width, height), "black")
draw = ImageDraw.Draw(image)

image2 = Image.new("RGB", (width, height), "black")
draw2 = ImageDraw.Draw(image)

c = 0x000000
# Функция для рисования точки по углу и радиусу от центра
def draw_point(angle, radius, r,g,b):
    global c
    angl = math.radians(angle-90)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    # current_color = image.getpixel((x, y)) 


    new_color = tuple([int(r),int(g),int(b)])
    c += 64
    draw.point((x, y), c)
    # draw.point((x, y), new_color)

# Функция для обновления изображения
def update_image():
    an = 0
    rd = 90
    while True:
        if an< 360:
            an += .47
        else: 
            an = 0
            if rd>0:
                rd -= 1
            else:
                rd = 90
        # Рисование точки на случайных координатах
        angle = an
        radius = rd
        draw_point(angle, radius, random.randint(0,255),random.randint(0,255),random.randint(0,255))

        # Обновление изображения в окне Tkinter
        img_tk = ImageTk.PhotoImage(image)
        canvas.itemconfig(canvas_image, image=img_tk)
        canvas.image = img_tk

        # Задержка на 1 секунду
        time.sleep(0.0001)

# Создание окна Tkinter
root = tk.Tk()
root.title("Рисование точек")
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

# Отображение изображения в окне Tkinter
img_tk = ImageTk.PhotoImage(image)
canvas_image = canvas.create_image(0, 0, anchor="nw", image=img_tk)

# Запуск потока для обновления изображения
thread = threading.Thread(target=update_image)
thread.daemon = True
thread.start()

# Запуск главного цикла Tkinter
root.mainloop()
