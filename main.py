import time
import badger2040
import time
import state_handling

from global_constants import (
    BATTERY_TIMER
)

import badge, qrgen, gallery, battery

display = badger2040.Badger2040()


def update_content(state: dict) -> None:
    mode = state["mode"]

    if mode == "badge":
        badge.draw_badge(state[mode + "_index"])

    if mode == "qr":
        qrgen.draw_qr_file(state[mode + "_index"])

    if mode == "gallery":
        gallery.show_image(state[mode + "_index"])

    if mode == "battery":
        battery.show_status()


def buttons_abc(state: dict) -> bool:
    button_a = machine.Pin(badger2040.BUTTON_A).value()
    button_b = machine.Pin(badger2040.BUTTON_B).value()
    button_c = machine.Pin(badger2040.BUTTON_C).value()

    if any([button_a, button_b, button_c]):

        if button_a and not button_c:
            state["mode"] = "badge"
            print("button_a")

        if button_c and not button_a:
            state["mode"] = "gallery"
            print("button_c")

        if button_b:
            state["mode"] = "qr"
            print("button_b")

        if button_a and button_c:
            state["mode"] = "battery"
            print("button_a+c")
            wait_for_user_to_release_buttons()

        return True

    return False


def buttons_updown(state: dict) -> bool:
    button_up = machine.Pin(badger2040.BUTTON_UP).value()
    button_down = machine.Pin(badger2040.BUTTON_DOWN).value()

    mode = state["mode"]
    if mode != "battery":
        if button_up:
            state[mode+"_index"] += 1
            print("button_up")

        if button_down:
            state[mode+"_index"] -= 1
            print("button_down")

        if button_up or button_down:
            return True

    return False


def wait_for_user_to_release_buttons():
    pr = display.pressed
    while pr(badger2040.BUTTON_A) or pr(badger2040.BUTTON_B) or pr(badger2040.BUTTON_C) or pr(badger2040.BUTTON_UP) or pr(badger2040.BUTTON_DOWN):
        time.sleep(0.01)


def main_loop():
    state = state_handling.state_defaults()
    if not state_handling.state_load("main", state):
        update_content(state)

    start_time = time.time()

    woken_by_button = badger2040.woken_by_button()

    while True:

        if woken_by_button:
            start_time = time.time()
            display.led(128)
            woken_by_button = False

        if buttons_abc(state) or buttons_updown(state):
            update_content(state)
            start_time = time.time()
            state_handling.state_modify("main", state)
            print(open('/state/main.json').read())

        current_time = time.time()

        if current_time - start_time > BATTERY_TIMER:
            display.led(0)
            display.halt()


# ------------------------------
#       Main program
# ------------------------------

if __name__ == "__main__":
    main_loop()
