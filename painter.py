from PIL import Image, ImageFilter, ImageGrab
from pynput.mouse import Button, Controller
from pynput import keyboard
import time

mouse = Controller()
p = None
img = None
isB = False


def click(x, y):
    mouse.position = (x, y)
    mouse.click(Button.left, 1)


def rgb_distance(rgb_1, rgb_2):
    r1, g1, b1 = rgb_1
    r2, g2, b2 = rgb_2
    return ((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)**0.5


def draw(s, pt=p, n=1, m='00', r=1, t=220, st=0.01):
    global img
    img = Image.open(s)
    img = img.resize((int(img.width*n), int(img.height*n)))
    pt = p

    if m[0] == '0':
        img = img.filter(ImageFilter.SMOOTH).filter(
            ImageFilter.CONTOUR).convert('L')
    else:
        img = img.convert('L')

    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):

            if isB:
                print('已中止')
                return

            pix = pixels[x, y]
            if r*pix < r*t:
                if m[1] == '0' or (x % 2 == 0 and y % 2 == 0):
                    click(pt[0]+x, pt[1]+y)
                    time.sleep(st)


def color(s, n=1, st=0.01):
    global img
    colors, pos = [], []
    print("先将光标移动到画板上回车，再将光标移动到颜色按钮回车\n最后输入s并回车从当前光标位置开始绘制，输入q并回车退出")
    while True:
        input_str = input()
        if input_str == 's':
            break
        elif input_str == 'q':
            return
        mp = mouse.position
        if len(pos) == 0:
            mp = (mp[0]-2, mp[1]-2)
        c = ImageGrab.grab().getpixel(mp)
        pos.append(mp)
        colors.append(c)
        print('{} {}'.format(c, mp))

    mp = mouse.position
    img = Image.open(s)
    img = img.resize((int(img.width*n), int(img.height*n))).convert('RGB')
    pixels = img.load()
    while True:
        for x in range(img.width):
            for y in range(img.height):

                if isB:
                    print('已中止')
                    return

                pix = pixels[x, y]
                ds = []
                for c in colors:
                    ds.append(rgb_distance(c, pix))
                index = ds.index(min(ds))
                if index != 0:
                    click(pos[index][0], pos[index][1])
                    click(mp[0]+x, mp[1]+y)
                    time.sleep(st)
        if input('输入s再画一个，回车则结束：') != 's':
            return


def on_release(key):
    if key == keyboard.Key.esc:
        global isB
        isB = True


listener = keyboard.Listener(on_release=on_release)
listener.start()

print("""对象：
    p：光标所在位置             mouse：鼠标
    time：时间                 img：图像
命令：
    draw(s图片地址，pt点坐标，n缩放倍数，m模式，r是否反转，t下笔阈值，st延迟时间)：绘制黑白图片
        例如 draw('img.png') 或 draw('img.png', pt=[200, 300], n=1, m='00', r=-1, t=220, st=0)
    color(s图片地址，n缩放倍数，st延迟时间)：绘制彩色图片
        例如 color('img.png', n=0.1)
    click(横坐标，纵坐标)：点击某位置
        例如 click(200, 300)
模式：
    第1个数字：             第2个数字：
        0：去噪边缘灰度化        0：正常
        1：只进行灰度化          1：稀疏

注意：
    1.使用 CTRL+C 退出程序，绘制中按下ESC键中止
    2.还可执行其它的python命令，如 img.show() 显示图片
""")

while True:
    isB = False
    i = input('>>> ')
    p = mouse.position
    try:
        o = eval(i)
        if o != None:
            print(o)
    except Exception as e:
        print(e)
