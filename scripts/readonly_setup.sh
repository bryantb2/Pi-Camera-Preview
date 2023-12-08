#!/bin/bash

# Check if script is running with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

# Define the file path for the read-only script
readonly_script_path="/etc/systemd/system/read-only.service"

# Create a systemd service file for read-only mode
cat << EOF > "$readonly_script_path"
[Unit]
Description=Enable read-only mode

[Service]
Type=oneshot
ExecStart=/bin/mount -o remount,ro /
ExecStop=/bin/mount -o remount,rw /

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to read the new service
systemctl daemon-reload

# Enable the read-only service
systemctl enable read-only

echo "Raspberry Pi configured to boot into read-only mode. Reboot to apply changes."
