import cv2
from picamera2 import Picamera2
from pyzbar import pyzbar
import time
import os

SERIAL_PORT = "/dev/ttyGS0"
BAUD = 115200

# Wait for host to open serial
time.sleep(3)

# Open serial device as a file (no pyserial)
ser = os.open(SERIAL_PORT, os.O_RDWR | os.O_NOCTTY)

def write_line(text):
    os.write(ser, (text + "\n").encode("utf-8"))
    time.sleep(0.02)

# Camera setup
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)
picam2.start()

print("Pi ready. Waiting for QR code.")

sent = False

while not sent:
    frame = picam2.capture_array()
    codes = pyzbar.decode(frame)

    for code in codes:
        qr_text = code.data.decode("utf-8")

        print("QR detected:")
        print(qr_text)

        write_line("---BEGIN---")
        for line in qr_text.splitlines():
            write_line(line)
        write_line("---END---")

        sent = True
        break

    time.sleep(0.1)

os.close(ser)
picam2.stop()

