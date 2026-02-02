import os
import glob
import termios
import fcntl
import time

BAUD = termios.B115200

def find_pi_serial():
    candidates = []
    candidates += glob.glob("/dev/ttyACM*")        # Linux
    candidates += glob.glob("/dev/tty.usbmodem*")  # macOS

    if not candidates:
        raise RuntimeError("No Pi serial device found")

    # Pick newest device
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]

def open_serial(path):
    fd = os.open(path, os.O_RDWR | os.O_NOCTTY)

    attrs = termios.tcgetattr(fd)
    attrs[0] = 0  # iflag
    attrs[1] = 0  # oflag
    attrs[2] = termios.CS8 | termios.CREAD | termios.CLOCAL
    attrs[3] = 0  # lflag

    attrs[4] = BAUD
    attrs[5] = BAUD

    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)

    return fd

print("Searching for Raspberry Pi...")
port = find_pi_serial()
print(f"Using serial port: {port}")

fd = open_serial(port)

buffer = []
recording = False

while True:
    try:
        data = os.read(fd, 1024).decode("utf-8", errors="ignore")
    except BlockingIOError:
        time.sleep(0.05)
        continue

    for line in data.splitlines():
        line = line.strip()

        if line == "---BEGIN---":
            buffer = []
            recording = True
            continue

        if line == "---END---":
            code = "\n".join(buffer)
            print("\nReceived code:\n")
            print(code)
            print("\nExecuting...\n")

            #VERY DANGEROUS — controlled environment only
            exec(code, {"__builtins__": __builtins__}, {})

            os.close(fd)
            exit(0)

        if recording:
            buffer.append(line)

