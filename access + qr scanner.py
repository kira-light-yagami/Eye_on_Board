from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

# List of valid QR codes (you can add any valid QR code data here)
valid_qr_codes = [
    "VALID_QR_CODE_1",
    "VALID_QR_CODE_2",
    "VALID_QR_CODE_3"
]

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

print("Press 'c' to capture an image or 'q' to quit.")
while True:
    user_input = input("Enter 'c' to capture or 'q' to quit: ").strip().lower()
    if user_input == 'c':
        # Capture and save image
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

            # Convert the image to numpy array for OpenCV
            qr_image_cv = np.array(qr_image_gray)

            # Decode QR code from the processed image
            decoded_objects = decode(qr_image_gray)

            if decoded_objects:
                for obj in decoded_objects:
                    qr_data = obj.data.decode("utf-8")
                    print("QR Code detected:", qr_data)

                    # Check if the QR code is in the valid list
                    if qr_data in valid_qr_codes:
                        print("Valid QR Code!")
                    else:
                        print("Fake QR Code detected!")
            else:
                print("No QR code detected.")
        except Exception as e:
            print(f"Error processing image: {e}")
    elif user_input == 'q':
        # Quit the program
        print("Exiting...")
        break

# Stop the camera and preview
picam2.stop_preview()
picam2.stop()
