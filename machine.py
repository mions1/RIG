import random
from copy import deepcopy
from job import Job

class Machine():
	""" Descrive una macchina in un sistema di macchine parallele identiche.
		Una macchina è descritto da:
			- un numero identificativo 
			- una lista di jobs appartenenti al suo schedule, inizialmente vuota

	"""

	def __init__(self, id_number):
		""" 

		Args:
			id_number (int): il numero della macchina
		"""
		self._id_number = id_number
		# lista dei jobs ordinati per schedule di questa macchina
		self._jobs = []
		
	def __str__(self):
		return str(self._id_number)
