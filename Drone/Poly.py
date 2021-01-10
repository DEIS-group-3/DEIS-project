import tello
import logging

# logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
# log = logging.getLogger('Drone app')
# log.info('Starting')

def ployfly(sides):
	for s in range(sides):
		t.forward(100)
		t.rotate_ccw(round(360/sides))
		
		
		
t = tello.Tello()

# try:
	# t.get_battery()
t.takeoff()
ployfly(5)
# except Exception as e:
	# log.error(e)
t.land()
t.get_battery()



