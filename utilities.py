from job import Job

debug = 100

def print_d(text, lvl=0):
	if lvl >= debug or debug==-1:
		print(text)

def print_schedule(machines):
	for i,k in enumerate(machines):
		print("Machine #"+str(i+1)+": ",end="")
		print("(", end="")
		for job in k._jobs:
			print(job._id_number,end=", ")
		print(")")

def print_schedule_d(machines, lvl):
	if lvl >= debug or debug == -1:
			print("")
			for k in machines:
				print("Machine #"+str(k))
				for j in k._jobs:
					print(j)
				print("")

def print_schedule_detailed(machines):
	print("--------------- Dettaglio -----------------")
	for k in machines:
		prev_job = None
		c_t = 0
		print("Machine #"+str(k))
		print("Job #\tSetup time\tInizio a\tFine a\tTardiness")
		for j in k._jobs:
			c_t += Job.get_setup_time(prev_job, j)
			print(j._id_number, end="\t\t")
			print(Job.get_setup_time(prev_job, j), end="\t")
			print(c_t, end="\t\t")
			c_t += j._processing_time
			print(c_t, end="\t")
			print(max(c_t-j._due_date, 0), end="\n")
			prev_job = j
		
		print("Total tardiness: ", k.get_total_tardiness())
	print("-------------------------------------------")