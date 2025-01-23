from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance, ImageOps
import sqlite3
import numpy as np

# Initialize the camera
print("Starting camera...")
picam2 = Picamera2()

# Configure camera resolution and preview
camera_config = picam2.create_preview_configuration(main={"size": (1280, 720)})  # Higher resolution for better QR detection
picam2.configure(camera_config)

# Start the camera with preview
print("Starting preview...")
picam2.start_preview(Preview.QTGL)
picam2.start()

# Function to check QR code validity from the database
def is_valid_qr_code(qr_data):
    conn = sqlite3.connect('qr_codes.db')
    cursor = conn.cursor()

    # Check if the QR code data exists in the database
    cursor.execute('''
    SELECT * FROM scanned_qr_codes WHERE qr_data = ?
    ''', (qr_data,))
    
    qr_code = cursor.fetchone()
    conn.close()

    # Return True if QR code exists in the database, otherwise False
    return qr_code is not None

# Function to capture and process the image
def capture_and_process_image():
    image_name = "captured_image.jpg"
    print("Capturing image...")
    picam2.capture_file(image_name)
    print(f"Image captured and saved as {image_name}.")

    # Process image for QR code
    print("Processing image for QR code...")

    try:
        # Open the captured image
        qr_image = Image.open(image_name)

        # Convert to grayscale
        qr_image_gray = qr_image.convert('L')

        # Enhance image brightness and contrast if needed (optional)
        enhancer = ImageEnhance.Contrast(qr_image_gray)
        qr_image_gray = enhancer.enhance(2.0)  # Increase contrast (tune this value if necessary)

        # Decode QR code from the processed image
        decoded_objects = decode(qr_image_gray)

        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print(f"QR Code detected: {qr_data}")

                # Check if the QR code is valid by comparing with the database
                if is_valid_qr_code(qr_data):
                    print("The QR code is valid.")
                else:
                    print("The QR code is fake or not in the database.")
        else:
            print("No QR code detected.")
    except Exception as e:
        print(f"Error processing image: {e}")

# Main loop for capturing images and checking QR codes
print("Press 'c' to capture an image or 'q' to quit.")
while True:
    user_input = input("Enter 'c' to capture or 'q' to quit: ").strip().lower()
    if user_input == 'c':
        capture_and_process_image()
    elif user_input == 'q':
        # Quit the program
        print("Exiting...")
        break

# Stop the camera and preview
picam2.stop_preview()
picam2.stop()
