#!/bin/bash
# setup-dev-env.sh – Configure a new developer's local environment

set -e

# Configuration
DEV_USER="$1"
DEV_HOME="/home/$DEV_USER"

if [ -z "$DEV_USER" ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

# Check if user exists
if ! id "$DEV_USER" &>/dev/null; then
    echo "Creating user: $DEV_USER"
    sudo useradd -m -s /bin/bash "$DEV_USER"
    echo "Set password for $DEV_USER:"
    sudo passwd "$DEV_USER"
fi

# Install common developer tools (RHEL example)
echo "Installing developer tools..."
sudo dnf groupinstall -y "Development Tools" 2>/dev/null || echo "Group not found"

# Add user to groups
echo "Adding user to required groups..."
sudo usermod -aG wheel,docker,dev "$DEV_USER"

# Clone configuration repository (if exists)
if [ -d "/etc/config-repo" ]; then
    sudo -u "$DEV_USER" git clone /etc/config-repo "$DEV_HOME/config"
fi

# Set up Git config
sudo -u "$DEV_USER" git config --global user.name "$DEV_USER"
sudo -u "$DEV_USER" git config --global user.email "$DEV_USER@example.com"

echo "Environment setup complete for $DEV_USER"
echo "User can now log in and start developing."