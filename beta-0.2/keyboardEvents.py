from pynput import keyboard

import Static_Var


class KeyBoard:

    def N(e):

        pass

    def KeyChecker(self):
        pass

    def key_press(key):
        global keyfunction
        if (Static_Var.Fokus):
            ret = "p", str(key).replace("'","")

            keyfunction(ret)


    def key_release(key):
        global keyfunction
        if (Static_Var.Fokus):

            ret = "r", str(key).replace("'","")
            keyfunction
            keyfunction(ret)

            pass

    listener = keyboard.Listener(
        on_press=key_press,
        on_release=key_release)
    listener.start()


keyfunction = KeyBoard.N


def setKeyFunction(f):
    global keyfunction

    keyfunction=f
    print(keyfunction)
