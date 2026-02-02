# PiQR

> pronounced "piker"

i am very sleep deprived

Works on:

- macOS
- Linux

No dependencies are required on your host other than the support script.

---

## ⚠️ READ THIS OR REGRET IT

This project **literally executes code from a QR code**.

That means:

- Do NOT scan random QR codes
- Do NOT plug this into random computers
- Do NOT blame me if you nuke your laptop

Use this for **learning, trolling friends (with consent of course), or controlled chaos only**.

---

## How This Works

```
[ QR Code ]
     ↓
[ Pi Camera ]
     ↓
[ Raspberry Pi Zero ] --USB--> [ Your Computer ]
                                      ↓
                                 runs Python
```

The Pi pretends to be a **USB serial device**, like an Arduino, and uses a Pi camera to read qr codes that you can generate and pass the code read to your host machine.

---

## Stuff You Need

### Hardware

- Raspberry Pi Zero
- Pi Camera (v1 or v2)
- MicroSD card (8GB+)
- USB cable (Pi Zero **data** port, not power-only)
- A computer running macOS or Linux

### Software

- Raspberry Pi OS (Lite or Desktop)
- Python3 (already installed on most systems)

---

## 🐧 Step 1: Set Up Raspberry Pi OS

Flash Raspberry Pi OS onto the SD card.

Enable:

- SSH (optional but recommended)

Boot the Pi.

---

## Step 2: Prep on the Pi

Run this command on the Pi (make sure you have internet):

```bash
sudo bash -c "$(curl -fsSL https://github.com/Salbyo192/PiQR/releases/download/Testing/setup.sh)"
```

---

## Step 3: Computer setup

Download the serial\_exec.py file from the releases section.

---

## Step 4: Generating the QR Codes.

Download qrgen.py from the releases page and run it with python3.\
It will ask you for a python one-liner and generate a QR code in the same directory as the script. Print it out or something.

---

## 🚀 Step 5: Run It

### On your computer

```bash
python3 serial_exec.py
```

### Plug in the Pi (USB data port)

---

## Known Issues

- Camera not detected → enable it in `raspi-config`
- No serial device → wrong USB port or bad cable
- macOS permissions → allow terminal USB access

