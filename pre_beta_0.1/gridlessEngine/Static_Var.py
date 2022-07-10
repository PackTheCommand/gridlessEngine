__ElementList = {}#[]
Hilight=None
screen_link=None
Fokus=True
global_Layer_ID=0
global_lowestKey=0
def removeElement(e):
    global __ElementList
    #__ElementList.remove(e)
    one=True
    for key in __ElementList:
        if one:
            global_lowestKey=key
            one=False
        if (__ElementList.get(key) is e):
            del __ElementList[key]
            break
def DelKey(k):
    del __ElementList[k]


link_Debuger=None
def ret_objviewer():
    return link_Debuger
def addElement(e):

    global __ElementList,global_Layer_ID
    print(__ElementList)
    global_Layer_ID+=1
    __ElementList[global_Layer_ID]=e
def setFocus(t):
    global Fokus
    Fokus=t
