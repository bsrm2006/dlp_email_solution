#!/bin/bash

# Comprehensive DLP Solution Installation

set -e

# Prerequisite checks
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Update system packages
apt update && apt upgrade -y

# Install dependencies
apt install -y \
    python3-pip \
    python3-venv \
    postfix \
    libmilter-dev \
    libsasl2-dev \
    postfix-pcre

# Create virtual environment
python3 -m venv /opt/dlp_email_solution/venv
source /opt/dlp_email_solution/venv/bin/activate

# Install Python dependencies
pip install \
    Flask \
    pymilter \
    SQLAlchemy \
    cryptography \
    email-validator

# Configure Postfix
bash /opt/dlp_email_solution/postfix_integration/postfix_config.sh

# Setup systemd service
cp postfix_integration/dlp_milter.service /etc/systemd/system/
systemctl enable dlp_milter
systemctl start dlp_milter

# Final configuration
echo "DLP Email Solution Installed Successfully!"




