__ElementList = []
Hilight=None
screen_link=None
Fokus=True
def removeElement(e):
    global __ElementList
    #__ElementList.remove(e)
    one=True
    __ElementList.remove(e)
    return

def lower_insert(element):
    global __ElementList
    __ElementList.insert("-1",element)

def clear():
    global __ElementList,Hilight,screen_link,Fokus
    __ElementList = []
    Hilight = None
    screen_link = None
    Fokus = True
link_Debuger=None
def ret_objviewer():
    return link_Debuger
def addElement(e):
    global __ElementList
    __ElementList+=[e]


def setFocus(t):
    global Fokus
    Fokus=t
