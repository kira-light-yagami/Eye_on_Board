from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance
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

print("Press 'c' to capture an image or 'q' to quit.")
while True:
    user_input = input("Enter 'c' to capture or 'q' to quit: ").strip().lower()
    if user_input == 'c':
        # Capture and save image
        image_name = "captured_image.jpg"
        print("Capturing image...")
        picam2.capture_file(image_name)
        print(f"Image captured and saved as {image_name}.")

        # Process the captured image for QR code
        print("Processing the captured image for QR code...")

        try:
            # Open the captured image
            qr_image = Image.open(image_name)

            # Convert to grayscale for better QR code detection
            qr_image_gray = qr_image.convert('L')

            # Enhance image brightness and contrast if needed (optional)
            enhancer = ImageEnhance.Contrast(qr_image_gray)
            qr_image_gray = enhancer.enhance(2.0)  # Increase contrast (adjust if necessary)

            # Convert to numpy array for pyzbar
            qr_image_cv = np.array(qr_image_gray)

            # Decode QR code from the processed image
            decoded_objects = decode(qr_image_cv)

            if decoded_objects:
                for obj in decoded_objects:
                    print("QR Code detected:", obj.data.decode("utf-8"))
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
