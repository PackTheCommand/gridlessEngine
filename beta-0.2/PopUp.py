import copy
import tkinter
from tkinter import Tk, ttk, Label, messagebox

import pyautogui
from pynput.mouse import Controller
import tkinter.font as tkFont
import Static_Var

Clipboard = None


class popUp:
    def __init__(self, lem):
        mouse = Controller()
        self.lem = lem
        self.c_H_on_texture_save = True


        current_mouse_position = mouse.position
        rk_window = Tk()

        self.t = rk_window
        rk_window.bind("<FocusOut>", self.leave)
        x, y = pyautogui.position()
        rk_window.geometry("+%d+%d" % (x, y))
        rk_window.wm_overrideredirect(True)
        #rk_window.wm_geometry("%dx%d" % (59, 180))
        rk_window.configure(bg="gray")

        B1 = ttk.Button(rk_window, text="Coppie", command=self.Coppie,width=8 ).grid(row=1, column=0, sticky="W", pady=0)
        B2 = ttk.Button(rk_window, text="Paste", command=self.Paste, width=8).grid(row=2, column=0, sticky="W", pady=0)
        B3 = ttk.Button(rk_window, text="Edit", command=self.openEditor,width=8).grid(row=3, column=0, sticky="W", pady=0)
        B4 = ttk.Button(rk_window, text="Delete", command=self.DeleteElement,width=8 ).grid(row=4, column=0, sticky="W",                                                                            pady=0)
        B5 = ttk.Button(rk_window, text="Dub", command=self.Dublicate, width=8).grid(row=5, column=0, sticky="W", pady=0)

    def leave(self, dghj):
        try:
            self.t.destroy()
        except tkinter.TclError:
            pass

    def Dublicate(self):
        self.Coppie()
        self.Paste()

    def DeleteElement(self):

        o = self.lem.object
        o.screen.Draw.delete(o.img)
        Static_Var.removeElement(o)
        self.lem.label.destroy()
        del self.lem
        pass

        self.leave("")

    def Coppie(self):
        self.leave("")
        global Clipboard

        o = self.lem.object
        Clipboard = o

    def Paste(self):
        global Clipboard
        if(Clipboard==None):
            return
        self.leave("")
        o = Clipboard
        new_o = copy.copy(Clipboard)
        new_o.name+="-copy"
        new_o.img=new_o.screen.Draw.create_image(o.b_x,o.b_y,image=new_o.image,anchor="nw")
        Static_Var.addElement(new_o)
        Static_Var.link_Debuger.addElement(new_o)

        pass

    def openEditor(self):
        self.leave("")
        obj = self.lem.object
        self.L = {}
        obj = self.lem.object
        tk = Tk()
        self.tk=tk
        tk.iconbitmap("resources\editor_dark.ico")
        tk.resizable(False, False)


        tk.geometry("+%d+%d" % (300, 100))
        tk.title("Obj-Editor")
        self.L["name"]=Box(obj.name,tk)

        Label(master=tk, text="").pack()
        if obj.type == "Texture":
            Label(master=tk, text="  Texture:  ").pack()
            self.L["texture"] = Box(f"{obj.path}", tk)
            ttk.Checkbutton(tk,
                        text='adjust cords',
                        command=None,
                        variable=self.c_H_on_texture_save,
                        onvalue=True,
                        offvalue=False).pack()
        Label(master=tk, text="  Cords: (xb|yb) ,(xe|ye)         ").pack()

        Label(master=tk, text=f">> from:                       ").pack()
        self.L["cords"] = Box(f"({obj.b_x}|{obj.b_y})", tk)

        self.L["l_pos"]=Label(master=tk, text=f">> to:     ({obj.e_x}|{obj.e_y})   ")
        self.L["l_pos"].pack()
        f= tkinter.Frame(master=tk,width=150, height=1)

        f.pack(side=tkinter.TOP, anchor= "n")
        try:
            Label(master=f, text=f"function : \n >> {getFunctionNameFromObjCall(obj.function.function)}()", width=10, height=2).pack(side="left")
        except AttributeError:
            Label(master=f, text=f"function : \n >> None", width=10,
                  height=2).pack(side="left")
        tkinter.Button(master=f,text="ID",command=self.Co_Func_id, width=1, height=1,relief="flat",bg="#89CAFF").pack(side="right")
        # self.L["func"] = Box(f"{obj.funcName}", tk)
        Label(master=tk, text="").pack()

        ttk.Button(master=tk, text="Save", command=self.Save).pack()
    def Co_Func_id(self):
        obj = self.lem.object
        self.tk.clipboard_append(obj.function)
    def Save(self):

        obj = self.lem.object
        text = self.L["cords"].get("1.0", "end-1c")
        x, y = makeVars(text)

        if (digitFloat(x) & digitFloat(x)):
            obj.moveTo(float(x), float(y))


        else:
            messagebox.showerror("Invalid input", "The cords are in the wrong format \n (x|y)")
        # -------------
        if obj.type == "Texture":
            try:
                t=self.L["texture"].get("1.0", "end-1c")
                if t!=obj.path:
                    obj.ChangeTexture(t,  ChangeHitbox=self.c_H_on_texture_save)

            except tkinter.TclError:
                messagebox.showerror("Invalid input", "This texture is corrupted \n or non existent")
        # obj.ChangeFunction(self.L["func"].get("1.0", "end-1c"))
        newName=self.L["name"].get("1.0", "end-1c")
        obj.name=newName
        self.lem.label.configure(text=newName)
        self.L["l_pos"].configure(text=f">> to:     ({obj.e_x}|{obj.e_y})   ")
        self.L["cords"].delete(0.0,tkinter.END)
        self.L["cords"].insert(0.0, f"({obj.b_x}|{obj.b_y})")
        Static_Var.screen_link.Draw.delete(Static_Var.Hilight)
        Static_Var.Hilight=None
def Box(insert, master):
    font1 = tkFont.Font(family="Gadugi", size=3)#weight="bold")
    t0 = tkinter.Text(master=master, width=15, height=1,font=font1 )
    t0.insert(0.0, insert)

    t0.pack()
    return t0


def makeVars(text):
    t = text.replace("(", "").replace(")", "").replace(" ", "").replace("\n", "")
    x, y = t.split("|")
    return x, y

def digitFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
def getFunctionNameFromObjCall(func):
    a=str(func).split(" ")
    return a[1]