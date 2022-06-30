from math import floor, sqrt
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from clipboard import copy
from random import choice, randint
from copy import deepcopy
from time import sleep
from colorsys import hsv_to_rgb, rgb_to_hsv
  

def hextorgb(hex):
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]
    
def rgbtohex(rgb):
  rgb = [int(x) for x in rgb]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in rgb]).replace('-', '0')

def closest(color):
    global masterGradient
    
    score = None
    
    for i in masterGradient:
        if score == None or cps(i[1:], color) < score:
            score = cps(i[1:], color)
    
    for i in masterGradient:
        if score == cps(i[1:], color):
            return i[1:]

def cinv(inp):
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    res = []
    inp = [converter[i] for i in inp]
    for i in inp:
        res.append(list(converter.keys())[abs(15-i)])
    
    return ''.join(res)
    
def cav(inp0, inp1):
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    res = []
    inp0 = [converter[i] for i in inp0]
    inp1 = [converter[i] for i in inp1]
    for i in range(len(inp0)):
        ind = int(abs((inp0[i]+inp1[i])/2))
        if ind > 15:
            ind = 15-ind
        res.append(list(converter.keys())[ind])
        
    return ''.join(res)
    
def cadd(inp0, inp1):
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    inp0 = [converter[i] for i in inp0]
    inp1 = [converter[i] for i in inp1]
    res = []
    mres = []
    for i in range(len(inp0)):
        ind = (inp0[i]+inp1[i])
        while ind > 15:
            ind = 15
            if i % 2 and mres[-1] < 15:
                mres[-1] += 1
        
        mres.append(ind)
    
    for i in range(len(mres)):
        res.append(list(converter.keys())[mres[i]])
        
    return ''.join(res)

def csub(inp0, inp1):
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    inp0 = [converter[i] for i in inp0]
    inp1 = [converter[i] for i in inp1]
    res = []
    mres = []
    for i in range(len(inp0)):
        ind = (inp0[i]-inp1[i])
        while ind < 0:
            ind += 15
            if i % 2 and mres[-1] > 0:
                mres[-1] -= 1
        
        mres.append(ind)
    
    for i in range(len(mres)):
        res.append(list(converter.keys())[mres[i]])
        
    return ''.join(res)

def palettefmix(initial=None, colorAmount=6):
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    res = []
    
    if not initial:
        initial = [choice(list(converter.values())) for  i in range(6)]
    else:
        initial = [converter[i] for i in initial]
        
    res = [''.join([list(converter.keys())[z] for z in initial])]
        
    next = deepcopy(initial)
        
    for i in range(colorAmount):
        for x in range(len(initial)):
            next[x] += randint(-1*(initial[x]+15), initial[x])
            next[x] = abs(next[x])
            if next[x] > 15:
                next[x] = 15
                
        total = 0
        cache = []
        
        for n in range(len(next)):
            if not n % 2:
                total += next[i]
                cache.append(next[i])
                
        cache.sort()
    
        if total > 25:
            for n in range(len(next)):
                if (not n % 2):
                    if next[n] == cache[2]:
                        next[n] = floor(next[n]/2)
                    elif next[n] == cache[1]:
                        next[n] = floor(next[n]/1.5)
            
        res.append(cav(''.join([list(converter.keys())[z] for z in initial]), ''.join([list(converter.keys())[z] for z in next])))
        
    return res
        
def cps(boat, anchor):
    return sqrt((int(boat[:2], 16)-int(anchor[:2], 16))**2+(int(boat[2:4], 16)-int(anchor[2:4], 16))**2+(int(boat[4:], 16)-int(anchor[4:], 16))**2)
        
def palettefadd(initial=None, colorAmount=6, ambiguity=1.):
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    res = []
    
    if not initial:
        while initial == None or cps(initial, 'ffffff') > 350:
            initial = ''.join([choice(list(converter)) for  i in range(6)])
    else:
        initial = ''.join([converter[i] for i in initial])
    
    for i in range(len(initial)):
        resm = None
        atts = 0
        while resm == None or cps(resm, '000000') > 350 or cps(resm, 'ffffff') > 350 or cps(resm, initial) < 50 and atts < 50:
            current = list(converter)[floor(choice(list(converter.values()))*ambiguity)]
            if converter[current] > 15:
                current = 'f'
            elif converter[current] < 0:
                current = '0'
            
            next = ''.join([current for i in range(colorAmount)])
            if i % 2:
                resm = cadd(initial, next)
            else:
                resm = csub(initial, next)
            
            print(cps(resm, '000000'), cps(resm, 'ffffff'), cps(resm, initial), 90)
            
            if resm in res:
                resm = None
            
            atts += 1
            
        res.append(resm)
    
    return res
    
def triadMixed(starts=[]):
    global masterGradient
    
    res = []
    
    converter = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    while len(starts) < 3:
        possible = choice(masterGradient)
        if not possible in starts:
            starts.append(possible)
            
    print(starts)
        
    for i in starts:
        for x in starts:
            if i != x:
                print(i,x)
                res.append(cav(i[1:], x[1:]))
                
    print(res, 'res')
    
    return res
    
def linearGradient(starth='ffffff', endh='ff0000', magnitude=10):
    start = hextorgb('#'+starth)
    end = hextorgb('#'+endh)
    
    res = [start]
    
    for i in range(1, magnitude):
        difference = [floor((end[x]-start[x])/magnitude) for x in range(3)]
        res.append([abs(res[-1][x]+difference[x]) for x in range(3)])
    
    return res
    
def palettefratio(start='4638ab', amount=10):
    global masterGradient
    
    baseAngle = len(masterGradient)*(1-(1/1.618))
    angle = baseAngle
    angle = masterGradient.index('#'+start)
    palette = []
    
    for i in range(amount):
        if angle > len(masterGradient):
            angle -= len(masterGradient)
        palette.append(masterGradient[floor(angle)]
        )
        angle += baseAngle
    return palette
    
def increasedHue(color, amount=1):
    color = list(rgb_to_hsv(*hextorgb(color)))
    
    for i in range(amount):
        color[0] = color[0] + 1/360
        
    color = rgbtohex(hsv_to_rgb(*color))
    
    return color
    
class pfl:
    def __init__(self):
        pass
    
    @staticmethod
    def pfl(color, locations):
        res = ['#'+color]
        for i in locations:
            res.append(increasedHue(color, i))
    
        return res
    
    @staticmethod
    def triad(color):
        print(color)
        return pfl.pfl(color, [120, 240])
    
    @staticmethod
    def square(color):
        return pfl.pfl(color, [90, 180, 270])
        
    @staticmethod
    def rectangle(color, lengthwise=False):
        if not lengthwise:
            return pfl.pfl(color, [45, 125, 160])
        return pfl.pfl(color, [90, 125, 215])
        
    @staticmethod
    def triadmixed(color):
        return ['#'+palettefmix(x, 1)[1] for x in [i[1:7] for i in pfl.triad(color)]]
        
    @staticmethod
    def goldenAngle(color, amount):
        res = ['#'+color]
        angle = 137.5
        
        for i in range(amount):
            res.append(increasedHue(color, floor(angle)))
            angle += 137.5
            
            if angle > 360:
                angle -= 360
        
        return res
        

doRoot = False
    
if doRoot:
    root = tk.Tk()
    root.title('Tkinter Color Chooser')
    #root.geometry('300x150')

def change_color():
    global clicked
    global buf0
    global buf1
    global hd
    
    c2 = False
    
    if clicked.get() == 'average':
        func = cav
        c2 = True
    elif clicked.get() == 'add':
        func = cadd
        c2 = True
    elif clicked.get() == 'subtract':
        func= csub
        c2 = True
        
    elif clicked.get() == 'invert':
        func = cinv
    
    colors0 = askcolor(title="1")
    
    if c2:
        colors1 = askcolor(title="2")
        bgc = '#'+func(''.join([i for i in colors0[1]][1:]), ''.join([i for i in colors1[1]][1:]))
    else:
        bgc = '#'+func(''.join([i for i in colors0[1]][1:]))
    
    root.configure(bg=bgc)
    buf0.configure(bg=bgc)
    buf1.configure(bg=bgc)
    hd.configure(text=bgc, bg=bgc, fg='#'+cinv(bgc[1:]))
    copy(bgc[1:])
    
if doRoot:
    options = ('average', 'invert', 'add', 'subtract')
    
    clicked = tk.StringVar()
    clicked.set(options[0])
        
    buf0 = tk.Label(master=root, text='')
    buf0.grid(column=0, row=0, sticky='nwse', padx=0, pady=0, columnspan=2)
    
    enterButton = tk.Button(master=root, text='Select a Color', command=change_color)
    enterButton.grid(column=0, row=1, sticky='nwse', padx=50, pady=5)
    
    selector = tk.OptionMenu(root, clicked, *options)
    selector.grid(column=0, row=2, sticky='ew', padx=50, pady=5)
    
    hd = tk.Label(master=root, text='#d9d9d9', fg='#'+cinv('d9d9d9'))
    hd.grid(column=0, row=3, sticky='ew', padx=50, pady=5)
    
    buf1 = tk.Label(master=root, text='')
    buf1.grid(column=0, row=4, sticky='ew', padx=0, pady=0, columnspan=2)

show = tk.Tk()
show.attributes('-fullscreen', True)

current = 0

def updateBg():
    global show
    global palette
    global current
    
    if current < len(palette):
        show.configure(bg=palette[current])
        show.after(500, updateBg)
    else:
        show.destroy()
        pass
    
    current += 1
    
show.after(0, updateBg)

show.mainloop()
    
#root.mainloop()