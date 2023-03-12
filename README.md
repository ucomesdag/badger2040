# Badger 2040

This is a minimal implementation of a three button mode for the [Pimoroni Badger 2040](https://shop.pimoroni.com/products/badger-2040).

* Button A accesses the badge mode.
* Button B accesses the QR code mode.
* Button C accesses the gallery mode.

All three modes support image switching by using the up and down buttons.

The current state is saved on to the flash memory, when turned on it will resume from where you where.

All three modes have their own asset folders, and can be set in the `global_constants.py` file.

The text for the QR codes and badges should follow the format of the provided examples. Images for the badge mode should have a resolution of `104x128`. Images for the gallery should have a resolution of `296x128`. They can be converted to the proper binary format using the [`convert.py`](https://github.com/pimoroni/pimoroni-pico/tree/main/examples/badger2040/image_converter) script.

For example:
```
python3 convert.py --binary images/my_image.jpg
```
