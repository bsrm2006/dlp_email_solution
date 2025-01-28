
#!/bin/bash

# DLP Solution Uninstallation Script

set -e

# Ensure script is run with sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Stop and disable services
systemctl stop dlp_milter || true
systemctl disable dlp_milter || true

# Remove systemd service
rm -f /etc/systemd/system/dlp_milter.service

# Remove project directory
rm -rf /opt/dlp_email_solution

# Restore original Postfix configuration
if [ -f /etc/postfix/main.cf.backup ]; then
    mv /etc/postfix/main.cf.backup /etc/postfix/main.cf
fi

if [ -f /etc/postfix/master.cf.backup ]; then
    mv /etc/postfix/master.cf.backup /etc/postfix/master.cf
fi

# Remove Postfix DLP user
userdel postfix_dlp || true

# Reload systemd
systemctl daemon-reload
systemctl restart postfix

echo "DLP Solution Uninstalled Successfully!"