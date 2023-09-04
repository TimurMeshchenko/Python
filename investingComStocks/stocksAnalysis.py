from pyautogui import *
import keyboard

def showStockMax():
    if keyboard.is_pressed('a'):
        x, y = locateCenterOnScreen(r'D:\Python\investingComStocks\Max.png', region=(0,0, 1920, 1080), confidence=0.75)
        click(x, y)  

def closeLastSitePage():
    if keyboard.is_pressed('s'):
        allCrossesOnScreen = list(locateAllOnScreen(r'D:\Python\investingComStocks\closeSite.png', region=(0,0, 1920, 1080), confidence=0.96))
        lastCrossOnScreen = allCrossesOnScreen[len(allCrossesOnScreen) - 1]
        x, y, _, _ = lastCrossOnScreen

        click(x, y)   

def openStocksNPages():
    if keyboard.is_pressed('d'):
        distanceToStockName: int = 30
        allStocksNamesInScreen = list(locateAllOnScreen(r'D:\Python\investingComStocks\russiaFlag.png', region=(0,0, 1920, 1080), confidence=0.96))
        
        for i in range(21):
            if (i >= len(allStocksNamesInScreen)): return

            stockNameInScreen = allStocksNamesInScreen[i]
            x, y, _, _ = stockNameInScreen

            keyDown('ctrl')
            click(x + distanceToStockName, y)
            keyUp('ctrl')  


while (True):
    showStockMax()
    closeLastSitePage()
    openStocksNPages()




