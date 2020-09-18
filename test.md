class Bicycle:
	def __init__(self):
		self.wheels=2
bike=Bicycle()

def count_wheels(obj):
	try:
		print obj.wheels
	except AttributeError as e:
		print 'This object doesn't seem to have wheels'
count_wheels(bike)