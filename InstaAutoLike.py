import keyboard
import mss
import cv2
import numpy as np
from time import time, sleep
import pyautogui

THRESHOLD = 0.99
LIKE_THRESHOLD = 15
LIKE_DAILY_THRESHOLD = 10000
pyautogui.PAUSE = 0

print("Press 'e' to start auto-like")
print("Once started press 'q' to quit")
keyboard.wait('e')
x, y = pyautogui.size()
sct = mss.mss()

like_img = cv2.imread('./like_button.png')

fps_time = time()

dimensions = {
    'left': 0,
    'top': 0,
    'width': x,
    'height': y
}

scr = np.array(sct.grab(dimensions))
size_ratio = x/scr.shape[1]

# cv2.imshow('Screen', scr_remove)

# while True:
#     key = cv2.waitKey(0)
#     if key in [27, ord('q'), ord('Q')]:
#         cv2.destroyAllWindows()

liked_count = 0
liked_total_count = 0

while True:
    scr = np.array(sct.grab(dimensions))
    scr_remove = scr[:, :, :3]
    scr_remove[:int(scr_remove.shape[1]*0.15), :, :] = 0

    result = cv2.matchTemplate(scr_remove, like_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    yloc, xloc = np.where(result >= THRESHOLD)
    
    if liked_total_count > LIKE_DAILY_THRESHOLD:
        break
    elif liked_count > LIKE_THRESHOLD:
        sleep(120)
        liked_count = 0  
    elif len(xloc) > 0:
        pyautogui.click(x=int(xloc[0]*size_ratio), y=int(yloc[0]*size_ratio))
        sleep(.5)
        liked_count += 1
        liked_total_count += 1
    else:
        pyautogui.press('right')
        pyautogui.scroll(-20)
        sleep(1)

    if keyboard.is_pressed('q'):
        break
    sleep(.1)
    fps_time = time()
