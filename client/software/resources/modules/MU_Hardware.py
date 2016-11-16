from multiprocessing import Process, Queue
from panda3d.core import *
from direct.showbase.MessengerGlobal import messenger
import serial
from hardware_auto_find import *
 
class HW_support:
	def hardware_event_handler(self, port_num = 'auto'):
		try:
			port_list = serial_ports()
			if serial_ports():
				port_num = port_list[0] if port_num == 'auto' else port_num
				self.hardware_port = serial.Serial(port_num, 115200)
			else:
				messenger.send('HW_ERROR', ['HW_NOT_FOUND'])
				print("Could not open Serial port")
				return
		except:
			messenger.send('HW_ERROR', ['HW_NOT_FOUND'])
			print("Could not open Serial port")
			return
		
		while True:
			try:
				input_data = self.hardware_port.readline()
				if input_data:
					messenger.send('HW_SERIAL', ['CARD_READ'])
					print(input_data)
					event_case = input_data[:8]
					event_data = input_data[9:]
				
					if event_case == 'CARD_IN': #Card reader signal
						messenger.send('HW_SERIAL', ['CARD_READ'])
					elif event_case == 'CTRL_IN': #Input signal
						messenger.send('HW_SERIAL', ['TOUCH_IN'])
					
					elif event_case == 'ERR_HW_': #Error Handling
						messenger.send('HW_ERROR', ['ERROR_CARD'])
					else: #If event is unknown, let's just ignore it.
						pass
			except Exception as e:
				print e
		return