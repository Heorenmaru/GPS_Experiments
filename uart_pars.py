#########
# Autor: Heorenmaru
# License: CC-BY-SA
#########

import serial #pyserial
import serial.tools.list_ports
import math
from threading import Thread
from numpy import int32, uint32, uint8, int8, uint64
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import threading
import sys
import os
#go to file directory
try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

##################################################
#   conf
##################################################
port = 'COM7'
baud = 115200


# Создание изображения
width = 200
height = 200

image1 = Image.new("RGB", (width, height), "black")
draw1 = ImageDraw.Draw(image1)

image2 = Image.new("RGB", (width, height), "black")
draw2 = ImageDraw.Draw(image2)

image3 = Image.new("RGB", (width, height), "black")
draw3 = ImageDraw.Draw(image3)


def iron_gradient(value):
    """
    Функция для перевода числа в цвет RGB, согласно тепловому градиенту "iron".
    :param value: число от 0 до 1
    :return: кортеж (R, G, B) с цветом в формате RGB
    """
    if value < 0:
        value = 0
    elif value > 1:
        value = 1

    # Определение цвета в зависимости от значения
    if value < 0.2:
        r = 0
        g = 0
        b = int(255 * value / 0.2)
    elif value < 0.4:
        r = 0
        g = int(255 * (value - 0.2) / 0.2)
        b = 255
    elif value < 0.6:
        r = int(255 * (value - 0.4) / 0.2)
        g = 0
        b = 255
    elif value < 0.8:
        r = 255
        g = int(255 * (value - 0.6) / 0.2)
        b = 0
    else:
        r = 255
        g = 255
        b = int(255 * (1 - value) / 0.2)

    return tuple([r, g, b])



def draw_sat(image, draw, angle, radius, r,g,b):
    angl = math.radians(angle-90)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    current_color = image.getpixel((x, y))
    draw.point((x, y), tuple([r,g,b]))


# Функция для рисования точки по углу и радиусу от центра
    
def draw_point_iron(image, draw, angle, radius, c):
    angl = math.radians(angle-90)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    current_color = image.getpixel((x, y))
    t =  iron_gradient(c)
    draw.point((x, y), iron_gradient(c))

def draw_point_direct(image, draw, angle, radius, r,g,b):
    angl = math.radians(angle-90)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    current_color = image.getpixel((x, y))
    draw.point((x, y), tuple([r,g,b]))

def draw_point(image, draw, angle, radius, cr,cg,cb):
    angl = math.radians(angle-90)
    x = int(width / 2 + radius * math.cos(angl))
    y = int(height / 2 + radius * math.sin(angl))
    current_color = image.getpixel((x, y)) 
    r = 0
    g = 0
    b = 0
    if cr >0:
        r = current_color[0]+1
    else:
        r = current_color[0]

    if cg >0:
        g = current_color[1]+1
    else:
        g = current_color[1]

    if cb >0:
        b = current_color[2]+1
    else:
        b = current_color[2]

    if(r>255):
        r = 255
    if(g>255):
        g = 255
    if(b>255):
        b = 255
    new_color = tuple([int(r),int(g),int(b)])
    draw.point((x, y), new_color)

# def draw_point2(angle, radius, brightness_factor):
#     x = int(width / 2 + radius * math.cos(angle))
#     y = int(height / 2 + radius * math.sin(angle))
#     current_color = image.getpixel((x, y))
#     new_color = tuple(min(255, int(value * brightness_factor)) for value in current_color)
#     image.putpixel((x, y), new_color)


# Функция для обновления изображения
def gps_read():
    while True:
        
        
        ser = serial.Serial(port, baud)
        while True:
            try:
                line = ser.readline().decode('utf-8')
                try:
                    f = open('nmea.log','a')
                    f.write(line)
                except Exception as e:
                    print(f'nmea save error: {e}')


                if "GSV" in line:
                    print(line.rstrip('\n'))
                    

                    try:
                        fields = line.split(',')
                        # SAT 1
                        try:
                            sat1 = fields[4:]

                            satid = int(sat1[0]),
                            elevation = int(sat1[1]),
                            azimuth = int(sat1[2]),
                            snr = -1
                            try:
                                snr = int(sat1[3])
                            except:
                                pass
                            
                            # Рисование точки 
                            angle = azimuth[0]
                            radius = 90-elevation[0]

                            if 'GP' in line:
                                draw_point(image1,draw1, angle, radius, 0,1,0)
                                if snr>=0:
                                    #draw_point_direct(image2,draw2,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image2,draw2,angle, radius ,(snr/100) )
                            if 'GL' in line:
                                draw_point(image1,draw1, angle, radius, 1,0,0)
                                if snr>=0:
                                    #draw_point_direct(image3,draw3,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image3,draw3,angle, radius ,(snr/100) )
                        except:
                            pass
                        # SAT 2
                        try:
                            sat2 = fields[8:]

                            satid = int(sat2[0]),
                            elevation = int(sat2[1]),
                            azimuth = int(sat2[2]),
                            snr = -1
                            try:
                                snr = int(sat1[3])
                            except:
                                pass
                            
                            # Рисование точки 
                            angle = azimuth[0]
                            radius = 90-elevation[0]

                            if 'GP' in line:
                                draw_point(image1,draw1, angle, radius, 0,1,0)
                                if snr>=0:
                                    #draw_point_direct(image2,draw2,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image2,draw2,angle, radius ,(snr/100) )
                            if 'GL' in line:
                                draw_point(image1,draw1, angle, radius, 1,0,0)
                                if snr>=0:
                                    #draw_point_direct(image3,draw3,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image3,draw3,angle, radius ,(snr/100) )
                        except:
                            pass
                        # SAT 3
                        try:
                            sat3 = fields[12:]

                            satid = int(sat3[0]),
                            elevation = int(sat3[1]),
                            azimuth = int(sat3[2]),
                            snr = -1
                            try:
                                snr = int(sat1[3])
                            except:
                                pass
                            
                            # Рисование точки 
                            angle = azimuth[0]
                            radius = 90-elevation[0]

                            if 'GP' in line:
                                draw_point(image1,draw1, angle, radius, 0,1,0)
                                if snr>=0:
                                    #draw_point_direct(image2,draw2,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image2,draw2,angle, radius ,(snr/100) )
                            if 'GL' in line:
                                draw_point(image1,draw1, angle, radius, 1,0,0)
                                if snr>=0:
                                    #draw_point_direct(image3,draw3,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image3,draw3,angle, radius ,(snr/100) )
                        except:
                            pass
                        # SAT 4
                        try:
                            sat4 = fields[16:]

                            satid = int(sat4[0]),
                            elevation = int(sat4[1]),
                            azimuth = int(sat4[2]),
                            snr = -1
                            try:
                                snr = int(sat1[3])
                            except:
                                pass
                            
                            # Рисование точки 
                            angle = azimuth[0]
                            radius = 90-elevation[0]

                            if 'GP' in line:
                                draw_point(image1,draw1, angle, radius, 0,1,0)
                                if snr>=0:
                                    #draw_point_direct(image2,draw2,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image2,draw2,angle, radius ,(snr/100) )
                            if 'GL' in line:
                                draw_point(image1,draw1, angle, radius, 1,0,0)
                                if snr>=0:
                                    #draw_point_direct(image3,draw3,angle, radius ,int(256-200+snr*2),int(256-200+snr*2),int(256-200+snr*2))
                                    draw_point_iron(image3,draw3,angle, radius ,(snr/100) )
                        except:
                            pass



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

                    except ValueError as e:
                        pass
                        #print("Ошибка при парсинге NMEA:", e)

                    


                    #print(parse_nmea_satellites(line))
            except serial.SerialException as e:
                    print("Ошибка при чтении данных GPS:", e)
        



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
thread = threading.Thread(target=gps_read)
thread.daemon = True
thread.start()

# Запуск главного цикла Tkinter
root.mainloop()