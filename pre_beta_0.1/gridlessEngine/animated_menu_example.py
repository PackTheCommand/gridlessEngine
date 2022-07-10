import os

import psutil

from gridlessEngine import *

B, B1 = None, None
MenueState = -1  # -1=hiden,0=onMove,1=shown

def DisableMainGame():
    print("MainGame disabled")

def EnableMainGame():
    print("MainGame enabled")

def quit(e=""):
    x = threading.Thread(target=quit_thead)
    x.start()

def quit_thead():
    global B, B1, M, GameIsPAused, GameControllInteract
    B.setClickable(False)
    B1.setClickable(False)
    for i in range(0, 150, 10):
        B.move(3, 10)
        B1.move(-3, -10)
        time.sleep(0.001)
    current_system_pid = os.getpid()
    ThisSystem = psutil.Process(current_system_pid)
    ThisSystem.terminate()

def hide(e=""):

    global GameControllInteract, B,MenueState
    B.setClickable(False)
    if (MenueState == 1):
        MenueState =0
        GameControllInteract = False
        x = threading.Thread(target=fHide)
        x.start()

def fHide():  #
    global B, B1, M, MenueState

    for i in range(0, 300, 10):
        B.move(-10, 0)
        M.move(0, -12)
        104
        B1.move(10, 0)
        time.sleep(0.001)
    B.moveTo(-300, "~")
    B1.moveTo(806, "~")
    M.moveTo("~", -264)
    B1.setVisible(False)
    B.setVisible(False)
    M.setVisible(False)
    MenueState = -1
    EnableMainGame()

def SchowMenue():  #

    global MenueState
    if (MenueState==-1):
        MenueState =0
        DisableMainGame()
        x = threading.Thread(target=show_thead)
        x.start()

def show_thead():
    global B, B1, M, MenueState
    B.lift(),B1.lift(),M.lift()
    B1.setVisible(True)
    B.setVisible(True)
    M.setVisible(True)
    for i in range(0, 300, 10):
        B.move(10, 0)
        M.move(0, 12)
        B1.move(-10, 0)
        time.sleep(0.001)
    MenueState = 1
    B.setClickable(True)
    B1.setClickable(True)


def kl(par):
    global t, GameControllInteract, GameIsPAused,MenueState
    action, key = par
    if (action == "p"):
        match key:
            case "Key.esc":
                if MenueState == -1:
                    GameControllInteract = False
                    SchowMenue()
                elif (MenueState == 1):
                    hide()

        if MenueState !=-1:
            return
        match key:

            case 'w':
                print("test")
                G_cupe.move(0, -20)
            case "s":
                G_cupe.move(0, 20)
            case "a":

                G_cupe.move(-20, 0)
            case "d":
                G_cupe.move(20, 0)

def ButtonPreset():
    B.moveTo(-300, "~")
    B1.moveTo(806, "~")
    M.moveTo("~", -264)
    B1.setVisible(False)
    B.setVisible(False)
    M.setVisible(False)


setKeyListener(kl)
openScreen(800, 600, r"resources\b.png")
setTitel("Animated-Menu-Example")
B = PlaceElement(r"resources\examples\con.png", 0, 198, Name="Button-Continue", func=GameFunction(hide))
G_cupe = PlaceElement(r"resources\cube.png", 300, 150, Name="Cupe", func=GameFunction(hide))
B1 = PlaceElement(r"resources\examples\Quit.png", 506, 198, Name="Button-Quit", func=GameFunction(quit))
M = PlaceElement(r"resources\examples\midle.png", 274, 104, Name="menu_center")
ButtonPreset()
RunEngine()
