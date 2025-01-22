import cv2

# Path to the image you want to scan
image_path = r"D:\coding_projects\python\train thef detection\Eye_on_Board\code.png"  # Use a raw string to avoid escape issues

# Initialize QR code detector
qr_detector = cv2.QRCodeDetector()

# Read the image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print(f"Error: Could not load image from path: {image_path}")
else:
    # Detect and decode QR code
    decoded_text, points, _ = qr_detector.detectAndDecode(image)

    if decoded_text:
        print("QR Code detected:", decoded_text)
    else:
        print("No QR code detected.")
