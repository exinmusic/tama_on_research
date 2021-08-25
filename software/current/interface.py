import time
import digitalio
import board
import oled

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

if __name__ == "__main__":
    while True:
        if buttonB.value and not buttonA.value:  # just button A pressed
            oled.print_text('A!', '#FF0000')
            print("A")
        if buttonA.value and not buttonB.value:  # just button B pressed
            oled.print_text('B!', '#00FF00')
            print("B")
        if not buttonA.value and not buttonB.value:  # none pressed
            oled.print_text('WHAT DO YOU WANT FROM ME?', '#0000FF')