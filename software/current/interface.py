import time
import digitalio
import board
import oled

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

def now()->str:
    '''
    Returns a, b, ab, or none as str types based on buttons currently pressed.
    '''
    status = ''
    if buttonB.value and not buttonA.value:  # button A pressed
        status = 'a'
    if buttonA.value and not buttonB.value:  # button B pressed
        status = 'b'
    if not buttonA.value and not buttonB.value:  # both pressed
        status = 'ab'
    return status

oled.backlight.value = True

if __name__ == "__main__":
    while True:
        if now() == 'a':
            oled.print_text('A!', '#FF0000')
        if now() == 'b':
            oled.print_text('B!', '#00FF00')
        if now() == 'ab':
            oled.print_text('make up your mind.', '#0000FF')