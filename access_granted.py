from picamera2 import Picamera2, Preview

# Initialize the camera
print("Starting camera...")
picam2 = Picamera2()

# Configure camera resolution and preview
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)

# Start the camera with preview
print("Starting preview...")
picam2.start_preview(Preview.QTGL)  # Use QTGL for graphical preview (requires GUI/SSH forwarding)

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
    elif user_input == 'q':
        # Quit the program
        print("Exiting...")
        break

# Stop the camera and preview
picam2.stop_preview()
picam2.stop()
