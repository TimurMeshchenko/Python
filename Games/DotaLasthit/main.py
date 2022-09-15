import time
import keyboard
import pyautogui
import win32api
import win32con

time.sleep(5)


def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    time.sleep(0.1)

    

while not keyboard.is_pressed('q'):
    def locateScreen(png):
        start = pyautogui.locateCenterOnScreen('D:\Python\Games\Dota\{}'.format(png), region=(612, 355, 657, 409), confidence=0.8)
        if start is not None:
            pyautogui.moveTo(start[0], start[1] + 30)
            click()
        
    locateScreen('highHp.png')
    locateScreen('mediumHp.png')
    
