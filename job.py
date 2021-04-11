class Job():
	""" Descrive un job.
	    Il job è descritto da: 
			- un numero identificativo
			- una lista di specs, essendo un multi-spec setup time
			- un processing time
			- un due time

	"""
	
	def __init__(self, id_number: int, specs: list, processing_time: int, due_date: int):
		"""
		Args:
			id_number (int): numero identificativo del job
			specs (list): lista delle specs
			processing_time (int): processing time del job
			due_date (int): due date del job
		"""

		self._id_number = id_number
		self._specs = specs
		self._processing_time = processing_time
		self._due_date = due_date
					
		
	def __str__(self):
		return str(self._id_number)+"\t"+str(self._processing_time)+"\t"+str(self._due_date)
