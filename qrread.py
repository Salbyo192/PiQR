import cv2

def main():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("📷 Scanning for QR codes containing Python code... (Press 'q' to quit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame from webcam.")
            break

        data, points, _ = detector.detectAndDecode(frame)

        if points is not None:
            points = points[0].astype(int)
            for i in range(len(points)):
                pt1 = tuple(points[i])
                pt2 = tuple(points[(i+1) % len(points)])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        #cv2.imshow("QR Code Scanner", frame)

        if data:
            print(f"\n✅ QR code detected! Executing Python code:\n{data}")
            try:
                exec(data, {})
            except Exception as e:
                print(f"❌ Error executing code: {e}")
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("👋 Exiting scanner.")
            break

    cap.release()
    cv2.destroyAllWindows()

while True: #if __name__ == "__main__":
    main()
