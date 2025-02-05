import pyautogui
# doc: https://pyautogui.readthedocs.io/en/latest/mouse.html#:~:text=A%20tween%20or%20easing%20function,tween%20or%20linear%20easing%20function.

# Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
screenWidth, screenHeight = pyautogui.size() 
print(screenWidth, screenHeight)

# Returns two integers, the x and y of the mouse cursor's current position.
currentMouseX, currentMouseY = pyautogui.position() 
print(currentMouseX, currentMouseY)

# Move the mouse to the x, y coordinates 100, 150.
# pyautogui.moveTo(100, 150)

# # Click the mouse at its current location.
# pyautogui.click() 

# # Click the mouse at the x, y coordinates 200, 220.
# pyautogui.click(200, 220)

# Move mouse 10 pixels down, that is, move the mouse relative to its current position.
# (y, x) for some reason
# pyautogui.move(10, None)

# # Double click the mouse at the position
# pyautogui.doubleClick() 

# # Use tweening/easing function to move mouse over 2 seconds.
# easeInQuad - start off moving slowly and then speeding up towards the destination
# easeOutQuad - starts moving fast but slows down as it approaches the destination
# pyautogui.moveTo(100, 500, duration=2, tween=pyautogui.easeInOutQuad)

# # Type with quarter-second pause in between each key.
# pyautogui.write('Hello world!', interval=0.25) 

# # Simulate pressing the Escape key.
# pyautogui.press('esc')


# pyautogui.keyDown('shift')
# pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.hotkey('ctrl', 'c')


# # pyautogui.alert('This is an alert box. :P')