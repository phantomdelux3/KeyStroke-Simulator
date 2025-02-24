import time
import tkinter as tk
from threading import Thread
from pynput.keyboard import Controller, Key

# Initialize keyboard controller
keyboard = Controller()

# Global variable to control typing
typing_active = False

# Read text from a .txt file
def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.rstrip("\n") for line in file]  # Remove extra newlines

# Simulate keystrokes using pynput
def type_text(lines):
    global typing_active
    delay = 60 / 10  # Adjust for 50 WPM

    for line in lines:
        if not typing_active:
            print("Typing stopped.")
            return  # Stop typing if stopped externally

        # Move cursor to the beginning of the line
        keyboard.press(Key.home)
        keyboard.release(Key.home)
        time.sleep(0.1)

        for char in line:
            if not typing_active:
                return

            keyboard.type(char)
            time.sleep(delay / 60)  # Adjust for natural typing speed

        # Press enter after typing each line
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.1)

    print("\nTyping simulation completed.")

# Start typing function
def start_typing():
    global typing_active
    typing_active = True
    start_button.config(text="Stop Typing", command=stop_typing)  # Change button text
    time.sleep(5)  # 5-second delay before starting
    print("Typing started...")

    lines = read_txt("type.txt")  # Read lines from type.txt
    type_text(lines)

# Stop typing function
def stop_typing():
    global typing_active
    typing_active = False
    start_button.config(text="Start Typing", command=lambda: Thread(target=start_typing).start())  # Reset button

# GUI Setup
def create_gui():
    global start_button  
    root = tk.Tk()
    root.title("Typing Simulator")
    
    # Make the window stay on top
    root.attributes("-topmost", True)

    start_button = tk.Button(root, text="Start Typing", command=lambda: Thread(target=start_typing).start(), height=2, width=15)
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
