from tkinter import *
import tkinter

def clicked(*args):
    print(args)

def DrawPixels(canva:Canvas, x_size:int, y_size:int, pixSize:int):
    for y in range(0, y_size, pixSize):
        for x in range(0 , x_size, pixSize):
            color = "white"
            rect = canva.create_rectangle(x, y, x+pixSize , y+pixSize , fill=color, outline="#b6c5e9", tags=(x,y))
            canva.tag_bind("rect", '<Button-1>', clicked(x,y))
            canva.pack()
            x += pixSize 
        y += pixSize 
        x = pixSize 
        
def draw_dot(canvas:Canvas, x, y, color='black'):
    x1 = x*10
    y1 = y*10
    canvas.create_rectangle(x1-10, y1-10, x1, y1, fill=color, outline=color)

def take(canva, x:list):
    dots = []
    try:
        for el in x:
            print(el.get())
            dots.append(int(el.get()))
    except Exception:
        print(f"{el} is not integer")  
        return
    printLine(canva, dots[0], dots[1], dots[2], dots[3], 10)  
    
def clear(mainCanvas, x:list):
    for el in x: el.delete(0, END)
    DrawPixels(mainCanvas, 900, 500, 10)

def createBlockOfCoordinates(toolFrame, name_x:str, name_y:str):
    toolPart = Frame(toolFrame, width=200, height=100, bg="#8eddfb")
    toolPart.pack(side=TOP)
 
    XPart = Frame(toolPart, width=100)
    XPart.pack(side=LEFT)
    Label(XPart, text=name_x).pack(side=LEFT)
    x = Entry(XPart, width=10)
    x.pack(side=LEFT, padx=10, pady=15)
    
    YPart = Frame(toolPart, width=100)
    YPart.pack(side=LEFT)
    Label(YPart, text=name_y).pack(side=LEFT)
    y = Entry(YPart, width=10)
    y.pack(side=LEFT, padx=10, pady=15)
   
    return x, y

def printLine(canva:Canvas, x, y, x1, y1, pixSize):
    for yp in range(y*10, y1*10, pixSize):
        for xp in range(x*10, x1*10, pixSize):
            canva.create_rectangle(xp*10, yp*10, xp*10+pixSize, yp*10+pixSize, fill="blue", outline="#b6c5e9")
            xp += pixSize
        yp += pixSize
        xp = pixSize
        
def convertPixels(x, y):
    x = int(x / 10) + 1
    y = int(y / 10) + 1
    return x, y

def mirror(mainCanvas, x, y, center_x, center_y, color="black"):
    mirrored_x = center_x - x - 1
    mirrored_y = center_y - y - 1
    draw_dot(mainCanvas, mirrored_x, y + center_y, color)
    draw_dot(mainCanvas, x + center_x, mirrored_y, color)
    draw_dot(mainCanvas, mirrored_x, mirrored_y, color)

def sign(number):
    if number < 0: return -1
    else: return 1
