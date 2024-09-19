import cv2
import numpy as np
import pyttsx3

def detect_color_band(frame):
    try:
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges
        color_ranges = {
            'brown': ((10, 100, 20), (20, 255, 200)),
            'green': ((40, 40, 40), (80, 255, 255)),
            'blue': ((90, 100, 20), (130, 255, 255)),
            'yellow': ((20, 100, 20), (30, 255, 255))
        }

        # Iterate through color ranges
        for color, (lower, upper) in color_ranges.items():
            # Create masks for each color
            mask = cv2.inRange(hsv_frame, lower, upper)

            # Check if any pixel is present in the mask
            if cv2.countNonZero(mask) > 0:
                return color  # Return the detected color band

        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def speak_year(color_band):
    # Speech dictionary
    year_speech = {
        'brown': "This student is from first year.",
        'green': "This student is from second year.",
        'blue': "This student is from third year.",
        'yellow': "This student is from fourth year."
    }

    # Initialize text to speech engine
    engine = pyttsx3.init()

    # Set properties before adding things to say
    engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Adding the text to speech engine
    engine.say(year_speech.get(color_band, "Unable to determine the year."))

    # Run and wait until finished
    engine.runAndWait()

if __name__ == "__main__":
    # Open video capture device (0 is the default webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        # Detect color band
        color_band = detect_color_band(frame)

        if color_band is not None:  # Check if color_band is not None
            print(f"Detected color band: {color_band}")
            speak_year(color_band)
        else:
            print("No valid color band detected.")

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()
