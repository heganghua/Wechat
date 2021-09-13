# -*- coding: utf-8 -*-
import pyautogui
from subprocess import check_output
import psutil

# print(3//2)
# print(map(int,check_output(["pidof", "WeChat"]).split()))
process_list = list(psutil.process_iter())
for item in process_list:
    # print(item.name(), item.pid)
    if item.name() == "WeChat.exe":
        print(item.pid)

# coords = pyautogui.locateOnScreen("./more.png")
# print(coords)
# print(coords.left)
# print(coords.top)
