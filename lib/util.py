from skimage.feature import match_template
import numpy as np 
import cv2
import pyautogui

def make_screenshot(x, y, w, h):
   return pyautogui.screenshot(region=(x, y, w, h))

def template_match(needle, haystack):
   result = match_template(haystack, needle)
   ij = np.unravel_index(np.argmax(result), result.shape)
   x, y = ij[1], ij[0]
   score = result[y, x]
   return x, y, score

def clip(value, max=1, min=-1):
   if value > max:
      value = max
   if value < min:
      value = min
   return value

def is_image_dark(image):
   gray = cv2.cvtColor(np.float32(image), cv2.COLOR_RGB2GRAY)
   blur = cv2.blur(gray, (32, 32))
   if cv2.mean(blur)[0] > 90:
      return False 
   else:
      return True