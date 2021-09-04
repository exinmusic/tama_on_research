import time
from adafruit_ble import BLERadio
from ble_services import TAMAService

import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# DISPLAY STUFF
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

def size_img(image_name):
    image = Image.open(image_name)
    
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
    return image

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

img = size_img('blinka.jpg')

# Display image.
disp.image(img, rotation)
time.sleep(1)
# END DISPLAY STUFF

ble = BLERadio()

def replay(tama_connection, f):
    for i in f.readlines():
        hex_line = i[:-1].decode('utf-8')
        ln = bytes.fromhex(hex_line)
        tama_connection[TAMAService].write(ln)
        print(f"-> {hex_line}")
        time.sleep(.05)

tama_connection = None
# See if any existing connections are providing TAMAService.
if ble.connected:
    for connection in ble.connections:
        if TAMAService in connection:
            tama_connection = connection

print("Scanning...")
while not tama_connection:
    for adv in ble.start_scan():
        print(adv.complete_name)
        if 'TMGC_meets' == adv.complete_name:
            print("found a TAMAService advertisement")
            tama_connection = ble.connect(adv)
            break
    # Stop scanning whether or not we are connected.
    ble.stop_scan()

if tama_connection and tama_connection.connected:

    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    y = top
    draw.text((x, y), "Sending bitcoin to tama...", font=font, fill="#6ffc03")
    disp.image(image, rotation)

    f = open("playback/handshake.txt", "rb")
    replay(tama_connection, f)
    f.close()

    time.sleep(1)

    f = open("playback/new_owned.txt", "rb")
    replay(tama_connection, f)
    f.close()

draw.rectangle((0, 0, width, height), outline=0, fill=0)
y = top
draw.text((x, y), "Done.", font=font, fill="#ff0000")
disp.image(image, rotation)
time.sleep(2)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.image(image, rotation)
backlight.value = False
print('done')