import pyautogui

def make_screenshot(x, y, w, h):
    return pyautogui.screenshot(region=(x, y, w, h))