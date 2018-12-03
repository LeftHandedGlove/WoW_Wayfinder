import pyautogui
import time

# When turning with keypresses,
# the game will turn the character a certain distance no matter the duration when the duration is short.
# There is also some uncertainty when doing long duration key presses
# However the difference is fairly small and can be corrected with a feedback loop

# Using mouse click and drag seems to break the game for some reason

keypress_duration_360 = 1.8
keypress_duration_10 = keypress_duration_360 / 36
mouse_movement_360 = 50 * 1
delay = (mouse_movement_360 / 100) * 0.5
pyautogui.PAUSE = 0.025

time.sleep(5)

for i in range(0, 100):
    pyautogui.keyDown(key='right')
    pyautogui.keyUp(key='right')
    time.sleep(0.5)

exit(0)

for i in range(0, mouse_movement_360):
    pyautogui.mouseDown(button='right')
    pyautogui.moveRel(xOffset=50, yOffset=0, duration=0)
    pyautogui.mouseUp(button='right')



exit(0)

pyautogui.keyDown(key='right')
time.sleep(0.1)
pyautogui.keyUp(key='right')
time.sleep(0.5)
pyautogui.keyDown(key='right')
time.sleep(0.01)
pyautogui.keyUp(key='right')
time.sleep(0.5)
pyautogui.keyDown(key='right')
time.sleep(0.2)
pyautogui.keyUp(key='right')
time.sleep(0.5)
pyautogui.keyDown(key='right')
pyautogui.keyUp(key='right')


exit(0)

for i in range(0, 36):
    pyautogui.keyDown("left")
    time.sleep(keypress_duration_10)
    pyautogui.keyUp("left")
    time.sleep(0.05)

exit(0)

pyautogui.keyDown(key='right')
time.sleep(keypress_duration_360)
pyautogui.keyUp(key='right')
time.sleep(0.5)
pyautogui.keyDown(key='left')
time.sleep(keypress_duration_360)
pyautogui.keyUp(key='left')
