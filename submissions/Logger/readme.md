#  Screenshot Logger & Keylogger Payload (HackyDucky)

>  **For educational and ethical penetration testing purposes only**.  
> Use only in **authorized environments** such as personal VMs or CTF labs.

---


This project contains a Python-based **keylogger and screenshot logger**, designed for use in **ethical red team testing**. It logs keystrokes, captures active window titles, and optionally sends logs to a **Discord webhook** at a fixed interval.

Combined with a **USB Rubber Ducky / Flipper Zero** Ducky Script, it simulates a keystroke injection attack to deploy and execute the payload silently.

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `logger.py` | Main keylogger & screenshot capture script |
| `payload.ducky` | Ducky Script to execute the payload from a known path |
| `README.md` | This documentation |

---

## 🧠 Features

- ✅ Keylogging with active window tagging
- 🖼️ (Optional) Screenshot capture (add `pyautogui`)
- 🔁 Sends logs to **Discord webhook**
- 🧠 Captures system info: User, IP, OS
- 📁 Saves logs locally in `%APPDATA%\SysLogger`
- 🧪 Works well inside **VM environments**

---

## ⚙️ Some test preview


<img width="1165" height="949" alt="Screenshot 2025-07-25 160933" src="https://github.com/user-attachments/assets/7832c09a-0271-4543-85b1-501793c357dd" />



