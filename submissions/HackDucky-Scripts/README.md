# 🦆 HackDucky-Scripts

**Author**: Devaansh Pathak  
**License**: MIT  
**Last Updated**: July 2025

## Overview

**HackDucky-Scripts** is a curated arsenal of automated payload scripts designed for **USB Rubber Ducky**, **BadUSB**, or **MalDuino** devices. Each script is tailored for ethical hacking, system automation, sysadmin provisioning, and developer environment setups. The scripts are written in DuckyScript 1.0 (compatible with standard interpreters) and optimized for Windows 10/11 machines.

> ⚠️ **Disclaimer**: These scripts are intended strictly for educational, ethical, and personal use only. Misuse may violate laws and policies. Use responsibly.

---

## 📁 Included Payloads

### 1. `devkit_injector.txt` — Full Dev Environment Setup

🛠 Installs a complete developer workstation from scratch:

- **Languages/Tools**: Git, Node.js, Python, VS Code, Docker, WSL2, Windows Terminal  
- **Packages**: Global Python + Node.js dev tools  
- **Git Setup**: Aliases, config, SSH keygen  
- **VS Code Extensions**: Python, ESLint, Docker, Live Server  
- **Directories & Boilerplate Projects**  
- **System Tweaks**: Power plan, dark mode  
- **Final Action**: Locks workstation when complete

### 2. `payload_generator.txt` — Offensive Payload Lab

💣 Builds a stealthy offensive lab with payload automation:

- **Repos**: Clones 20+ GitHub red team/payload frameworks  
- **Payload Builder**: Python script to generate encoded reverse shells  
- **Encoders & Droppers**: Auto-BAT files, PowerShell loaders  
- **Keylogger**: Stealth Python-based keystroke logger  
- **USB Drop Folder**: Simulates autorun payload deployment  
- **Desktop Shortcuts**: Quick launcher scripts  
- **Final Touch**: Drops decoy resume and logs message

### 3. `priv_guardian.txt` — Windows Privacy Hardening

🛡️ Deep privacy and anti-telemetry script:

- **Uses O&O ShutUp10++** with pre-configured policy  
- **Kills Telemetry Services & Schedules**  
- **Registry Hardenings**: Disable Cortana, Feedback, Ads  
- **Firewall Blocks**: Known MS telemetry IPs  
- **Installs**: Brave, Simplewall, BleachBit  
- **Custom DNS**: Cloudflare (1.1.1.1)  
- **Final Action**: Cleanup + Restart

### 4. `sys_admin_essentials.txt` — Elite Admin + Red Team Toolkit

⚙️ Powerful terminal-focused sysadmin stack:

- **Core Tools**: Windows Terminal, PowerToys, Process Hacker, Nmap  
- **WSL2 & Ubuntu**: With oh-my-posh + Nerd Fonts + aliases  
- **VS Code Setup**: Extensions for remote + cloud dev  
- **DevOps**: Docker CLI, Terraform, AWS CLI, Azure CLI, GitHub CLI  
- **Red Team Tools**: Metasploit, BloodHound, SQLMap, Hashcat  
- **Automation**: Daily tasks, logging scripts, profile mods

### 5. `web_stack_bomber.txt` — Web Dev MEVN + LAMP + Docker

🌐 Installs full-stack web development toolkit:

- **Stacks**: MEVN, LAMP, Docker, WSL2  
- **Services**: MongoDB, MySQL, Apache, PHP, NGINX  
- **Frontend Tools**: Vue CLI, Express, PM2  
- **Live Dev**: ngrok, localtunnel, live-server  
- **Dockerized Projects**: Prebuilt docker-compose.yml  
- **GitHub CI Integration**: Basic GitHub Actions setup  
- **Bonus**: Sample MEVN + LAMP project scaffolding

---

## 🧑‍💻 Usage

1. Flash script(s) using the **USB Rubber Ducky encoder** or **MalDuino payload uploader**
2. Plug into a target Windows system
3. Let it auto-run and watch the magic (ensure admin privileges where needed)

> ⏱ Scripts use `DELAY` carefully for realistic timing. You may adjust delays depending on system performance.

---

## 💼 Educational Use Cases

- Dev setup on fresh Windows machines
- Building payload testing labs
- Cybersecurity & red team training
- Hardening personal systems for privacy
- Automating sysadmin provisioning

---

## 📢 Contributing

Got an idea or want to improve a payload? PRs are welcome! Fork the repo, modify or add your `.txt` script, and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for more details.

---

## 🧠 Author

Built with 💻 by **Devaansh Pathak**  
🔗 GitHub: [@devaansh-pathak](https://github.com/devaanshpathak)

---