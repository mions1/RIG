class Spec():
	""" La classe Spec descrive la specifica del job.
		Nel caso del lavoro di riferimento, essa descriverà:
			- Length
			- Width
			- Thickness
			- Hardness
			- Colour
		
		Il valore dipende dal job, mentre il setup time dipende dalla caratteristica.
		I setup time (in minuti), per questo lavoro, sono:
			- 	length:		60
			-	width:		15
			-	thickness:	10
			-	hardness: 	20
			-	colour: 	15

		Il setup time è il tempo che serve per riprogrammare la macchina se due lavori
		successivi hanno, per la stessa caratteristica, due valori diversi.
		I setup time vanno sommani tra loro per avere il setup time totale per la riprogrammazione.
	"""

	def __init__(self, name: str, value: float, setup_time: int):
		""" 

		Args:
			name (str): nome della spec
			value (float): valore per la spec del job
			setup_time (int): valore del setuptime
		"""

		self._name = name
		self._value = value
		self._setup_time = setup_time