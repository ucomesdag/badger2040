import os
import qrcode
import badger2040

from global_constants import QR_CODE_DIRECTORY, WIDTH, HEIGHT

TOTAL_CODES = dict()
CODES = dict()
# Load all available QR Code Files
try:
    CODES = [
        f for f in os.listdir(f"/{QR_CODE_DIRECTORY}") if f.endswith(".txt")
    ]
    TOTAL_CODES = len(CODES)
except OSError:
    print(f"No QR codes found")
    pass

code = qrcode.QRCode()

display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# ------------------------------
#        QR Code Functions
# ------------------------------


def measure_qr_code(size: int, code: qrcode.QRCode):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox: int, oy: int, size: int, code: qrcode.QRCode) -> None:
    size, module_size = measure_qr_code(size, code)
    display.pen(15)
    display.rectangle(ox, oy, size, size)
    display.pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(
                    ox + x * module_size, oy + y * module_size, module_size, module_size
                )


def draw_qr_file(index: int = 0) -> None:
    display.led(128)

    if TOTAL_CODES == 0:
        print(f"No QR codes found. Code will not be printed.")
        return

    index = index % TOTAL_CODES
    file = CODES[index]
    codetext = open(f"{QR_CODE_DIRECTORY}/{file}", "r")

    lines = codetext.read().strip().split("\n")
    code_text = lines.pop(0)
    title_text = lines.pop(0)
    detail_text = lines

    # Clear the Display
    display.pen(15)  # Change this to 0 if a white background is used
    display.clear()
    display.pen(0)

    code.set_text(code_text)
    size, _ = measure_qr_code(128, code)
    left = top = int((HEIGHT / 2) - (size / 2))
    draw_qr_code(left, top, 128, code)

    left = 128 + 5

    # Draw a border around the screen and code
    display.pen(0)
    display.thickness(1)
    display.line(0, 0, WIDTH - 1, 0)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)
    display.line(0, 0, 0, HEIGHT - 1)
    display.line(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(128, 0, 128, HEIGHT - 1)

    # Draw black box around name
    display.thickness(26)
    display.line(128 + 13, 13, WIDTH - 1, 13)

    # Draw the header
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("bitmap6")
    display.thickness(1)
    display.text(title_text, left, 3, 3)

    # Draw detail lines
    display.thickness(1)
    display.pen(0)
    display.font("bitmap8")

    detail_size = 8.0  # A sensible starting scale
    detail_sample = ""
    for line in detail_text:
        if len(detail_sample) < len(line):
            detail_sample = line
    while True:
        detail_length = display.measure_text(detail_sample, detail_size)
        if detail_length >= (WIDTH - 128) and detail_size >= 0.1:
            print(str(detail_length) + " - " + str(detail_size))
            detail_size -= 0.01
        else:
            break

    top = 32
    for line in detail_text:
        display.text(line, left, top, detail_size)
        top += int((12 * detail_size) / 2) + 2

    # Draw box around bottom line
    display.thickness(26)
    display.line(128 + 13, HEIGHT - 11, WIDTH - 1, HEIGHT - 11)

    # Draw text for last details line
    display.font("bitmap6")
    display.thickness(1)
    display.pen(15)
    display.text("Scan the code!", left, HEIGHT - 19, 2)

    display.update()


# Main programme for testing purposes
if __name__ == "__main__":
    draw_qr_file()
