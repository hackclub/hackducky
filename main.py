import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

def autofill_login(username, password):
    if not username or not password:
        messagebox.showerror("Input Error", "Please enter both username and password.")
        return

    messagebox.showinfo("Get Ready", "You have 5 seconds to click on the username field.")
    time.sleep(5)

    # Start typing
    pyautogui.write(username, interval=0.1)
    pyautogui.press('tab')
    pyautogui.write(password, interval=0.1)
    pyautogui.press('enter')

username = "hackclub"
password = "Hackducky"

# GUI Setup
root = tk.Tk()
root.title("Auto Login")
root.geometry("300x300")

tk.Label(root, text="Username:").pack(pady=(10, 0))
tk.Label(root, text=f"{username}", font=("Arial", 16), fg="blue").pack(pady=20)

tk.Label(root, text="Password:").pack(pady=(10, 0))
tk.Label(root, text=f"{password}", font=("Arial", 16), fg="blue").pack(pady=20)

autofill_button = tk.Button(root, text="Auto Fill Login", command=lambda: autofill_login(username, password))
autofill_button.pack(pady=20)

root.mainloop()
