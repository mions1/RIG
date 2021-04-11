import numpy as np
import math
from random import randint
from copy import deepcopy
from machine import Machine
from spec import Spec
from job import Job
from utilities import print_d, print_schedule, print_schedule_d

# ------------ Utilità comuni ------------------------
def LPT(jobs: list):
	""" Ritorna la lista dei jobs in ordine dal più lungo al più corto
	    in riferimento al processing time (LPT)

	Args:
		jobs (list): lista dei job

	Returns:
		list: lista dei job in ordine LPT
	"""
	
	maxes = []
	while jobs:
		tmp_max = Job.get_max_processing_time(jobs)
		maxes.append(tmp_max)
		jobs.remove(tmp_max)

	return maxes

def EDD(jobs: list):
	""" Ritorna la lista dei jobs in ordine EDD, ovvero in ordine crescente
	    per la due date

	Args:
		jobs (list): lista dei jobs

	Returns:
		list: lista dei jobs in ordine EDD
	"""

	minies = []
	while jobs:
		tmp_min = Job.get_min_due_date(jobs)
		minies.append(tmp_min)
		jobs.remove(tmp_min)
	
	return minies

def EDD_m(jobs: list, machines: list):
	""" Carica il primo job per ogni macchina seguendo l'ordine EDD

	Args:
		jobs (list): lista dei job
		machines (list): lista delle macchine
	"""

	for machine in machines:
		tmp_min = Job.get_min_due_date(jobs)
		machine._jobs.append(tmp_min)
		jobs.remove(tmp_min)

# ------------ Scheduler 0 - Corrente ----------------
def step_1_sched_corrente(jobs: list, machines: list):
	""" Il primo step dello scheduler corrente consiste nell'assegnare alle macchine
	    i job in ordine dal più lungo (in termini di processing time) al più corto

	Args:
		jobs (list): lista di jobs
		machines (list): lista di macchine

	Returns:
		list: lista di macchine aggiornata allo step1
	"""

	# ordino la lista dei jobs in ordine decrescente per processing time
	lpt = LPT(jobs)
	# assegno i primi job delle macchine
	for k in machines:
		k._jobs.append(lpt[0])
		lpt.remove(lpt[0])
		
	print_d("\nStep 1 scheduler corrente", 1)

	print_d("\nPrimi due job con processing time maggiore")
	print_d(str(machines[0]._jobs[0]), 1)
	print_d(str(machines[1]._jobs[0]), 1)
	
	# assegno ogni job ancora non schedulato alla prima macchina libera
	for job in lpt:
		k = Machine.first_machine_avaible(machines)
		k._jobs.append(job)
	
	print_schedule_d(machines, 1)
		
	return machines

def step_2_sched_corrente(machines: list):
	""" Il secondo step dello scheduler corrente consiste nel ri-ordinare lo schedule
	    di ogni macchina, calcolato tramite lo step 1, in ordine EDD

	Args:
		machines (list): lista di macchine
	"""
	
	# per ogni macchina, assegno alla macchina la sua lista dei jobs ordinata
	# con la regola EDD
	for k in machines:
		mins_dd = EDD(k._jobs)
		k._jobs = mins_dd
		
	print_d("Step 2 scheduler corrente", 1)
	print_schedule_d(machines, 1)


from datas import setup_times, specs_list, jobs, machines

# ------------------------SCHEDULING CORRENTE----------------------------------
# scheduling corrente - prendo dati
jobs_0 = deepcopy(jobs)
machines_0 = deepcopy(machines)

print("------ Scheduler 0 - Corrente ----------")
	# step 1 - Assegno alle macchine i job dal più lungo al più corto
step_1_sched_corrente(jobs_0, machines_0)

	# step 2 - Per ogni macchina, ri-ordino lo schedule in ordine EDD
step_2_sched_corrente(machines_0)

	# risultato
print("Risultato per scheduling corrente")
tardiness = Machine.get_total_tardiness_per_machine(machines_0)
print_schedule(machines_0)
print("Tardiness totale: ", str(max(tardiness)))
