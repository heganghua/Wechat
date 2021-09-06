# -*- coding: utf-8 -*-
import pyautogui


# print(3//2)

coords = pyautogui.locateOnScreen("./more.png")
print(coords)
print(coords.left)
print(coords.top)
