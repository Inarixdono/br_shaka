import pyautogui, webbrowser
from time import sleep

webbrowser.open('https://web.whatsapp.com/send?phone=8099158938')
sleep(5)
with open('span.txt','r') as file:
    for line in file:
        pyautogui.typewrite(line)
        pyautogui.press('enter')