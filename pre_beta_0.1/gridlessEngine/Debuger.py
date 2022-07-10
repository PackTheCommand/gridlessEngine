
from tkinter import Tk, ttk, Scrollbar, Frame, Label, Entry, Button, Canvas

import Static_Var
from PopUp import popUp


class Obj_viever_frame(ttk.Frame):
    # credit to https://blog.teclado.com/tkinter-scrollable-frames/
    def __init__(self, Master, *args, **kwargs):
        super().__init__(Master, *args, **kwargs)

        scrol_in = Canvas(self, width=160, height=300)
        scrol_in.configure()
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=scrol_in.yview)
        self.frame = ttk.Frame(scrol_in)

        self.frame.bind("<Configure>",lambda e: scrol_in.configure(scrollregion=scrol_in.bbox("all")))
        scrol_in.create_window((1, 0), window=self.frame)
        scrol_in.configure(yscrollcommand=scrollbar.set)
        scrol_in.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def Frame(self):
        return self.frame


class debugWindow():
    def __init__(self):
        self.tk = Tk()
        self.tk.resizable(True,False)
        self.tk.title("Obj-Viewer")
        self.tk.iconbitmap(r"resources\obj_viever.ico")
        self.tk.wm_geometry("%dx%d" % (190, 300))
        f = Obj_viever_frame(self.tk)
        f.pack()
        self.Board = f.Frame()
        self.lememt_List = []
    def setNotShow(self):


        #self.tk.minsize()
        self.tk.overrideredirect(True)
        self.tk.withdraw()
    def hilight(self,Lem):
        obj=Lem.object
        if Static_Var.Hilight!=None:
            Static_Var.screen_link.Draw.delete(Static_Var.Hilight)
            Static_Var.Hilight=None
        #l=self.
        x1,y1=obj.b_x,obj.b_y
        x2, y2 =obj.e_x,obj.e_y
        Static_Var.Hilight=Static_Var.screen_link.Draw.create_rectangle(x1,y1,x2,y2,outline="yellow",width=5)

    def addElement(self, element):
        Name = element.name

        l = ttk.Button(self.Board, text=Name, command=lambda: self.hilight(Lem))
        Lem = lement(element)
        Lem.setl(l)

        l.pack()
        l.bind("<Button-3>", Lem.openPop)
        self.tk.bind("<Button-1>", Lem.closePop)

        self.tk.bind("<Configure>", Lem.closePop)

V_popup=None
class lement:
    def __init__(self, element):
        self.object = element
        self.label = None
    def setl(self,l):
        self.label=l
    def openPop(self, event):
        global V_popup
        try:
            self.closePop("")
        except Exception as e:
            print(e)
            pass
        V_popup = None
        V_popup = popUp(self)


    def closePop(self, event):
        global V_popup
        if (V_popup != None):
            V_popup.leave("")
            V_popup = None



debuger_ = debugWindow()
Static_Var.link_Debuger=debuger_
def plusElement(s):
    global debuger_
    debuger_.addElement(s)