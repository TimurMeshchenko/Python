from pyautogui import *


def locateScreen(png):
    x, y = locateCenterOnScreen(r'C:\Users\Admin\Desktop\WindowsConfig\png\{}'.format(png), region=(0,0, 1920, 1080), confidence=0.9)
    click(x, y)


def runBox(exe):
    hotkey('win', 'r')
    write(exe)
    press('enter')



def fileExplorerOptions():
    runBox('rundll32.exe shell32.dll, Options_RunDLL 0')
    press('down')

    [locateScreen('checkMark.png') for i in range(0, 2)]
    locateScreen('viewButton.png')
    locateScreen('emptyCircle.png')
    locateScreen('hideExtensions.png')
    locateScreen('apply.png')
    locateScreen('exit.png')


def keyboardOptions():
    runBox('control main.cpl keyboard')
    time.sleep(.5)
    locateScreen('fast.png')
    press('tab')
    press('right', interval=.01, presses=20)
    locateScreen('apply.png')
    locateScreen('exit.png')


def mouseOptions():
    runBox('control main.cpl')
    time.sleep(.5)
    locateScreen('pointer.png')
    press('right')
    locateScreen('checkMark.png')
    locateScreen('apply.png')
    locateScreen('exit.png')

def display():
    runBox('desk.cpl')
    time.sleep(1)
    press('down', interval=.01, presses=5)
    time.sleep(1)
    locateScreen('displaySettings.png')
    time.sleep(1)
    press('down', interval=.01, presses=2)
    time.sleep(1)
    locateScreen('refresh.png')
    locateScreen('144hz.png')
    locateScreen('customizeExit.png')
    
def customize():
    runBox('Control Desktop')
    time.sleep(2)
    locateScreen('picture.png')
    locateScreen('color.png')
    locateScreen('colors.png')
    time.sleep(1)
    locateScreen('custom.png')
    locateScreen('dark.png')
    time.sleep(3)
    locateScreen('customizeExit.png')
    

customize()
time.sleep(2)
fileExplorerOptions()
keyboardOptions()
mouseOptions()
display()


