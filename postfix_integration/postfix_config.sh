#!/bin/bash

# Postfix DLP Configuration Script

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Backup existing Postfix configuration
cp /etc/postfix/main.cf /etc/postfix/main.cf.backup
cp /etc/postfix/master.cf /etc/postfix/master.cf.backup

# Configure Postfix for Milter Integration
postconf -e "milter_default_action = accept"
postconf -e "milter_protocol = 6"
postconf -e "smtpd_milters = inet:localhost:8000"
postconf -e "non_smtpd_milters = inet:localhost:8000"
postconf -e "milter_macro_daemon_name = ORIGINATING"

# Create Postfix User for DLP
useradd -r -s /sbin/nologin postfix_dlp

# Set appropriate permissions
chmod 755 /etc/postfix/postfix_dlp_milter.py
chown postfix_dlp:postfix /etc/postfix/postfix_dlp_milter.py

# Restart Postfix
systemctl restart postfix

echo "Postfix DLP configuration completed successfully!"


