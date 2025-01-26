import RPi.GPIO as GPIO
import time
import cv2
import csv
from datetime import date, datetime
from picamera2 import Picamera2, Preview
import numpy as np
import servo_controller  # Import your servo control library

# GPIO setup for LEDs
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
green_led_pin = 17
red_led_pin = 27
servo_pin = 18  # Pin for servo motor

# Set up LED pins
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

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

# QR code detection method
detector = cv2.QRCodeDetector()

# Adding time and date information
today = date.today()
date_today = today.strftime("%d-%b-%Y")

now = datetime.now()
timeRN = now.strftime("%H:%M:%S")

print("Press 'c' to capture an image or 'q' to quit.")
while True:
    user_input = input("Enter 'c' to capture or 'q' to quit: ").strip().lower()
    if user_input == 'c':
        # Capture image using Picamera2
        image_name = "captured_image.jpg"
        print("Capturing image...")
        picam2.capture_file(image_name)
        
        # Read the captured image using OpenCV
        img = cv2.imread(image_name)
        
        # Detect QR code in the image
        data, bbox, _ = detector.detectAndDecode(img)
        
        # If QR code data is found
        if data:
            print("QR Code detected: ", data, date_today, timeRN)
            
            # Write data to CSV file
            try:
                with open('Database.csv', mode='a') as csvfile:
                    csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                    csvfileWriter.writerow([data, date_today, timeRN])
            except Exception as e:
                print("Error writing to CSV file: ", e)
            
            # Control LEDs and Servo based on QR code data
            if data == 'green':
                # Turn on green LED, turn off red LED
                GPIO.output(green_led_pin, GPIO.HIGH)
                GPIO.output(red_led_pin, GPIO.LOW)
                
                # Activate Servo motor
                print("Correct QR code detected. Activating servo motor.")
                servo_controller.move_servo(servo_pin, 90)  # Rotate the servo to 90 degrees (adjust as needed)
                
            elif data == 'red':
                # Turn on red LED, turn off green LED
                GPIO.output(green_led_pin, GPIO.LOW)
                GPIO.output(red_led_pin, GPIO.HIGH)
                
                # Deactivate Servo motor
                print("Incorrect QR code detected. Deactivating servo motor.")
                servo_controller.move_servo(servo_pin, 0)  # Return servo to initial position (0 degrees)
        
        print(f"Image captured and saved as {image_name}.")
        
    elif user_input == 'q':
        # Quit the program
        print("Exiting...")
        break

# Stop the camera and preview
picam2.stop_preview()
picam2.stop()

# Cleanup GPIO
GPIO.cleanup()
