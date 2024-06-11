from not_share_values import username, password

import time
import ctypes


# Defining some constants from the Windows API
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
VK_RETURN = 0x0D  # Enter key
VK_SHIFT = 0x10
VK_SPACE = 0x20
VK_BACK = 0x08
VK_RETURN = 0x0D

# Sleep for a few seconds to give time for VRChat to open in windows
time.sleep(5)

# Getting user32.dll library
user32 = ctypes.windll.user32

# Getting screen width and height
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Calculate the center of the screen as we want it to make a random click at center at first to make cursor active in VRChat app.
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Ensuring VRChat is the active window (if the name is different replace 'VRChat' with the actual window title)
# Note: we might need to install the 'pywin32' library but in my case it is already there
try:
    import win32gui
    hwnd = win32gui.FindWindow(None, "VRChat")
    win32gui.SetForegroundWindow(hwnd)
except ImportError:
    print("win32gui not installed, skipping SetForegroundWindow")

# Moveing the cursor to the center of the screen
user32.SetCursorPos(center_x, center_y)
time.sleep(0.1)  # Small delay to ensure the cursor is positioned

# Simulate a left mouse button down event on the center to make the mouse active on VRChat's window 
user32.mouse_event(MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0) # mouse Left click down press
time.sleep(0.01)  # Small delay to ensure the click is registered
user32.mouse_event(MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0) # mouse Left click release press
time.sleep(2)

# Move the cursor to the exact position where we have the login button of VRChat account. 
# We need to adjust if the screen is different and the login button of VRChat account is not exactly in the below defined position.
center_x = int(screen_width / 2) - 100     # on x axis the button of VRChat login is at abit left (100 px left)
center_y = int(screen_height / 2) + 100    # on y axis the button of VRChat login is at abit below (100 px down)
user32.SetCursorPos(center_x, center_y)
time.sleep(0.1)  # Small delay to ensure the cursor is positioned

# Simulating another left mouse button click that actually clicks on the VRChat account button on the VRChat's login UI window.
user32.mouse_event(MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0)
time.sleep(0.01)  # Small delay to ensure the click is registered
user32.mouse_event(MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0)

time.sleep(0.2)

# Once the button of login with VRChat account is clicked by above actions, we need to type in the Username and password
#Simulating the typing of user name and password (please make sure to put your username and password in not_share_values.py)

# Typing:
# Function to simulate key press and release
def keybd_event(key, flag):
    user32.keybd_event(key, 0, flag, 0)

# Mappings for special characters that require Shift
special_char_map = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
    '_': '-', '+': '=', '{': '[', '}': ']', ':': ';', '"': "'", '<': ',', '>': '.', '?': '/', '|': '\\',
    '~': '`'
}

# Mappings for direct special characters
direct_char_map = {
    ' ': VK_SPACE, '.': 0xBE, ',': 0xBC, '/': 0xBF, '\\': 0xDC, ';': 0xBA, '\'': 0xDE,
    '[': 0xDB, ']': 0xDD, '`': 0xC0, '=': 0xBB, '-': 0xBD
}

# Function to type a string (we use it to type username and password in gui of Vrchat automatically)
def type_string(string):
    for char in string:
        if char.isupper() or char in special_char_map:
            keybd_event(VK_SHIFT, 0)  # Press Shift
        if char in special_char_map:
            key = ord(special_char_map[char])
        elif char in direct_char_map:
            key = direct_char_map[char]
        else:
            key = ord(char.upper())
        keybd_event(key, 0)  # Key press
        keybd_event(key, 2)  # Key release
        if char.isupper() or char in special_char_map:
            keybd_event(VK_SHIFT, 2)  # Release Shift
        time.sleep(0.1)  # Add a small delay between each key press

# autotyping username
type_string(username)
print("typed the username")


# Simulating the Enter Pressing action.
user32.keybd_event(VK_RETURN, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_RETURN, 0, 0x0002, 0)
time.sleep(2)


# Simulating typing the password (please replace 'password' with your actual password in the not_share_values.py)
type_string(password)
# SImulating Enter Press after password been typed
user32.keybd_event(VK_RETURN, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_RETURN, 0, 0x0002, 0)

#