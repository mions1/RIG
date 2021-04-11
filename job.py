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

	@staticmethod
	def get_max_processing_time(jobs: list):
		""" Restituisce il job col max processing time.
		    Utile ad implementare la regola HPT first

		Args:
			jobs (list): lista dei jobs

		Returns:
			Job: job col max processing time
		"""

		max_p = jobs[0]._processing_time
		max_j = jobs[0]
		for job in jobs:
			if max_p < job._processing_time:
				max_p = job._processing_time
				max_j = job
		
		return max_j

	@staticmethod
	def get_min_due_date(jobs: list):
		""" Restituisce il job col due date minore.
		    Utile per implementare la regola EDD.

		Args:
			jobs (list): lista dei jobs

		Returns:
			Job: job col due date minore
		"""

		min_dd = jobs[0]._due_date
		min_j = jobs[0]
		for job in jobs:
			if min_dd > job._due_date:
				min_dd = job._due_date
				min_j = job
		
		return min_j
	
	@staticmethod
	def get_setup_time(job_1, job_2):
		""" Restituisce il setup time eventuale tra due job consecutivi

		Args:
			job_1 (Job): job precedente a job_2
			job_2 (Job): job successivo a job_1

		Returns:
			int: setup time tra job_1 e job_2
		"""
		
		# se job_1 non ha il successivo o se job_2 non ha un precedente, setuptime=0
		if not job_1 or not job_2:
			return 0

		setup_1 = job_1._specs
		setup_2 = job_2._specs
		
		setup_time = 0
		# calcolo il setuptime come la somma dei setup time delle spec per cui
		# job_1 e job_2 hanno value diverso
		for i in range(len(setup_1)):
			if setup_1[i]._value != setup_2[i]._value:
				setup_time += setup_1[i]._setup_time
	
		return setup_time
		
	@staticmethod
	def get_processing_time_avg(jobs: list):
		""" Restituisco la media dei processing time dei jobs.
	    	Usata per calcolare, ad es, ATCS

		Args:
			jobs (list): lista di jobs

		Returns:
			float: media dei processing time dei jobs passati
		"""

		total_processing_time = 0
		for job in jobs:
			total_processing_time += job._processing_time
			
		return total_processing_time/len(jobs)
		
	@staticmethod
	def get_Na(job, jobs: list, spec_name: str):
		""" Restituisce il numero di jobs che hanno il valore della spec "spec_name" 
			uguale al valore della stessa specifica in "job".
			Usato per calcolare APD.

		Args:
			job (Job): job di riferimento
			jobs (list): lista di jobs da confrontare
			spec_name (str): nome della specifica selezionata

		Returns:
			int: numero di jobs che hanno stesso valore di spec_name di job
		"""
		
		na = 0
		for j in jobs:
			if j != job:
				for i in range(len(job._specs)):
					if job._specs[i]._name == spec_name:
						if job._specs[i]._value == j._specs[i]._value:
							na += 1
						break
						
		return na
					
		
	def __str__(self):
		return str(self._id_number)+"\t"+str(self._processing_time)+"\t"+str(self._due_date)
