import os
import badger2040

from global_constants import HEIGHT, WIDTH, BADGE_DIRECTORY

# ------------------------------
#      Badge settings
# ------------------------------

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 0.6
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

DEFAULT_TEXT = """mustelid inc
H. Badger
RP2040
2MB Flash
E ink
296x128px
/badges/badge.jpg
"""

# ------------------------------
#      Badge functions
# ------------------------------

DICT_BADGE_IMAGES = dict()
BADGE_IMAGES = dict()

TOTAL_BADGES = dict()
BADGES = dict()
# Load all available badges
try:
    BADGES = [
        f
        for f in os.listdir(f"/{BADGE_DIRECTORY}/")
        if f.endswith(".txt")
    ]
    TOTAL_BADGES = len(BADGES)
except OSError:
    print(f"No badges found")
    pass

display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# ------------------------------
#      Utility functions
# ------------------------------


# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge(index: int = 0, full_update: bool = True) -> None:

    if TOTAL_BADGES == 0:
        print(f"No badges found. No badge will be printed")
        return

    index %= TOTAL_BADGES
    with open(f"/{BADGE_DIRECTORY}/{BADGES[index]}", "r") as f:
        company = f.readline()
        name = f.readline()
        detail1_title = f.readline()
        detail1_text = f.readline()
        detail2_title = f.readline()
        detail2_text = f.readline()
        badge_image_file = f.readline()

    # Truncate all of the text (except for the name as that is scaled)
    company = truncatestring(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)

    detail1_title = truncatestring(
        detail1_title, DETAILS_TEXT_SIZE, TEXT_WIDTH
    )
    detail1_text = truncatestring(
        detail1_text,
        DETAILS_TEXT_SIZE,
        TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    )

    detail2_title = truncatestring(
        detail2_title, DETAILS_TEXT_SIZE, TEXT_WIDTH
    )
    detail2_text = truncatestring(
        detail2_text,
        DETAILS_TEXT_SIZE,
        TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE)
    )

    # Blank badge image to write to before drawing:
    badge_image = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))

    if badge_image_file == "":
        print(f"No badge image file found")
    else:
        open(f"{badge_image_file}", "rb").readinto(badge_image)

    display.pen(0)
    display.clear()

    # Draw badge image
    display.image(badge_image, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Uncomment this if a white background is wanted behind the company
    # display.pen(15)
    # display.rectangle(1, 1, TEXT_WIDTH, COMPANY_HEIGHT - 1)

    # Draw the company
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("serif")
    display.thickness(2)
    display.text(company, LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, COMPANY_TEXT_SIZE)

    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(name, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(name, (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 1, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    name_length = display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)
    display.text(detail1_text, 5 + name_length + DETAIL_SPACING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)

    # Draw the second detail's title and text
    display.thickness(2)
    name_length = display.measure_text(detail2_title, DETAILS_TEXT_SIZE)
    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)
    display.text(detail2_text, LEFT_PADDING + name_length + DETAIL_SPACING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)

    display.update()


# Main programme for testing purposes
if __name__ == "__main__":
    draw_badge()
