import threading
import time
import tkinter
from copy import copy, deepcopy

from tkinter import *

import keyboardEvents
from keyboardEvents import *
from types import NoneType
import Static_Var
import Debuger

fps = 20
__runtimeTicks = 1.0
__waitTime = 1 / fps
RenderFrame = True
from PIL import Image  #


def doNothing(e=""):
    pass


def t(d=""):
    print("000")


__screen = None
__running = True
__RuntimeFunction = doNothing()  # sets the defuld function to do nothing


def openScreen(x, y, bg):
    global __screen

    __screen = screen(x, y, bg)
    Static_Var.screen_link = __screen


def setFPS(new_fps):
    global fps
    new_fps = fps


def __Runtime():
    global __RuntimeFunction
    __RuntimeFunction  # executes the Function


def addElement(e):

    Static_Var.__ElementList[Static_Var.global_Layer_ID] = e
    Static_Var.global_Layer_ID += 1


def removeElement(e):
    Static_Var.__ElementList.remove(e)


def testForClickable(event):
    x = event.x
    y = event.y
    #print(Static_Var.__ElementList)
    L = []
    for key in Static_Var.__ElementList.keys():

        L+=[key]
    if(L == []):
        return


    L.reverse()
    for key in L:


        i = Static_Var.__ElementList[key]

        if (i.is_in_click(x, y)):
            # if(type(ab)==tuple):
            #    item.runKlickFunction()
            # else:
            #    if(ab.is_in_click()):
            #        ab.runKlickFunction()

            r = x, y
            i.runKlickFunction()
            break


def DisableObjViewer():
    global __screen
    objV = Static_Var.ret_objviewer()
    objV.setNotShow()
    __screen.tk.deiconify()


def StopEngine():
    global __running
    __running = False
    exit(0)
    pass


class screen():
    def __init__(self, screen_x, screen_y, background):
        tk = Tk()
        tk.geometry("+%d+%d" % (screen_x, screen_y))
        tk.configure(borderwidth=0)
        tk.title("Game")
        tk.bind("<FocusIn>", self.__Focus_in)
        tk.bind("<FocusOut>", self.__Focus_out)
        tk.protocol("WM_DELETE_WINDOW", self.__all_exit)
        tk.iconbitmap(r"resources\game.ico")
        self.tk = tk

        tk.resizable(False, False)
        y = int(100 / 2)
        self.images = []
        self.BackgroundImage = background
        self.i = tkinter.PhotoImage(master=tk, file=self.BackgroundImage)

        self.screen_x = screen_x
        self.screen_y = screen_y

        canvas = tkinter.Canvas(master=tk, width=screen_x, height=screen_y)
        canvas.pack(expand=YES, fill=BOTH)  #

        canvas.configure(borderwidth=0)

        # anvas.create_line(1,1,2,2,fill="#ff9f9f")
        canvas.bind("<Button-1>", testForClickable)
        self.Draw = canvas
        self.RenderBackgroung()

    def __Focus_in(self, gfe=""):
        Static_Var.setFocus(True)
        print("focus in")

    def __Focus_out(self, gfe=""):
        Static_Var.setFocus(False)
        print("focus out")

        # self.Draw.create_rectangle(x, y, x, y, outline=collor)
        #                  p1,cx,p2,cy                # p1,p2=Punkte #cx= X_Coordinate,cy=Y_Coordinate

    def RenderBackgroung(self):
        t=self.Draw.create_image(0, 0, image=self.i, anchor=NW)

        return

    def RenderImage(self, bx, by, image):
        """Engineside"""
        self.Draw.create_image(bx, by, image=image, anchor=NW)

    def __all_exit(self):
        self.tk.destroy()
        exit(0)


def setKeyListener(function):
    """Sets the KeyBoard-Listener(The function that is called is a key is pressed/released)
       the used function gets a tuple(p/r:str,key:str) p is pressed,r is released
    """
    keyboardEvents.setKeyFunction(function)


def PlaceElement(Path, x_pos, y_pos, func=None, Name=None):
    """"Ads a new Element to the screen ,returns the Element-Object
    """
    global __screen, Debuger
    Im = Image.open(Path)
    # CI = Im.convert('RGB')
    # FI = CI.load()

    w, h = Im.width, Im.height

    image = tkinter.PhotoImage(master=__screen.tk, file=Path)

    # __screen.Draw.create_image(x_pos, y_pos, image=image, anchor=NW)
    s = sc_Element(x_pos, y_pos, w + x_pos, h + y_pos, func, image, __screen, Name=Name, path=Path)
    Debuger.plusElement(s)
    return s


def setTitel(t):
    """Sets the screens Titel"""
    global __screen
    __screen.tk.title(t)


def setIcon(Path):
    """Sets the screens Icon"""
    global __screen
    __screen.tk.iconbitmap(Path)


def SetRuntimeFunction(function, runs_per_sec):
    """!: Unsupported"""
    global __RuntimeFunction, __runtimeTicks
    __RuntimeFunction = function
    __runtimeTicks = 1 / runs_per_sec


def str_has(str_, sym):
    return str_.replace(sym, "") != str_


class sc_Element():

    def __init__(self, x, y, max_x, max_y, function_, image, screen, Name=None, path=""):
        if (Name != None):
            self.name = Name
        else:
            self.name = "?"
        self.path = path
        self.Layer = 0

        self.function = function_
        self.img = screen.Draw.create_image(x, y, image=image, anchor=NW)
        self.elementKey = Static_Var.global_Layer_ID
        self.screen = screen
        self.image = image
        self.b_x, self.b_y = x, y
        self.e_x, self.e_y = max_x, max_y
        addElement(self)

        self.isActive = True

    def lift(self):
        self.screen.Draw.lift(self.img)
        # Static_Var.global_Layer_ID+=1

        v = Static_Var.global_Layer_ID
        Static_Var.addElement(self)
        Static_Var.DelKey(self.elementKey)
        self.elementKey = v + 1

    def lower(self):
        self.screen.Draw.lower(self.img)
        Static_Var.global_lowestKey -= 1

        v = Static_Var.global_lowestKey
        Static_Var.__ElementList[v] = self
        del Static_Var.__ElementList[self.elementKey]
        self.elementKey = v

    def ChangeFunction(self, func):
        """!: Unsupported"""
        self.function = func

    def ChangeTexture(self, Texture, ChangeHitbox=True):
        """Changes the Texture and if 'ChangeHitbox' : Hitbox gets set to the new textures size """
        i = tkinter.PhotoImage(master=self.screen.tk, file=Texture)

        self.screen.Draw.delete(self.img)
        self.image = i
        self.img = self.screen.Draw.create_image(self.b_x, self.b_y, image=i, anchor="nw")

        self.path = Texture
        if (ChangeHitbox):
            Im = Image.open(Texture)
            w, h = Im.width, Im.height

            self.e_x, self.e_y = self.b_x + w, self.b_y + h

    def delete(self):
        """Warning: Unsupported"""
        removeElement(self)

    def setClickable(self, state: bool):
        self.is_active = state

    def runKlickFunction(self):
        if type(self.function) != NoneType:
            self.function.get()

    def move(self, x, y):
        if (type(x) == str):
            if (x == ""):
                raise ValueError("given x value is empty")
            x = int(float(x.replace("~", str(self.b_x))))
        if (type(y) == str):
            if (x == ""):
                raise ValueError("given y value is empty")
            y = int(float(y.replace("~", str(self.b_y))))
        """Moves the Object to an relative Position"""
        self.b_x += x
        self.e_x += x
        self.b_y += y
        self.e_y += y
        self.screen.Draw.move(self.img, x, y)

    def setVisible(self, state: bool):
        """Toggles the Visibility,MuseKlick-intractability of the object"""
        if (not state):
            s = 'hidden'
            self.isActive = False
        else:
            s = 'normal'
            self.isActive = True
        self.screen.Draw.itemconfigure(self.img, state=s)

    def moveTo(self, x, y):
        if (type(x) == str):
            if (x == ""):
                raise ValueError("given x value is empty")
            x = int(float(x.replace("~", str(self.b_x))))
        if (type(y) == str):
            if (x == ""):
                raise ValueError("given y value is empty")
            y = int(float(y.replace("~", str(self.b_y))))

        """Moves the Object to an absolute Position"""
        old_x, old_y = self.b_x, self.b_y
        new_x, new_y = x, y
        if (old_x == 0):
            old_x = 1
        if (old_y == 0):
            old_y = 1
        change_x, change_y = new_x / old_x, new_y / old_y

        fx, fy = -1 * (old_x - old_x * change_x), -1 * (old_y - old_y * change_y)

        self.e_x, self.e_y = self.e_x + fx, self.e_y + fy
        self.b_x, self.b_y = old_x + fx, old_y + fy

        self.screen.Draw.move(self.img, fx, fy)

    def is_in_click(self, x, y):

        xb, yb = self.b_x, self.b_y
        xe, ye = self.e_x, self.e_y
        # print(f"{xb}<{x}<{xe}|||{yb}<{y}<{ye}")

        t = (xb <= x <= xe) & (yb <= y <= ye)

        if t & self.isActive:
            return True
        return False

        pass


def RunEngine():
    """Starts The Game-Engine"""
    try:
        __screen.tk.mainloop()

    except RuntimeError:
        pass


class GameFunction:
    def __init__(self, function, args=()):
        """This Object ids used to store links to functions() for the PlaceElement( ... func=GameFunction(function)   ... """
        self.function = function
        self.args = args

    def get(self):
        self.function(self.args)


if __name__ == "__main__":
    RunEngine()
RenderFrame = True
