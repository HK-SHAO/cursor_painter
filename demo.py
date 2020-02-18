from pynput.mouse import Button, Controller
from PIL import Image, ImageFilter
import math
import time

mouse = Controller()

def click(x, y):
    mouse.position = (x, y)
    mouse.click(Button.left, 1)

def line(p1, p2):
    mouse.position = p1
    mouse.press(Button.left)
    mouse.position = p2
    mouse.release(Button.left)

def circle(p, r):
    n = 10000
    mouse.position = [p[0]+r, p[1]]
    mouse.press(Button.left)
    time.sleep(0.01)
    for i in range(1, n):
        a = 2*math.pi*i/n
        mouse.position = [p[0]+r*math.cos(a), p[1]+r*math.sin(a)]
    mouse.release(Button.left)

def polygon(p, r, n):
    mouse.position = [p[0]+r, p[1]]
    for i in range(1, n):
        a = 2*math.pi*i/n
        line(mouse.position, [p[0]+r*math.cos(a), p[1]+r*math.sin(a)])
    line(mouse.position, [p[0]+r, p[1]])

#click(100, 100)
#line([200,200], [200,400])
#circle([200,200], 50)

def draw(p, s, n = 1, mode = 0):
    img = Image.open(s)
    # img = img.convert('1')
    img = img.resize((int(img.width*n), int(img.height*n)))
    img = img.filter(ImageFilter.SMOOTH).filter(ImageFilter.CONTOUR).convert('L')
    
    # img.show()
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            pix = pixels[x, y]
            if pix < 220:
                click(p[0]+x, p[1]+y)
                #time.sleep(0.01)

draw(mouse.position, 'write2.png', 0.8)
