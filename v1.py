from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance
import sqlite3
import RPi.GPIO as GPIO
from time import sleep

# GPIO setup
GREEN_LED = 17
RED_LED = 27
SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up servo motor PWM
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
servo.start(0)  # Start with the servo at 0 position

# Initialize the camera
print("Starting camera...")
picam2 = Picamera2()

# Configure camera resolution and preview
camera_config = picam2.create_preview_configuration(main={"size": (1280, 720)})
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
        qr_image = Image.open(image_name)
        qr_image_gray = qr_image.convert('L')  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(qr_image_gray)
        qr_image_gray = enhancer.enhance(2.0)  # Increase contrast

        decoded_objects = decode(qr_image_gray)
        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print(f"QR Code detected: {qr_data}")

                # Check validity and control LEDs/servo
                if is_valid_qr_code(qr_data):
                    print("The QR code is valid.")
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(RED_LED, GPIO.LOW)
                    servo.ChangeDutyCycle(7.5)  # Move servo to 90°
                    sleep(1)
                    servo.ChangeDutyCycle(0)  # Stop servo movement
                else:
                    print("The QR code is fake or not in the database.")
                    GPIO.output(RED_LED, GPIO.HIGH)
                    GPIO.output(GREEN_LED, GPIO.LOW)
        else:
            print("No QR code detected.")
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
    except Exception as e:
        print(f"Error processing image: {e}")
    finally:
        # Reset LEDs
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.LOW)

# Main loop for capturing images and checking QR codes
print("Press 'c' to capture an image or 'q' to quit.")
try:
    while True:
        user_input = input("Enter 'c' to capture or 'q' to quit: ").strip().lower()
        if user_input == 'c':
            capture_and_process_image()
        elif user_input == 'q':
            print("Exiting...")
            break
finally:
    # Cleanup GPIO and stop camera
    GPIO.cleanup()
    picam2.stop_preview()
    picam2.stop()
    servo.stop()
