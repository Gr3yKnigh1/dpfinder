class event(object):

	def __init__(self):
		self.__funcs = set()

	def invoke(self, *args):
		for f in self.__funcs:
			f.__call__(*args)

	def reg(self, func):
		self.__funcs.add(func)
