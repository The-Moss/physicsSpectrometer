# importing the cool stuff
import cv2
import numpy as np
import matplotlib.pyplot as plt
import Rpi.GPIO as GPIO
import time
# GPIO setup for Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Camera setup for Rasberry pi
picam2 = Picamera2()

def doTheThing():
    # Load the image from a file
    image_path = "/Users/tomosr/Desktop/Screenshots/spectrum.jpg"  # Replace with the path to image
    frame = cv2.imread(image_path)

    if frame is None:
        print("wrong file pal")
        return

    roi_selected = False

    while True:
        k = cv2.waitKey(1)

        if k & 0xFF == ord('s') and roi_selected:
            shape = cropped.shape
            r_dist = []
            b_dist = []
            g_dist = []
            i_dist = []
        for i in range(shape[1]):
            b_val = np.mean(cropped[:, i][:, 0])  # Blue
            g_val = np.mean(cropped[:, i][:, 1])  # Green
            r_val = np.mean(cropped[:, i][:, 2])  # Red
            i_val = (r_val + b_val + g_val) / 3  # Intensity (mean of all channels)
        
            r_dist.append(r_val)
            g_dist.append(g_val)
            b_dist.append(b_val)
            i_dist.append(i_val)

            plt.subplot(2, 1, 1)
            plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct color display

            plt.subplot(2, 1, 2)
            plt.plot(r_dist, color='r', label='red')
            plt.plot(g_dist, color='g', label='green')
            plt.plot(b_dist, color='b', label='blue')
            plt.plot(i_dist, color='k', label='mean')
            plt.legend(loc="upper left")
            plt.show()

        elif k & 0xFF == ord('r'):
            r = cv2.selectROI("computer, enhance", frame)
            roi_selected = True

        elif k & 0xFF == ord('q'):
            break

        else:
            if roi_selected:
                cropped = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                cv2.imshow('The cool part', cropped)
            else:
                cv2.imshow('The thing', frame)

    cv2.destroyAllWindows()
# actually doing the thing
def main():
    print("uhh dude you gotta press the button to start the thing")
    
    #waits for button to be pressed, then does the thing
    try:
        while True:
            if GPIO.input(17) == GPIO.HIGH:
                picam2.start()
                time.sleep(2)
                picam2.capture_file("spectrum.jpg")
                print("thaks mate, processing the image...")
                doTheThing()
                break
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("uh dude whyd you stop me? dafuq?")

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
