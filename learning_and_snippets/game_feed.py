import win32gui
import mss.tools
import numpy

sct = mss.mss()
top_buffer = 31
other_buffer = 7

def get_game_frame():
    region = win32gui.GetWindowRect(win32gui.FindWindow(None, "World of Warcraft"))
    left, top, right, bottom = region
    region = left + other_buffer, top + top_buffer, right - other_buffer, bottom - other_buffer
    img = numpy.array(sct.grab(region))
    return img


