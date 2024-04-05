from tkinter import *
import tkinter
from tools import *
import math

_WIDTH = 1200
_HEIGHT = 600

x = x2 = y = y2 = 0
_COORDINATES = []
pressed_button=None
color='#000000'

def draw(click):
    global _COORDINATES
    global mainCanvas
    x, y= convertPixels(click.x, click.y)
    _COORDINATES.append((x, y))
    if pressed_button == firstButton:  line_diff_analyzer()
    elif pressed_button == secondButton:  line_brezenhem()
    elif pressed_button == thirdButton:   line_smooth()
    elif pressed_button == fourthButton:   circle()
    elif pressed_button == fifthButton:   ellips()
    elif pressed_button == sixButton: hyperbola()
    elif pressed_button == sevenButton: parabola2()
    else: _COORDINATES = []

def change_button(button):
    global pressed_button
    if pressed_button == None:
        pressed_button = button
        button['state'] = 'disabled'
    elif pressed_button == button:
        pressed_button = None
        button['state'] = 'active'
    else:
        pressed_button['state'] = 'active'
        pressed_button = button
        button['state'] = 'disabled'
        
def get_color(base, alpha):
    global root
    background_r, background_g, background_b = 255, 255, 255
    rgb = root.winfo_rgb(base)
    new_r = round((1 - alpha) * background_r + alpha * rgb[0]/256)
    new_g = round((1 - alpha) * background_g + alpha * rgb[1]/256)
    new_b = round((1 - alpha) * background_b + alpha * rgb[2]/256)
    return f"#{new_r:02X}{new_g:02X}{new_b:02X}"

def change_color(new_color): 
    global color
    color = new_color
    
def line_diff_analyzer():
    global _COORDINATES
    global mainCanvas
    if len(_COORDINATES) == 2:
        x, y, x2, y2 = _COORDINATES[0][0], _COORDINATES[0][1], _COORDINATES[1][0], _COORDINATES[1][1]
        length = max(abs(x2-x), abs(y2-y))
        if length == 0:
            draw_dot(mainCanvas, x, y, color)
            _COORDINATES = []
            return
        dx = (x2-x)/length
        dy = (y2-y)/length
        draw_dot(mainCanvas, x, y, color)
        i = 0
        while i < length:
            x = x + dx
            y = y + dy
            round_x, round_y = round(x), round(y)
            draw_dot(mainCanvas, round_x, round_y, color)
            i += 1
        _COORDINATES = []

def line_brezenhem():
    global _COORDINATES
    global mainCanvas
    if len(_COORDINATES) == 2:
        x, y, x2, y2 = _COORDINATES[0][0], _COORDINATES[0][1], _COORDINATES[1][0], _COORDINATES[1][1]
        dx = x2-x
        dy = y2-y
        if abs(dx) >= abs(dy):
            main, main_s = x, 'x'
            sec, sec_s = y, 'y'
            main_d = dx
            sec_d = dy
        else:
            main, main_s = y, 'y'
            sec, sec_s = x, 'x'
            main_d = dy
            sec_d = dx
        e = abs(2*sec_d) - abs(main_d)
        draw_dot(mainCanvas, x, y, color)
        i = 0
        while i < abs(main_d):
            if e >= 0:
                sec += 1*sign(sec_d)
                e -= abs(2*main_d)
            main += 1*sign(main_d)
            e += abs(2*sec_d)
            i += 1
            if abs(dx) >= abs(dy): draw_dot(mainCanvas, main, sec, color)
            else: draw_dot(mainCanvas, sec, main, color)
        _COORDINATES = []

def line_smooth():
    global _COORDINATES
    global mainCanvas
    color = "black"
    if len(_COORDINATES) == 2:
        x, y, x2, y2 = _COORDINATES[0][0], _COORDINATES[0][1], _COORDINATES[1][0], _COORDINATES[1][1]
        length = max(abs(x2-x), abs(y2-y))
        if length == 0:
            draw_dot(mainCanvas, x, y)
            _COORDINATES = []
            return
        dx = (x2-x)/length
        dy = (y2-y)/length
        if abs((x2-x)) >= abs(y2-y):
            main = x
            sec = y
            main_d = dx
            sec_d = dy
        else:
            main = y
            sec = x
            main_d = dy
            sec_d = dx
        draw_dot(mainCanvas, x, y, color)
        i = 0
        while i < length:
            main += main_d
            sec += sec_d
            sec_fractional = sec%1
            first_color, second_color = get_color(color, 1-sec_fractional), get_color(color, sec_fractional)
            sec1 = int(sec)
            sec2 = sec1+1
            if abs((x2-x)) >= abs(y2-y):
                draw_dot(mainCanvas, main, sec1, first_color)
                draw_dot(mainCanvas, main, sec2, second_color)
            else:
                draw_dot(mainCanvas, sec1, main, first_color)
                draw_dot(mainCanvas, sec2, main, second_color)
            i += 1
        _COORDINATES = []

def circle():
    global _COORDINATES
    global mainCanvas
    if len(_COORDINATES) == 2:
        x1, y1, x2, y2 = _COORDINATES[0][0], _COORDINATES[0][1], _COORDINATES[1][0], _COORDINATES[1][1]
        R = math.sqrt((x2-x1)**2+(y2-y1)**2)
        x, y = 0, round(R)
        limit = 0
        d = 2 - 2*R
        draw_dot(mainCanvas, x1, round(y1+R), color)
        mirror(mainCanvas, 0, round(R), x1, y1, color)
        diagonal = True
        while y > limit:
            diagonal = True
            if d > 0:
                d1 = 2*d - 2*x - 1
                if d1 > 0: 
                    diagonal = False
                    y -= 1
                    d = d - 2*y + 1
            elif d < 0:
                d1 = 2*d + 2*y - 1
                if d1 <= 0: 
                    diagonal = False
                    x += 1
                    d = d + 2*x + 1
            if diagonal:
                x += 1
                y -= 1
                d += 2*x - 2*y +2
            draw_dot(mainCanvas, x + x1, y + y1, color)
            mirror(mainCanvas, x, y, x1, y1, color)
        _COORDINATES = []


def ellips():
    global _COORDINATES
    global mainCanvas
    if len(_COORDINATES) == 2:
        x1, y1, x2, y2 = _COORDINATES[0][0], _COORDINATES[0][1], _COORDINATES[1][0], _COORDINATES[1][1]
        a = round(abs((x2-x1))/2)
        b = round(abs((y2-y1))/2)
        center_x = round((x2+x1)/2)
        center_y = round((y2+y1)/2)
        x, y = 0, b
        limit = 0
        d = b**2 - 2*b*a**2 + a**2
        draw_dot(mainCanvas,center_x, round(center_y+b), color)
        mirror(mainCanvas, 0, round(b), center_x, center_y)
        diagonal = True
        while y > limit:
            diagonal = True
            if d > 0:
                d1 = 2*d - 2*x*b**2 - b**2
                if d1 > 0: 
                    diagonal = False
                    y -= 1
                    d = d - 2*y*a**2 + a**2
            elif d < 0:
                d1 = 2*d + 2*y*a**2 - a**2
                if d1 <= 0: 
                    diagonal = False
                    x += 1
                    d = d + 2*x*b**2 + b**2
            if diagonal:
                x += 1
                y -= 1
                d += 2*x*b**2 - 2*y*a**2 + b**2 + a**2
            draw_dot(mainCanvas, x + center_x, y + center_y, color)
            mirror(mainCanvas,x, y, center_x, center_y)
        _COORDINATES = []
        

def parabola2():
    global _COORDINATES
    global mainCanvas
   
    if len(_COORDINATES) == 2:
        xc, yc, x_end, _ = _COORDINATES[0][0], _COORDINATES[0][1],  _COORDINATES[1][0], _COORDINATES[1][1] 
        try:
            p = float(x1Entry.get())
        except Exception:
            print(f"{x1Entry.get()} is not integer")  
            _COORDINATES = []
            return
        bound = x_end
        draw_dot(mainCanvas,xc, yc)
        xi = 0
        yi=0
        x=0
        while (xc + x < bound and x**p < _HEIGHT):
            _COORDINATES = [[xc+x, yc-x**p],[xc+x+1, yc-(x+1)**p]]
            line_brezenhem()
            _COORDINATES = [[xc-x, yc-x**p],[xc-(x+1), yc-(x+1)**p]]
            line_brezenhem()
            x+=1
        _COORDINATES = []
        
def hyperbola():
    global _COORDINATES
    global mainCanvas
    if len(_COORDINATES) == 2:
        x1, y1, x2, y2 = _COORDINATES[0][0], _COORDINATES[0][1], _COORDINATES[1][0], _COORDINATES[1][1]
        a = round(abs((x2-x1))/2)
        b = round(abs((y2-y1))/2)
        center_x = round((x2+x1)/2)
        center_y = round((y2+y1)/2)
        x, y = a, 0
        canvas_height = 41
        limit = max(canvas_height-center_y, center_y)
        d = 2*a*b**2 - a**2
        draw_dot(mainCanvas,x + center_x, y + center_y, color)
        mirror(mainCanvas,x, y, center_x, center_y)
        i = 0
        diagonal = True
        while i < limit:
            diagonal = True
            if d > 0:
                d1 = 2*d - 2*x*b**2 - b**2
                if d1 > 0: 
                    diagonal = False
                    y += 1
                    d = d - 2*y*a**2 - a**2
            elif d < 0:
                d1 = 2*d + 2*y*a**2 + a**2
                if d1 <= 0: 
                    diagonal = False
                    x += 1
                    d = d + 2*x*b**2 + b**2
            if diagonal:
                x += 1
                y += 1
                d += 2*x*b**2 - 2*y*a**2 + b**2 - a**2
            draw_dot(mainCanvas,x + center_x, y + center_y, color)
            mirror(mainCanvas,x, y, center_x, center_y)
            i+=1
        _COORDINATES = []
        
root = Tk()
root.title("LinesDrawings")
root.maxsize(_WIDTH, _HEIGHT)
root.minsize(_WIDTH, _HEIGHT)
root.geometry("1200x600")
root.config(bg='white')
root.resizable(width=0, height=0)

drawFrame = Frame(root,  width=920, height=560, bg="#8eddfb", relief=RAISED)
drawFrame.pack(side=LEFT, padx=20, pady=20)
drawFrame.pack_propagate(0)

Label(drawFrame, text="Window", bg='#8eddfb', font="TkCaptionFont").pack(anchor="n")
mainCanvas = Canvas(drawFrame, bg="white", width=900, height=500)
mainCanvas.bind('<Button-1>', draw)

DrawPixels(mainCanvas, 900, 500, 10)

toolFrame = Frame(root, width=200, height=560,  bg="#8eddfb")
toolFrame.pack(side=RIGHT, padx=20, pady=20)
toolFrame.pack_propagate(0)

Label(toolFrame, text="Tools", bg='#8eddfb').pack(side=TOP, padx=5, pady=5)
x1Entry, y1Entry = createBlockOfCoordinates(toolFrame, "x1", "y1")
x2Entry, y2Entry = createBlockOfCoordinates(toolFrame, "x2", "y2")

entries = [x1Entry, x2Entry, y1Entry, y2Entry]
Button(toolFrame, text="Click", command = lambda: take(mainCanvas, entries)).pack(fill=X,anchor="n", padx=8, pady= 8)

clear_button = Button(toolFrame, text="Clear", command= lambda:clear(mainCanvas, entries))
clear_button.pack(anchor="n", fill=X, padx=6, pady=6)

names = ["diff_analyzer", "brezenhem", "smooth", "circle", "elipse", "giperbola", "parabola"]

firstButton = Button(toolFrame, text=names[0], command=lambda:change_button(firstButton), bg="white", width=10)
firstButton.pack(anchor="n", fill=X, padx=5, pady=5)
secondButton = Button(toolFrame, text=names[1], command=lambda:change_button(secondButton), bg="white", width=10)
secondButton.pack(anchor="n", fill=X, padx=5, pady=5)
thirdButton = Button(toolFrame, text=names[2], command=lambda:change_button(thirdButton), bg="white", width=10)
thirdButton.pack(anchor="n", fill=X, padx=5, pady=5)
fourthButton = Button(toolFrame, text=names[3], command=lambda:change_button(fourthButton), bg="white", width=10)
fourthButton.pack(anchor="n", fill=X, padx=5, pady=5)
fifthButton = Button(toolFrame, text=names[4], command=lambda:change_button(fifthButton), bg="white", width=10)
fifthButton.pack(anchor="n", fill=X, padx=5, pady=5)
sixButton = Button(toolFrame, text=names[5], command=lambda:change_button(sixButton), bg="white", width=10)
sixButton.pack(anchor="n", fill=X, padx=5, pady=5)
sevenButton = Button(toolFrame, text=names[6], command=lambda:change_button(sevenButton), bg="white", width=10)
sevenButton.pack(anchor="n", fill=X, padx=5, pady=5)

redButton = Button(toolFrame,bg="#FF0000", command=lambda:change_color("#FF0000"))
redButton.pack(anchor="w", fill=X, padx=5, pady=1)
blueButton = Button(toolFrame,bg="blue", command=lambda:change_color("blue"))
blueButton.pack(anchor="w", fill=X, padx=5, pady=5)
greenButton = Button(toolFrame,bg="green", command=lambda:change_color("green"))
greenButton.pack(anchor="w", fill=X, padx=5, pady=5) 

root.mainloop()
