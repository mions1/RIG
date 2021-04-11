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
		
	def get_total_tardiness(self):
		""" Restituisce la tardiness totale per questa macchina.
		    La tardiness è calcolata come max{C_i - D_i, 0}, dove:
			    - C_i è il tempo di completamento del job
				- D_i è il due time
			In questo caso, avendo multi-spec setup-time, viene anche tenuto conto
			del tempo di setup tra due job successivi

		Returns:
			int: tardiness totale dello schedule corrente di questa macchina
		"""

		total_tardiness = 0
		c_i = 0
		prev_job = None
		for job in self._jobs:
			# per ogni job, calcolo il completition time come il tempo in cui 
			# sono finiti tutti i job precedenti, più l'eventuale setup time
			c_i += job._processing_time + Job.get_setup_time(prev_job, job)
			# calcolo la tardiness del job e la sommo alla totale
			t_i = max([c_i-job._due_date, 0])
			total_tardiness += t_i
			# il prev_job mi servirà per calcolare l'eventuale setup time
			# col successivo
			prev_job = job
		
		return total_tardiness

	def get_free_time(self):
		""" Ritorna il momento nel quale la macchina si libera.
		    Essendo un multi-spec setup time, tiene conto anche di quello.

		Returns:
			int: completition time della macchina, quindi quando si libera
		"""

		c_total = 0
		prev_job = None
		# per ogni job calcolo il completition time e lo sommo per avere il totale
		# che sarà il tempo in cui la macchina si libererà
		for job in self._jobs:
			c_total += job._processing_time + Job.get_setup_time(prev_job, job)
			prev_job = job

		return c_total


	@staticmethod
	def get_total_tardiness_per_machine(machines: list):
		""" Restituisce la tardiness totale per ogni macchina

		Args:
			machines (list): lista delle macchine

		Returns:
			list: tardiness totale per ogni macchina
		"""

		tardiness = []
		for k in machines:
			tardiness.append(k.get_total_tardiness())
			
		return tardiness

	
	@staticmethod
	def get_machine_with_min_c(machines: list):
		""" Ritorna la macchina col completition time più basso tra quelle passate.
			Vedere get_free_time()

		Args:
			machines (list): lista di macchine

		Returns:
			Machine: macchina col completition time minore
		"""
		
		min_c_machines = dict()
		for k in machines:
			# per ogni macchina, calcolo il completition time (aka quando si libera)
			min_c_machines[k] = k.get_free_time()

		# ordino le macchine in ordine crescente per il completition time e restituisco
		# la prima, poiché sarà quella col completition time più basso
		min_c_machines = dict(sorted(min_c_machines.items(), key=lambda item: item[1]))
		for k,v in min_c_machines.items():
			min_c_machine = k
			break
		
		return min_c_machine

	@staticmethod
	def first_machine_avaible(machines: list):
		""" Ritorna la prima macchina che si libera.
		    Vedere get_free_time()

		Args:
			machines (list): lista di macchine

		Returns:
			Machine: prima macchina che si libea
		"""

		processing_time_per_machine = dict()
		
		for k in machines:
			# per ogni macchina calcolo il completition time
			processing_time_per_machine[k] = k.get_free_time()
		
		min_sum_processing_time = processing_time_per_machine[machines[0]]
		min_k = machines[0]
		# restituisco la macchina col completition time minore (aka quella che si libera prima)
		for k in machines:
			if min_sum_processing_time > processing_time_per_machine[k]:
				min_sum_processing_time = processing_time_per_machine[k]
				min_k = k
		
		return min_k
		
	@staticmethod
	def free_machine_at_t(machines: list, t: int):
		""" Restituisce la macchina libera al tempo t.
		    Se più di una, restituisce quella con meno jobs.
			Vedere get_free_time()

		Args:
			machines (list): lista di macchine
			t (int): tempo

		Returns:
			Machine: macchina libera al tempo t
		"""

		processing_time_per_machine = dict()
		
		for k in machines:
			# per ogni macchina calcolo il completition time (aka quando si libera)
			processing_time_per_machine[k] = k.get_free_time()

		# salvo in free_machines la lista delle macchine che sono libere al tempo t
		free_machines = []
		for k in machines:
			if t >= processing_time_per_machine[k]:
				free_machines.append(k)

		# se ce ne sono una o più, restituisco quella che finisce prima
		if free_machines:
			return Machine.get_machine_with_min_c(free_machines)

		# se non ce ne sono di libere al tempo t, restituisco quella che si libera prima
		return Machine.first_machine_avaible(machines)

	def __str__(self):
		return str(self._id_number)
