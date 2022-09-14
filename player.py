import pygame

class player():
	
	def __init__(self, screen):

		# screen rectangle size setup
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# used to keep track of which frame the current animation is on for each state
		self.frameCount = [0, 0, 0, 0, 0]
		self.atkFrameSpeed = float(0.1)
		self.jumpFrameSpeed = float(0.1)

		self.idleImg = pygame.image.load('imgs/knight.png')
		# holds current image, default is the idle
		self.img = self.idleImg

		self.midair = False # for jumping that gets interrupted

		# holds current state
		# 0 = idle, 1 = walk, 2 = attack, 3 = jump, 4 = hurt, 5 = dead
		self.state = 0
		self.dir = 0 # direction facing, 0 for right, 1 for left, 2 up, 3 down
 
		# loading in walking animation
		self.walkImg = []
		for i in range(1, 7): # 6 frames
			self.loadImg = pygame.image.load('imgs/walk/walk' + str(i) + '.png')
			self.walkImg.append(self.loadImg)

		self.atkImg = []
		for i in range(1, 7):
			self.loadImg = pygame.image.load('imgs/attk/walk_attack' + str(i) + '.png')
			self.atkImg.append(self.loadImg)

		self.jumpImg = []
		for i in range(1, 8):
			self.loadImg = pygame.image.load('imgs/jump/jump' + str(i) + '.png')
			self.jumpImg.append(self.loadImg)		

		# default sprite rectangular size
		self.rect = self.img.get_rect()

		# where to place initial default sprite on the screen
		self.rect.centerx = self.screen_rect.centerx - 500
		self.rect.bottom = self.screen_rect.bottom - 30

		# holds current position
		self.posx = self.rect.centerx + 0.1
		self.posy = self.rect.bottom + 0.1


		# priority.  hurt > attack > jump > movement > idle
		self.is_hurt = False
		self.is_attacking = False
		self.is_jumping = False
		self.is_idle = True
		self.is_dead = False

		# holds movement direction
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False


	def updateAnimationInt(self):

		if self.state == 3: # jump animation

			# reset frames to 0 if we're at the last animation
			if self.frameCount[self.state] >= 6: # hardcoded, jump has 7 images
				self.frameCount[self.state] = 0

			print("current frame is " + str(self.frameCount[self.state]))

			# slows down animation
			if self.jumpFrameSpeed % 10 == 0:
			
					#print("reset at 0")
				if self.dir == 0:
					self.img = self.jumpImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.jumpImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1
				self.jumpFrameSpeed += 0.1
			else:
				self.jumpFrameSpeed += 0.1
				self.jumpFrameSpeed = round(self.jumpFrameSpeed, 1)
			#print(self.frameCount[self.state])

			# first 3 frames for jumping is up, latter 3 is down (middle stays in the air)
			if self.frameCount[self.state] == 1 or self.frameCount[self.state] == 2:
				self.posy -= 0.2
				print("up " + str(self.frameCount[self.state]))
			elif self.frameCount[self.state] == 4 or self.frameCount[self.state] == 5:
				self.posy += 0.2
				print("down " + str(self.frameCount[self.state]))


		# idle animation
		if self.state == 0: # idle animations
			if self.dir == 0: # idle image direction
				self.img = self.idleImg
			elif self.dir == 1:
				self.img = pygame.transform.flip(self.idleImg, True, False)


		elif self.state == 1: # walking animations

			if self.frameCount[self.state] >= 5: # hardcoded, walk has 6 images
				self.frameCount[self.state] = 0

			# only update to the next animation every 10th/integer moves
			if self.posx % 10 == 0 or self.posy % 10 == 0:

				if self.dir == 0:
					self.img = self.walkImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.walkImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1

		elif self.state == 2: # attack animation

			if self.frameCount[self.state] >= 5: # hardcoded, attack has 6 images
				self.frameCount[self.state] = 0

			# slows down animation for attack
			if self.atkFrameSpeed % 10 == 0:
				# if finish attacking, reset to 0, end attack

					#self.is_attacking = False
					#self.state = 1
				if self.dir == 0:
					self.img = self.atkImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.atkImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1
				self.atkFrameSpeed += 0.1
			else:
				self.atkFrameSpeed += 0.1
				self.atkFrameSpeed = round(self.atkFrameSpeed, 1)




	def blitChar(self):

		self.updateAnimationInt()

		# sets current sprite location to where its position is updated to
		self.rect.centerx = self.posx
		self.rect.bottom = self.posy
		self.screen.blit(self.img, self.rect)


	# hurt > attack >= jump > move > idle (prototype). returns the state
	def checkMovementPriorty(self):

		if self.is_attacking:
			return 2
		elif self.is_jumping:
			return 3
		elif self.moving_right or self.moving_down or self.moving_up or self.moving_left:
			return 1
		else:
			return 0



	# updates character location, only applicable for walking, jumping
	def updateLoc(self):

	#	self.checkMovementPriorty()

		# halve the speed if the character is moving diagonally
		#if self.moving_right and self.moving_up or self.moving_right and self.moving_down or \
		#	self.moving_left and self.moving_up or self.moving_left and self.moving_down:
		#	speedFactor = 0.5

		# up down left right movement
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.posx += 0.1 
			self.posx = round(self.posx, 1)
		if self.moving_left and self.rect.left > 0:
			self.posx -= 0.1
			self.posx = round(self.posx, 1)
		if self.moving_up and self.rect.top > 0:
			self.posy -= 0.1
			self.posy = round(self.posy, 1)
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.posy += 0.1 
			self.posy = round(self.posy, 1)