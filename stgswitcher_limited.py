import tkinter as tk
import sys
import os
import pydirectinput
import keyboard
import json

pydirectinput.PAUSE = 0

if os.path.isfile("config_limited.json"):#config.jsonがあるか確認
    with open("config_limited.json","r",encoding = "utf-8") as f:
        config = json.load(f)
else:
    empty={
        "keys":[{"id":"スペース","key":"space"}],"onetouch":"ctrlleft"
    }

    with open("config_limited.json","w+",encoding = "utf-8") as f:
        json.dump(empty,f,indent=4)
        config = json.load(f)
onetouchkey = config["onetouch"]
endkey = config["end"]

with open("keys.json","r",encoding="utf-8") as g:
    usekey = json.load(g)
    usekeylist=[]
    for i in usekey:
        usekeylist.append(i)

class keys:
    def __init__(self, dic, one):
        self.keyout = dic["keyout"]
        self.keyin = dic["keyin"]
        self.id = dic["id"]
        self.onetouch = one
        self.bool=False
        self.runbool = False   # トグル状態（ON/OFF）
        self.key_is_down = False

    def switchkeymenu(self):
        if self.bool:
            self.bool=False
        else:
            self.bool=True

    def updaterun(self):
        if self.runbool:
            print(f"{self.id}:Running")
            pydirectinput.keyDown(self.keyout)
        else:
            print(f"{self.id}:Not Running")
            pydirectinput.keyUp(self.keyout)

class keylist:#keyについてのまとめ
    def __init__(self):
        self.key = []
    def update(self,lists):
        self.key = []
        for con in lists["keys"]:
            self.key.append(keys(con,onetouchkey))

class buttonlist:#buttonについてのまとめ
    def __init__(self):
        self.button=[]
        self.check=[]

    def setbutton(self,window,key):
        self.button=[]
        self.check=[]
        for i in key:
            self.button.append(tk.Button(window,text=i.id,command=lambda i=i:self.update(window,key,i)))
            self.check.append(tk.Label(window,text="動作:"+str(i.bool)))

    def update(self,window,keyvalue,thiskey):
        thiskey.switchkeymenu()
        self.check[keyvalue.index(thiskey)]=tk.Label(window,text="動作:"+str(thiskey.bool))
        self.view()

    def view(self):
        for con in self.button:
            con.grid(row=2+self.button.index(con),column=0,columnspan=2,padx=10,pady=10)
        for che in self.check:
            che.grid(row=2+self.check.index(che),column=2,padx=10,pady=10)

def startrun(key, window,func):
    keyboard.unhook_all()
    keyboard.hook(lambda event:func(event,key))
    running(key, window)

def running(key, window):
    for i in key.key:
        if i.runbool:
            pydirectinput.press(i.keyout)

    # 終了キー
    if keyboard.is_pressed(endkey):
        print("End")

        for i in key.key:
            i.runbool = False
            i.key_is_pressed = False
        keyboard.unhook_all()
        return

    window.after(10, lambda: running(key, window))

def switchkey(event,key):
    for k in key.key:
            if k.bool:
                if event.name == k.keyin:
                    if event.event_type == "down":
                        print("keydown")
                        if k.key_is_down:
                            return
                        k.key_is_down = True
                        k.runbool = not k.runbool
                        k.updaterun()
                    elif event.event_type == "up":
                        print("keyup")
                        k.key_is_down = False


def main(configs):#メイン

    def addkey(origin,allkey):#キーを追加する動作
        addkeywindow = tk.Toplevel(origin)
        addkeywindow.title("Add Key")
        idlabel = tk.Label(addkeywindow,text="名前を決めてね")
        keylabel = tk.Label(addkeywindow,text="キーを決めてね")
        entryid = tk.Entry(addkeywindow)
        entrykey = tk.ttk.Combobox(addkeywindow,value=allkey)
        savecontent = tk.Button(addkeywindow,text="Save",command=lambda:savechange(entryid.get(),usekey[entrykey.get()]["pyauto"],usekey[entrykey.get()]["kb"],addkeywindow))
        closewindow = tk.Button(addkeywindow,text="Close",command=addkeywindow.destroy)

        idlabel.grid(row=0,column=0,padx=10,pady=10)
        entryid.grid(row=1,column=0,padx=10,pady=10)
        keylabel.grid(row=0,column=1,padx=10,pady=10)
        entrykey.grid(row=1,column=1,padx=10,pady=10)
        savecontent.grid(row=2,column=0,padx=10,pady=10)
        closewindow.grid(row=2,column=1,padx=10,pady=10)

    def savechange(addname,addkeyout,addkeyin,window):
        with open("config.json","r",encoding="utf-8") as f:
            config = json.load(f)
        config["keys"].append({"id":addname,"keyout":addkeyout,"keyin":addkeyin})
        with open("config.json","w",encoding="utf-8") as g:
            json.dump(config,g,indent=4)
        with open("config.json","r",encoding="utf-8") as f:
            config = json.load(f)
        key.update(config)
        buttons.setbutton(root,key.key)
        buttons.view()
        window.destroy()

    root = tk.Tk()
    root.title("STG Switcher")
    config = configs

    key = keylist()#キーの種類をまとめるリスト
    buttons = buttonlist()#ボタンをまとめるリスト

    key.update(config)

    labelexplain = tk.Label(root, text="シューティングゲームで、キー長押しではなく切り替えをする機能")
    buttonrun = tk.Button(root,text="Run",command=lambda:startrun(key,root,switchkey))
    buttonend = tk.Button(root,text="End",command=sys.exit)
    buttons.setbutton(root,key.key)

    labelexplain.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
    buttonrun.grid(row=1,column=0,padx=10,pady=10)
    buttonend.grid(row=1,column=2,padx=10,pady=10)
    buttons.view()

    root.mainloop()

main(config)