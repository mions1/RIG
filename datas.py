from machine import Machine
from job import Job
from spec import Spec

machines = [
	Machine(1),
	Machine(2)
]

# setup times dalla tabella 2 dell'articolo
setup_times = {
	"length":	60,
	"width":	15,
	"thickness":10,
	"hardness": 20,
	"colour": 	15,
}

# creazione delle specs per ogni job, dalla tabelle 2 dell'articolo
specs_list = {
	1: [
		Spec("length", 240, setup_times["length"]),
		Spec("width", 12, setup_times["width"]),
		Spec("thickness", 1.5, setup_times["thickness"]),
		Spec("hardness", 7, setup_times["hardness"]),
		Spec("colour", 1, setup_times["colour"])
	],
	2: [
		Spec("length", 96, setup_times["length"]),
		Spec("width", 36, setup_times["width"]),
		Spec("thickness", 5.0, setup_times["thickness"]),
		Spec("hardness", 8, setup_times["hardness"]),
		Spec("colour", 1, setup_times["colour"])
	],
	3: [
		Spec("length", 96, setup_times["length"]),
		Spec("width", 24, setup_times["width"]),
		Spec("thickness", 3.0, setup_times["thickness"]),
		Spec("hardness", 9, setup_times["hardness"]),
		Spec("colour", 2, setup_times["colour"])
	],
	4: [
		Spec("length", 240, setup_times["length"]),
		Spec("width", 36, setup_times["width"]),
		Spec("thickness", 8.0, setup_times["thickness"]),
		Spec("hardness", 8, setup_times["hardness"]),
		Spec("colour", 2, setup_times["colour"])
	],
	5: [
		Spec("length", 240, setup_times["length"]),
		Spec("width", 36, setup_times["width"]),
		Spec("thickness", 1.5, setup_times["thickness"]),
		Spec("hardness", 7, setup_times["hardness"]),
		Spec("colour", 2, setup_times["colour"])
	],
	6: [
		Spec("length", 240, setup_times["length"]),
		Spec("width", 12, setup_times["width"]),
		Spec("thickness", 3.0, setup_times["thickness"]),
		Spec("hardness", 9, setup_times["hardness"]),
		Spec("colour", 1, setup_times["colour"])
	],
	7: [
		Spec("length", 96, setup_times["length"]),
		Spec("width", 36, setup_times["width"]),
		Spec("thickness", 1.5, setup_times["thickness"]),
		Spec("hardness", 7, setup_times["hardness"]),
		Spec("colour", 9, setup_times["colour"])
	],
	8: [
		Spec("length", 96, setup_times["length"]),
		Spec("width", 48, setup_times["width"]),
		Spec("thickness", 3.0, setup_times["thickness"]),
		Spec("hardness", 9, setup_times["hardness"]),
		Spec("colour", 1, setup_times["colour"])
	],
	9: [
		Spec("length", 144, setup_times["length"]),
		Spec("width", 36, setup_times["width"]),
		Spec("thickness", 3.0, setup_times["thickness"]),
		Spec("hardness", 9, setup_times["hardness"]),
		Spec("colour", 1, setup_times["colour"])
	],
	10: [
		Spec("length", 96, setup_times["length"]),
		Spec("width", 24, setup_times["width"]),
		Spec("thickness", 5.0, setup_times["thickness"]),
		Spec("hardness", 7, setup_times["hardness"]),
		Spec("colour", 2, setup_times["colour"])
	]
}

# creazione dei jobs in riferimento alla tabella 2 dell'articolo

jobs = [
	Job(1, specs_list[1], 444, 2315),
	Job(2, specs_list[2], 189, 2087),
	Job(3, specs_list[3], 474, 1614),
	Job(4, specs_list[4], 313, 2463),
	Job(5, specs_list[5], 644, 2037),
	Job(6, specs_list[6], 253, 2275),
	Job(7, specs_list[7], 578, 2142),
	Job(8, specs_list[8], 645, 1693),
	Job(9, specs_list[9], 459, 1754),
	Job(10, specs_list[10], 361, 1596)
]