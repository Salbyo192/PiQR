import qrcode

def main():
    print("Enter the Python code you want to encode (single line or small snippet):")
    code = input(">>> ")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(code)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save("python_code_qr.png")
    print("✅ QR code generated and saved as 'python_code_qr.png'")

if __name__ == "__main__":
    main()
