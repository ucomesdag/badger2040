import os
# import jpegdec
import badger2040

from global_constants import GALLERY_DIRECTORY

# REAMDE = """
# Images must be 296x128 pixel JPEGs

# Create a new "images" directory via Thonny, and upload your .jpg files there.
# """

REAMDE = """
Images must be 296x128 pixel with 1bit colour depth.
You can use examples/badger2040/image_converter/convert.py to convert them:
python3 convert.py --binary --resize image_file_1.png image_file_2.png image_file_3.png
Create a new "images" directory via Thonny, and upload the .bin files there.
"""

display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# jpeg = jpegdec.JPEG(display.display)

# Load gallery images
IMAGES = dict()
TOTAL_IMAGES = dict()
try:
    IMAGES = [
        f for f in os.listdir(f"/{GALLERY_DIRECTORY}") if f.endswith(".bin")
    ]
    TOTAL_IMAGES = len(IMAGES)
except OSError:
    print(f"No images directory found")
    pass

# Blank full size image to write to
full_image = bytearray(int(296 * 128 / 8))

# ------------------------------
#        Gallery functions
# ------------------------------

def show_image(index: int) -> None:

    if TOTAL_IMAGES == 0:
        print(f"No images found. No image will be printed")
        return

    index %= TOTAL_IMAGES
    # jpeg.open_file(f"{GALLERY_DIRECTORY}/{IMAGES[index]}".format(IMAGES[index]))
    open(f"{GALLERY_DIRECTORY}/{IMAGES[index]}", "r").readinto(full_image)

    display.image(full_image)
    display.update()
