import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# ST7789 DISPLAY:
disp = st7789.ST7789(
    board.SPI(),
    cs=digitalio.DigitalInOut(board.CE0),
    dc=digitalio.DigitalInOut(board.D25),
    rst=None,
    baudrate=64000000,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)

# VARIABLES
height = disp.width 
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
padding = -2
top = padding
bottom = height - padding
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()

def sized_img(image_name):
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

def print_text(text_input:str, text_color:str)->None:
    '''
    Writes out a string on the oled screen.
    Second argument is a hex color value for the text.
    '''
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    y = top
    draw.text((0, y), text_input, font=font, fill=text_color)
    disp.image(image, rotation)

#Display image
def display_image(img_name:str)->None:
    '''
    Displays an image on the oled screen.
    '''
    disp.image(sized_img(img_name), rotation)


if __name__ == "__main__":
    from time import sleep
    # turn backlight
    backlight.value = True

    # display text
    print_text('Hello world!', '#00FF00')

    sleep(2)

    # Display image.
    display_image('kustama.jpg')

    sleep(2)

    # display text
    print_text('Good bye cruel world...', '#FF0000')

    sleep(2)

    # Display image.
    display_image('pic2.jpg')