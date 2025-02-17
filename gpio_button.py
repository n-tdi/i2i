import RPi.GPIO as GPIO
import time
import cv2

# Pin definitions
button_pin = 17  # Change to the GPIO pin you're using

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up pull-up resistor

cam = cv2.VideoCapture(0)

def buttonPressed():
    print("Pressed!")
    ret, image = cam.read()
    cv2.imwrite('/home/nikkasouza/testimage.jpg', image)
    


try:
    while True:
        button_state = GPIO.input(button_pin)
        
        if button_state == GPIO.LOW:  # Button is pressed (since it's pulled up)
            buttonPressed()
            while button_state == GPIO.LOW:
                button_state = GPIO.input(button_pin)
                time.sleep(0.1)
        time.sleep(0.1)  # Debouncing delay

except KeyboardInterrupt:
    pass  # Clean up when Ctrl+C is pressed

finally:
    GPIO.cleanup()  # Reset GPIO settings

