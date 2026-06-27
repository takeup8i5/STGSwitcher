# STGSwitcher
STGで一度キーを押すだけでキーが押され続け、もう一度押すことで解除されるプログラムを作りたかった(Windows用)  
Shiftがあまりうまく動かないかも

**必要なライブラリ**
* pyautogui
* pydirectinput
* keyboard  


#ターミナルで入れる
```
pip install pyautogui
```
```
pip install pydirectinput
```
```
pip install keyboard
```  
  
  
**config_limited.jsonで使うキーの設定**
* "id"で表示される名前
* "keyoutで出力するキー
* "keyin"でどのキーが押された時に"keyout"のキーを押し続けるか
* "keys.json"のpyautoがkeyoutに対応(最初はpyautoを使おうとしていた),kbが"keyin"に対応
