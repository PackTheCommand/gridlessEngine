import threading
import time
import tkinter

import tkinter.font as tkFont
import importlib
from tkinter import *

import keyboardEvents
from keyboardEvents import *
from types import NoneType
import Static_Var
import Debuger

fps = 20
__runtimeTicks = 1.0
__waitTime = 1 / fps

from PIL import Image  #


def doNothing(e=""):
    pass


def t(d=""):
    print("000")


__screen = None
__running = True
__RuntimeFunction = doNothing()  # sets the defuld function to do nothing


def openScreen(x, y, bg_image, DevMode=True):
    global __screen

    importlib.reload(tkinter)
    Debuger.Ope_Debug(DevMode)
    __screen = screen(x, y, bg_image)
    Static_Var.screen_link = __screen


def setFPS(new_fps):
    global fps
    new_fps = fps


def __Runtime():
    global __RuntimeFunction
    __RuntimeFunction  # executes the Function


def removeElement(e):
    Static_Var.__ElementList.remove(e)


def testForClickable(event=None, ovw=False, _x=0, _y=0):
    if ovw:
        x, y = _x, _y
    else:
        x = event.x
        y = event.y
    # print(Static_Var.__ElementList)
    L = Static_Var.__ElementList

    L.reverse()
    for elm in L:

        # print(elm.is_in_click(x, y))
        if (elm.is_in_click(x, y)):
            # if(type(ab)==tuple):
            #    item.runKlickFunction()
            # else:
            #    if(ab.is_in_click()):
            #        ab.runKlickFunction()

            r = x, y
            elm.runKlickFunction()
            return True
    t = threading.Thread(target=__thre_emp_k)
    t.start()
    return False


emp_klick = False


def __thre_emp_k():
    global emp_klick
    emp_klick = True
    time.sleep(0.1)
    emp_klick = False


def DisableObjViewer():
    global __screen
    objV = Static_Var.ret_objviewer()
    objV.setNotShow()
    __screen.tk.deiconify()


def StopEngine():
    global __running
    __running = False
    Static_Var.__ElementList == []


    exit(0)
    pass


class screen():
    def __init__(self, screen_x, screen_y, background, sx=100, sy=200):
        tk = Tk()
        w = tk.winfo_screenwidth()

        h = tk.winfo_screenheight()
        print(h)
        y = (h - screen_y) / 2
        x = (w - screen_x) / 2
        tk.geometry("%dx%d+%d+%d" % (screen_x, screen_y, x, y))
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

        self.exitFunc = None
        self.screen_x = screen_x
        self.screen_y = screen_y

        canvas = tkinter.Canvas(master=tk, width=screen_x, height=screen_y)
        canvas.pack(expand=YES, fill=BOTH)  #

        canvas.configure(borderwidth=0)

        # anvas.create_line(1,1,2,2,fill="#ff9f9f")
        canvas.bind("<Button-1>", testForClickable)

        self.Draw = canvas
        self.RenderBackgroung()

    def getTk(self):
        return self.tk

    def __Focus_in(self, gfe=""):
        Static_Var.setFocus(True)
        print("focus in")

    def __Focus_out(self, gfe=""):
        Static_Var.setFocus(False)
        print("focus out")

        # self.Draw.create_rectangle(x, y, x, y, outline=collor)
        #                  p1,cx,p2,cy                # p1,p2=Punkte #cx= X_Coordinate,cy=Y_Coordinate

    def RenderBackgroung(self):
        t = self.Draw.create_image(0, 0, image=self.i, anchor=NW)

        return

    def RenderImage(self, bx, by, image):
        """Engineside"""
        self.Draw.create_image(bx, by, image=image, anchor=NW)

    def __all_exit(self):
        self.tk.destroy()
        self.exitFunc()
        exit(0)


def setKeyListener(function):
    """Sets the KeyBoard-Listener(The function that is called is a key is pressed/released)
       the used function gets a tuple(p/r:str,key:str) p is pressed,r is released
    """
    keyboardEvents.setKeyFunction(function)


def setExitFunction(f):
    global __screen
    __screen.exitFunc = f


def forgetE(e):
    can_e = e.img
    __screen.Draw.delete(can_e)


def PlaceImage(Path, x_pos, y_pos, func=None, Name=None):
    """"Ads a new Element to the screen ,returns the Element-Object
    """
    global __screen, Debuger
    Im = Image.open(Path)
    # CI = Im.convert('RGB')
    # FI = CI.load()

    w, h = Im.width, Im.height

    image = tkinter.PhotoImage(master=__screen.tk, file=Path)

    # __screen.Draw.create_image(x_pos, y_pos, image=image, anchor=NW)
    s = Image_Element(x_pos, y_pos, w + x_pos, h + y_pos, func, image, __screen, Name=Name, path=Path)
    Debuger.plusElement(s)
    return s


def PlaceText(Text, x_pos, y_pos, Name=None, fontSize=8, Collor="black"):
    """"Ads a new Element to the screen ,returns the Element-Object
    """
    global __screen, Debuger
    # __screen.Draw.create_image(x_pos, y_pos, image=image, anchor=NW)
    s = Text_Element(x_pos, y_pos, Text, __screen, Name, font_Size=8)
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


class Image_Element():

    def __init__(self, x, y, max_x, max_y, function_, image, screen, Name=None, path=""):
        if Name is not None:
            self.name = Name
        else:
            self.name = "?"
        self.path = path
        self.type = "Texture"
        self.function = function_
        self.img = screen.Draw.create_image(x, y, image=image, anchor=NW)
        self.follower_List = []
        # old: self.elementKey = Static_Var.global_Layer_ID
        self.screen = screen
        self.image = image
        self.b_x, self.b_y = x, y
        self.e_x, self.e_y = max_x, max_y
        Static_Var.addElement(self)

        self.isActive = True

    def lift(self):
        self.screen.Draw.lift(self.img)

        v = Static_Var.global_Layer_ID
        Static_Var.addElement(self)
        Static_Var.removeElement(self)
        # self.elementKey = v + 1

    def lower(self):
        Static_Var.removeElement(self)
        Static_Var.lower_insert(self)

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

    def addFollower(self, element):
        """A Follower 'follows' the main objects movement"""
        self.follower_List += [element]

    def remFollower(self, element):
        self.follower_List.remove(element)

    def delete(self):
        """Warning: Unsupported"""
        Static_Var.removeElement(self)

    def setClickable(self, state: bool):
        self.is_active = state

    def runKlickFunction(self):
        if type(self.function) != NoneType:
            self.function.get()

    def move(self, x, y):
        if type(x) == str:
            if x == "":
                raise ValueError("given x value is empty")
            x = int(float(x.replace("~", str(self.b_x))))
        if type(y) == str:
            if x == "":
                raise ValueError("given y value is empty")
            y = int(float(y.replace("~", str(self.b_y))))
        """Moves the Object to an relative Position"""
        self.b_x += x
        self.e_x += x
        self.b_y += y
        self.e_y += y
        self.screen.Draw.move(self.img, x, y)
        for follower in self.follower_List:
            follower.move(x, y)

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
        """Moves the Object to an absolute Position"""
        if (type(x) == str):
            if (x == ""):
                raise ValueError("given x value is empty")
            x = int(float(x.replace("~", str(self.b_x))))
        if (type(y) == str):
            if (x == ""):
                raise ValueError("given y value is empty")
            y = int(float(y.replace("~", str(self.b_y))))

        x_plus = (self.b_x - x) * -1
        y_plus = (self.b_y - y) * -1

        self.move(x_plus, y_plus)

    def is_in_click(self, x, y):
        xb, yb = self.b_x, self.b_y
        xe, ye = self.e_x, self.e_y
        t = (xb <= x <= xe) & (yb <= y <= ye)
        if t & self.isActive:
            return True
        return False


class Text_Element():

    def __init__(self, x, y, text, screen, Name=None, font_Size=8, Color="black"):
        if (Name != None):
            self.name = Name
        else:
            self.name = "?"
        self.type = "Text"
        self.font_size = font_Size
        self.color = Color
        font1 = tkFont.Font(family="Arial", size=font_Size)  # weight="bold")
        self.img = screen.Draw.create_text(x, y, text=text, font=font1, fill=Color)
        self.follower_List = []
        self.screen = screen
        self.b_x, self.b_y = x, y
        self.e_x, self.e_y = x + 6, y + 6
        self.isActive = True

    def lift(self):
        self.screen.Draw.lift(self.img)

        # self.elementKey = v + 1

    def addFollower(self, element):
        """A Follower 'follows' the main objects movement"""
        self.follower_List += [element]

    def remFollower(self, element):
        self.follower_List.remove(element)

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
        for folower in self.follower_List:
            folower.move(x, y)

    def setText(self, text):
        self.screen.Draw.delete(self.img)
        font1 = tkFont.Font(family="Arial", size=self.font_size)  # weight="bold")
        self.img = self.screen.Draw.create_text(self.b_x, self.b_y, text=text, font=font1, fill=self.color)

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
        """Moves the Object to an absolute Position"""
        if (type(x) == str):
            if (x == ""):
                raise ValueError("given x value is empty")
            x = int(float(x.replace("~", str(self.b_x))))
        if (type(y) == str):
            if (x == ""):
                raise ValueError("given y value is empty")
            y = int(float(y.replace("~", str(self.b_y))))
        x_plus = (self.b_x - x) * -1
        y_plus = (self.b_y - y) * -1

        self.move(x_plus, y_plus)


def RunEngine():
    """Starts The Game-Engine"""
    try:
        __screen.tk.mainloop()
    except Exception:
        raise UserWarning("tkinter module is already runing in an other Thread \n"
                          " and so raised a RuntimeError the Engine might not be runing !")


class GameFunction:
    def __init__(self, function, args=()):
        print(f"::::{args=},{function=}")
        """This Object ids used to store links to functions() for the PlaceImage( ... func=GameFunction(function)   ... """
        self.function = function
        self.args = args

    def get(self):
        l = self
        self.function(*self.args)
