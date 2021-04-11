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