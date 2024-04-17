class settings():
	
	def __init__(self):
		pass
		

	def frames(self, character):

		# number of images/frames for each character...not to be confused with char type
		# listed same as state minus idle so by indices:
		# walk, attack, jump, jump attack, hurt, dead

		if character == "knight":
			return [6, 5, 7, 0, 4, 10]

		elif character == "mage":
			return [6, 7, 7, 0, 4, 10]

		elif character == "dragon":
			return [5, 4, 0, 0, 2, 5] # dragon doesn't have jump
		
		elif character == "fireBlastObj":
			return [0, 0, 0, 0, 0, 0]