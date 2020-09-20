import threading
import time
class Countdown(threading.Thread):
    """ Counter thread which counts down to zero in one second intervals """
    def __init__(self,runtime = 60):
    	threading.Thread.__init__(self)

    	self.counter = runtime
		# self.start()
	def run(self):
		while self.counter>0:
			print (self.counter time.sleep(1) self.counter -= 1)
			print('%s finished'%(self.name))
			
	# create two countdown objects
	# method of the Thread class
	# don’t start thread automatically
c1 = Countdown(50)
c2 = Countdown(100)
# start threads by calling the threads’ run() methods c1.start()
c2.start()
# pause program execution until both threads have finished c1.join()
c2.join()