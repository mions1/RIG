import numpy as np
import math
from random import randint
from copy import deepcopy
from machine import Machine
from spec import Spec
from job import Job
from utilities import print_d, print_schedule, print_schedule_d, print_schedule_detailed

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

# ------------ Scheduler 1 - ATCS --------------------
def ATCS(jobs, machines, setup_times, tao=0.9, R=0.2):
	""" Calcola l'ATCS index, che tiene conto dei setup times, oltre che
		il processing time ed il due date

	Args:
		jobs (list): [description]
		machines (list): [description]
		setup_times (list): [description]
		tao (float, optional): [description]. Defaults to 0.5.
		R (float, optional): [description]. Defaults to 0.8.
	"""
	# calcolo s come media dei setup times
	# calcolo p come media dei processing times
	s = Spec.get_setup_time_avg(setup_times)
	p = Job.get_processing_time_avg(jobs)

	# calcolo parametri di ATCS
	K1 = 1.2*np.log(len(jobs)/len(machines))-R
		#if tao<0.5 or (nano<0.5 and micro>0.5):
	if tao<0.5:
		K1 -= 0.5
	A2 = 1.8 if tao<0.8 else 2.0
	K2 = tao/(A2*math.sqrt(s/p))
	wi = 1

	U = deepcopy(jobs)

	print_schedule_d(machines, 2)
	
	# Step 1 - Prendo la macchina libera al tempo t, poi
	# Per ogni job non schedulato:
	#	a. Calcolo l'ATCS index
	#	b. Assegno alla macchina selezionata il job con ATCS_APD index maggiore
	print_d("Index ATCS:", 2)
	while U:
		I_i = dict()
		# prendo la macchina libera al tempo t
		k = Machine.first_machine_avaible(machines)
			# job_j è l'ultimo job processato dalla macchina selezionata. Serve per il setup time
		job_j = k._jobs[-1] if k._jobs else None
		# a. calcolo l'ATCS index
		for job_u in U:
			tmp_machine = deepcopy(k)
			tmp_machine._jobs.append(job_u)
			t = tmp_machine.get_free_time()
			I_i[job_u] = ((wi/job_u._processing_time)*math.exp(-max(job_u._due_date-job_u._processing_time-t, 0)/(K1*p))*math.exp(- Job.get_setup_time(job_j,job_u)/(K2*s)))

		I_i = dict(sorted(I_i.items(), key=lambda item: item[1], reverse=True))

		# b. assegno alla macchina il job con index maggiore alla macchina
		for j in I_i:
			print_d(j, 2)
			k._jobs.append(j)
			U.remove(j)
			break	

	print_d("Scheduling ATCS:", 2)
	print_schedule_d(machines, 2)

# ------------ Scheduler 2 - ATCS_APD ----------------
def ATCS_APD(jobs: list, machines: list, setup_times: list, tao:float=0.5, R:float=0.8):
	""" ATCS_APD mette insieme l'ATCS index e l'APD, dato che APD tiene conto
		in maniera più precisa dei setup times

	Args:
		jobs (list): [description]
		machines (list): [description]
		setup_times (list): [description]
		tao (float, optional): [description]. Defaults to 0.5.
		R (float, optional): [description]. Defaults to 0.8.
	"""

	# calcolo s come media dei setup times
	# calcolo p come media dei processing times
	s = Spec.get_setup_time_avg(setup_times)
	p = Job.get_processing_time_avg(jobs)

	# calcolo parametri di ATCS
	K1 = 1.2*np.log(len(jobs)/len(machines))-R
		#if tao<0.5 or (nano<0.5 and micro>0.5):
	if tao<0.5:
		K1 -= 0.5
	A2 = 1.8 if tao<0.8 else 2.0
	K2 = tao/(A2*math.sqrt(s/p))
	wi = 1

	U = deepcopy(jobs)

	print_schedule_d(machines, 2)

	# step 0 -  Calcolo l'APD per ogni job e setto t=0
	apds = APD(U, setup_times)
	t = 0
	
	# Step 1 - Prendo la macchina libera al tempo t, poi
	# Per ogni job non schedulato:
	#	a. Calcolo l'ATCS_APD index
	#	b. Assegno alla macchina selezionata il job con ATCS_APD index maggiore
	#	c. Imposto t come il loading machine
	print_d("Index APD_ATCS:", 3)
	while U:
		I_i = dict()
		# prendo la macchina libera al tempo t
		k = Machine.free_machine_at_t(machines, t)
			# job_j è l'ultimo job processato dalla macchina selezionata. Serve per il setup time
		job_j = k._jobs[-1] if k._jobs else None
		# a. calcolo l'ATCS_APD index
		for job_u in U:
			apd_i = apds[job_u]
			I_i[job_u] = ((wi/job_u._processing_time)*math.exp(-max(job_u._due_date-job_u._processing_time-t, 0)/(K1*p))*math.exp(- Job.get_setup_time(job_j,job_u)/(K2*s))*math.exp(-1/(apd_i*s)))

		I_i = dict(sorted(I_i.items(), key=lambda item: item[1], reverse=True))

		# b. assegno alla macchina il job con index maggiore alla macchina
		for j in I_i:
			# c. imposto il tempo t al loading time
			t = k.get_free_time() + Job.get_setup_time(job_j, j)
			print_d(j, 3)
			k._jobs.append(j)
			U.remove(j)
			break	

	print_d("Scheduling APD_ATCS:", 3)
	print_schedule_d(machines, 3)

def APD(jobs, setup_times):
	""" Calcolo APD index.
	    APD è un indice che prende in considerazione anche i setup times, 
		oltre che il processing time e il due date

	Args:
		jobs (list): lista di jobs
		setup_times (list): lista dei setup times

	Returns:
		dict: dizionario che contine il valore apd per ogni job
	"""
	
	apd = dict()
	for job in jobs:
		tmp = 0
		for setup_name, setup_time in setup_times.items():
			tmp += setup_time * Job.get_Na(job,jobs,setup_name) * job._due_date
		apd[job] = np.log(tmp)/job._processing_time
		
	#dict(sorted(apd.items(), key=lambda item: item[0]))

	return apd

# ------------ Scheduler 3 - ATCS_APD + Greedy -------
def RIG(jobs, machines, setup_times, l_max=100000):
	""" Scheduler Random Iterated Greedy.
	    Utilizza l'ATCS_APD insieme ad una metauristica Greedy per trovare
		una soluzione ottima

	Args:
		jobs (list): lista dei jobs
		machines (list): lista delle macchine
		setup_times (list): lista dei setup times
		l_max (int, optional): iterazioni massime. Defaults to 100000.

	Returns:
		list: lista delle macchine con lo scheduler aggiornato
	"""
	EDD_m(jobs, machines)
	ATCS_APD(jobs, machines, setup_times)

	tardiness_iniziale = max(Machine.get_total_tardiness_per_machine(machines))
	switch = False
	l = 0
	best_sol = [tardiness_iniziale, machines]
	while l < l_max:
		# scambio a caso due jobs
		if switch:
			tardiness_now = max(Machine.get_total_tardiness_per_machine(machines))
			if tardiness_now < best_sol[0]:
				best_sol[0] = tardiness_now
				best_sol[1] = deepcopy(machines)
				if tardiness_now == 52:
					return best_sol

		if not switch:
			Machine.exchange_jobs(machines)
			l += 1

		#print(l/l_max*100,"%")
		desc_type = randint(1,2)
		cons_type = randint(1,3)
		job = descruction(desc_type, machines)
		new_xes = construction(cons_type, job, machines)
		switch, machines = movement(machines, new_xes)

	print("Tardinss iniziale: ", tardiness_iniziale)
	return best_sol

def descruction(desc_type, machines):

	if desc_type == 1:
		# seleziono a random un job dalla macchina con max Cmax
		max_c_machine = Machine.get_machine_with_max_c(machines)
		return max_c_machine.get_random_job()	

	elif desc_type == 2:
		# seleziono a random un job da tutte le macchine
		return Machine.get_random_job_among_all(machines)

def construction(cons_type, job: Job, machines):
	# appendi tutte le macchine, sono solo quella modificata

	new_xes = []
	if cons_type == 1:
		# inserisci il job in qualunque posizione della macchina dalla quale viene
		for k in machines:
			if k.is_job_of_this_machine(job):
				for pos in range(len(k._jobs)):
					all_m = [machine for machine in machines if machine != k]
					tmp_cpy = deepcopy(k)
					j = Job.get_job_with_id(tmp_cpy._jobs, job._id_number)
					tmp_cpy._jobs.remove(j)
					tmp_cpy._jobs.insert(pos, j)
					all_m.append(tmp_cpy)
					new_xes.append(all_m)
				
				return new_xes

	elif cons_type == 2:
		# inserisci il job in tutte le posizione della macchina dalla quale viene e dalla macchina col minor Cmax
		k_min_c = Machine.get_machine_with_min_c(machines)
		for k in machines:
			if k.is_job_of_this_machine(job):
				for pos in range(len(k._jobs)):
					all_m = [machine for machine in machines if machine != k]
					tmp_cpy = deepcopy(k)
					j = Job.get_job_with_id(tmp_cpy._jobs, job._id_number)
					tmp_cpy._jobs.remove(j)
					tmp_cpy._jobs.insert(pos, j)
					all_m.append(tmp_cpy)
					new_xes.append(all_m)
				if k != k_min_c:
					for pos in range(len(k_min_c._jobs)):
						all_m = [machine for machine in machines if machine != k_min_c]
						tmp_cpy = deepcopy(k_min_c)
						if job in tmp_cpy._jobs:
							tmp_cpy._jobs.remove(job)
						tmp_cpy._jobs.insert(pos, job)
						all_m.append(tmp_cpy)
						new_xes.append(all_m)
				return new_xes

	elif cons_type == 3:
		# inserisci il job in tutte le posizioni di tutte le macchine
		for k in machines:
			for pos in range(len(k._jobs)):
				all_m = [machine for machine in machines if machine != k]
				tmp_cpy = deepcopy(k)
				if job in tmp_cpy._jobs:
					tmp_cpy._jobs.remove(job)
				tmp_cpy._jobs.insert(pos, job)
				all_m.append(tmp_cpy)
				new_xes.append(all_m)
			
		return new_xes		

def movement(old_x, new_xes):
	old_tardiness = []
	for k in old_x:
		old_tardiness.append(k.get_total_tardiness())

	best_tard = max(old_tardiness)
	best_sched = old_x
	for new_x in new_xes:
		new_x_tardiness = []
		for k in new_x:
			new_x_tardiness.append(k.get_total_tardiness())
		new_x_tardiness = max(new_x_tardiness)
		if new_x_tardiness < best_tard:
			best_tard = new_x_tardiness
			best_sched = new_x
	
	changed = True if best_tard != max(old_tardiness) else False

	return changed, best_sched
	

from datas import setup_times, specs_list, jobs, machines

which_scheds = 3

if which_scheds in [-1, 0]:
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

if which_scheds in [-1, 1]:
# ------------------------SCHEDULING CON ATCS------------------------------
	# scheduling con ATCS - prendo dati
	jobs_1_5 = deepcopy(jobs)
	machines_1_5 = deepcopy(machines)
	setup_times_1_5 = deepcopy(setup_times)

	print("------ Scheduler 1 - ATCS ----------")
		# step 0 - Assegno i primi m jobs in ordine EDD	
	EDD_m(jobs_1_5, machines_1_5)

		# step 1 - Assegno i job in accordo con ATCS index
	ATCS(jobs_1_5, machines_1_5, setup_times_1_5)

		# risultato
	print("Risultato per scheduling con ATCS")
	print_schedule(machines_1_5)
	tardiness = Machine.get_total_tardiness_per_machine(machines_1_5)
	print("Tardiness totale: ", str(max(tardiness)))
	print_schedule_detailed(machines_1_5)

if which_scheds in [-1, 2]:
# ------------------------SCHEDULING CON APD_ATCS------------------------------
	# scheduling con APD_ATCS - prendo dati
	jobs_1 = deepcopy(jobs)
	machines_1 = deepcopy(machines)
	setup_times_1 = deepcopy(setup_times)

	print("------ Scheduler 2 - APD_ATCS ----------")
		# step 0 - Assegno i primi m jobs in ordine EDD	
	EDD_m(jobs_1, machines_1)

		# step 1 - Assegno i job in accordo con ATCS index
	ATCS_APD(jobs_1, machines_1, setup_times_1)

		# risultato
	print("Risultato per scheduling con ATCS_APD")
	print_schedule(machines_1)
	tardiness = Machine.get_total_tardiness_per_machine(machines_1)
	print("Tardiness totale: ", str(max(tardiness)))

if which_scheds in [-1, 3]:
# ------------------------SCHEDULING CON GREEDY e APD_ATCS------------------------------
	# scheduling con GREEDY e APD_ATCS - prendo dati
	jobs_2 = deepcopy(jobs)
	machines_2 = deepcopy(machines)
	setup_times_2 = deepcopy(setup_times)

	print("------ Scheduler 3 - APD_ATCS + GREEDY ----------")
	# Calcolo le soluzioni con Random Iterated Greedy (RIG)
	sol = RIG(jobs_2, machines_2, setup_times_2, l_max=100)

	print("Risultato per scheduling con ATCS_APD + GREEDY")
	print_schedule(sol[1])
	tardiness = Machine.get_total_tardiness_per_machine(sol[1])
	print("Tardiness totale: ", str(max(tardiness)))
