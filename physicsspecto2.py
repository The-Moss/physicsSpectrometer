import cv2
import numpy as np
import matplotlib.pyplot as plt
import Rpi.GPIO as GPIO
import time
from picamera2 import Picamera2
# GPIO setup for Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Camera setup for Rasberry pi
picam2 = Picamera2()

#red hues dont show up in the initial graph, you must scroll to the right to see them
def doTheThing():
        # Load the image
        rgb_image = cv2.imread('insert image file here')
        rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        
        # Convert to HSV
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV).astype(np.float32)
        hue = hsv_image[:, :, 0] * 2        # Scale to [0, 360)
        sat = hsv_image[:, :, 1] / 255.0
        val = hsv_image[:, :, 2] / 255.0
        
        # Filter for colorful pixels
        mask = (sat > 0.3) & (val > 0.2)
        filtered_hue = hue[mask]
        
        # Histogram with 360 bins (1 degree per bin)
        bin_edges = np.arange(0, 361)  # 0–360 inclusive
        hist, _ = np.histogram(filtered_hue, bins=bin_edges)
        
        # Map hue bins to wavelength (red = 620 nm, violet = 450 nm)
        wavelengths = 700 - (170 / 360) * np.arange(0, 360)
        
        # Plot only nonzero bins
        nonzero_bins = np.nonzero(hist)[0]
        nonzero_counts = hist[nonzero_bins]
        nonzero_wavelengths = wavelengths[nonzero_bins]
        nonzero_hues = nonzero_bins
        
        # Plot
        fig, ax = plt.subplots(figsize=(9, 3))
        bars = ax.bar(nonzero_wavelengths, nonzero_counts, width=1, align='edge', edgecolor='none')
        
        # Color bars by hue
        for bar, hue_deg in zip(bars, nonzero_hues):
            rgb_color = plt.cm.hsv(hue_deg / 360)
            bar.set_facecolor(rgb_color)
        
        # Axis and appearance
        ax.set_xlim(450, 700)
        ax.set_ylim(0, max(5000, np.max(nonzero_counts)))
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.set_xlabel('Wavelength (nm)', color='white')
        ax.set_ylabel('Bin counts', color='white')
        ax.tick_params(colors='white')
        plt.tight_layout()
        plt.show()
def main():
    print("uhh dude you gotta press the button to start the thing")

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
