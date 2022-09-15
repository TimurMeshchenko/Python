from pyautogui import *
import pyautogui
import time
import keyboard
import win32api
import win32con

time.sleep(2)

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

while keyboard.is_pressed('q') == False:
    flag = 0
    pic = pyautogui.screenshot(region=(251, 171, 1303, 677))
    width, height = pic.size

    for x in range(0, width, 5):
        for y in range(0, height, 5):

            r, g, b = pic.getpixel((x, y))
            if r == 94 and g == 50 and b == 37:
                flag = 1
                click(x+251, y+171)
                time.sleep(0.05)
                break
        if flag == 1:
            break

