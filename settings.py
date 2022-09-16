class settings():
	
	def __init__(self):
		pass
		

	def frames(self, hero):

		# number of images/frames for each hero
		# listed same as state minus idle so by indices:
		# walk, attack, jump, jump attack, hurt, dead

		if hero == "knight":
			return [6, 5, 7, 0, 4, 10]

		elif hero == "mage":
			return [6, 7, 7, 0, 4, 10]