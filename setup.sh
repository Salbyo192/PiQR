#!/bin/bash
set -e

echo "[PiQR] starting setup..."

# -----------------------------
# must be run as root
# -----------------------------
if [ "$EUID" -ne 0 ]; then
  echo "run this script with sudo"
  exit 1
fi

# -----------------------------
# update system
# -----------------------------
echo "[PiQR] updating system..."
apt update
apt upgrade -y

# -----------------------------
# install dependencies
# -----------------------------
echo "[PiQR] installing dependencies..."
apt install -y \
  python3 \
  python3-opencv \
  python3-picamera2 \
  python3-pyzbar \
  wget

# -----------------------------
# enable camera (non-interactive)
# -----------------------------
echo "[PiQR] enabling camera..."
raspi-config nonint do_camera 0

# -----------------------------
# enable USB gadget serial
# -----------------------------
echo "[PiQR] configuring USB gadget serial..."

CONFIG_TXT="/boot/config.txt"
CMDLINE_TXT="/boot/cmdline.txt"

# config.txt
if ! grep -q "dtoverlay=dwc2" "$CONFIG_TXT"; then
  echo "dtoverlay=dwc2" >> "$CONFIG_TXT"
fi

if ! grep -q "enable_uart=1" "$CONFIG_TXT"; then
  echo "enable_uart=1" >> "$CONFIG_TXT"
fi

# cmdline.txt (must stay ONE LINE)
if ! grep -q "g_serial" "$CMDLINE_TXT"; then
  sed -i 's/rootwait/rootwait modules-load=dwc2,g_serial/' "$CMDLINE_TXT"
fi

# -----------------------------
# install script
# -----------------------------
echo "[PiQR] downloading QR reader script..."

INSTALL_DIR="/opt/piqr"
SCRIPT_PATH="$INSTALL_DIR/qr_read.py"

mkdir -p "$INSTALL_DIR"

wget -O "$SCRIPT_PATH" \
  "https://raw.githubusercontent.com/Salbyo192/PiQR/refs/heads/main/qr_read.py"

chmod +x "$SCRIPT_PATH"

# -----------------------------
# systemd service (auto-run)
# -----------------------------
echo "[PiQR] creating systemd service..."

SERVICE_FILE="/etc/systemd/system/piqr.service"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=PiQR QR Code Reader
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
WorkingDirectory=$INSTALL_DIR
StandardOutput=journal
StandardError=journal
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable piqr.service

# -----------------------------
# done
# -----------------------------
echo ""
echo "[PiQR] setup complete!"
echo "[PiQR] rebooting in 5 seconds..."
sleep 5
reboot
