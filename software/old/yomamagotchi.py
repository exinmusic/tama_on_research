import logging
import time
import uuid
import Adafruit_BluefruitLE
from os import system

# Enable debug output.
#logging.basicConfig(level=logging.DEBUG)
system('clear')
print("          __O__")
print("        .'     '.")
print("      .'         '.")
print("     .  _________  .")
print("     : |         | :")
print("    :  |  8===D  |  :")
print("    :  |  OWNED  |  :")
print("    :  |_________|  :")
print("     |             |")
print("     '   O     O   '")
print("      ',    O    ,'")
print("        '.......'")
print('     TAMAGOSASAYAKI\n-----------------------\n    written by XN\n')

# Define service and characteristic UUIDs used by the TAMA service.
BATTERY_SERVICE_UUID   = uuid.UUID('0000180F-0000-1000-8000-00805F9B34FB')
TAMA_SERVICE_UUID      = uuid.UUID('0000FFF0-0000-1000-8000-00805F9B34FB')
TX_UUID                = uuid.UUID('0000FFF2-0000-1000-8000-00805F9B34FB')
RX_UUID                = uuid.UUID('0000FFF1-0000-1000-8000-00805F9B34FB')



# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

def main():
	# Clear both bluez and CoreBluetooth cached data.
	ble.clear_cached_data()

	# Get the first available BLE network adapter and make sure it's powered on.
	adapter = ble.get_default_adapter()
	adapter.power_on()
	print('Found a dongle to use: {0}'.format(adapter.name))

	# Disconnect any currently connected UART devices.  Good for cleaning up and
	# starting from a fresh state.
	print('Washing hands from the last Tamagotchi...')
	ble.disconnect_devices([TAMA_SERVICE_UUID])

	# Scan for TAMA devices.
	print('Searching for a new Tamagotchi to mess with...')
	try:
		adapter.start_scan()
		# Search for the first UART device found (will time out after 60 seconds
		# but you can specify an optional timeout_sec parameter to change it).
		device = ble.find_device(name='TMGC_meets')
		if device is None:
			raise RuntimeError('Can\'t find any Tamagotchi friends...')
	finally:
		# Make sure scanning is stopped before exiting.
		adapter.stop_scan()
	print('Found a friend!')
	device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
					  # to change the timeout.

	# Once connected do everything else in a try/finally to make sure the device
	# is disconnected when done.
	try:
		# Wait for service discovery to complete for at least the specified
		# service and characteristic UUID lists.  Will time out after 60 seconds
		# (specify timeout_sec parameter to override).
		print('Discovering services...')
		device.discover([TAMA_SERVICE_UUID,BATTERY_SERVICE_UUID], [TX_UUID, RX_UUID])
		#device.discover()
		# Find the TAMA service and its characteristics.
		btry = device.find_service(BATTERY_SERVICE_UUID)
		tama = device.find_service(TAMA_SERVICE_UUID)
		time.sleep(1)
		if btry:
			print('Discovered Battery Service: {0}'.format(btry))
		if tama:
			print('Discovered Tama Service: {0}'.format(tama))

		print('Discovering characterisitics...')
		rx = tama.find_characteristic(RX_UUID)
		tx = tama.find_characteristic(TX_UUID)


		# Function to receive RX characteristic changes.  Note that this will
		# be called on a different thread so be careful to make sure state that
		# the function changes is thread safe.  Use queue or other thread-safe
		# primitives to send data to other threads.
		def received(data):
			print('<----------- {0}'.format(data.encode('hex')))

		# Turn on notification of RX characteristics using the callback above.
		print('Subscribing to FFF1...\n')
		rx.start_notify(received)

		# Write a string to the TX characteristic.
		print('Shaking hands with this thing...\n-----------------------\n')

		f = open("/Users/david/Desktop/raw/handshake.txt", "rb")  # log.txt file has line separated values, 
		tx.write_value('')
		for i in f.readlines():
			ln = i.replace("\n","").decode('hex')
			tx.write_value(ln)
			print('-> '+ln.encode('hex'))
			time.sleep(.07)
		
		#print('Talk to me bitch...')
		time.sleep(2)
		#tx.write_value('f08e0d'.decode('hex'))
		#print('-> f08e0d')
		#time.sleep(.07)
		tx.write_value('f08d'.decode('hex'))
		print('-> f08d')
		time.sleep(2)
		print('Attempting transfer...')

		f = open("/Users/david/Desktop/raw/upload_02.txt", "rb")  # log.txt file has line separated values, 
		tx.write_value('')
		for i in f.readlines():
			ln = i.replace("\n","").decode('hex')
			tx.write_value(ln)
			print('-> '+ln.encode('hex'))
			time.sleep(.07)	

		# Now just wait for 30 seconds to receive data.
		time.sleep(3)
		print('Keep the change ya filthy animal!')
		print(':P')
		time.sleep(10)
	finally:
		# Make sure device is disconnected on exit.
		device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)