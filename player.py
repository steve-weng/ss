import pygame

class player():
	
	def __init__(self, screen):

		# screen rectangle size setup
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# used to keep track of which frame the current animation is on for each state
		self.frameCount = [0, 0, 0, 0, 0, 0, 0]
		self.atkFrameSpeed = float(0.1)
		self.jumpFrameSpeed = float(0.1)
		self.hurtFrameSpeed = float(0.1)

		self.idleImg = pygame.image.load('imgs/knight.png')
		# holds current image, default is the idle
		self.img = self.idleImg
		self.maskImg = pygame.mask.from_surface(self.img)

		self.midair = False # for jumping that gets interrupted

		# holds current state
		# 0 = idle, 1 = walk, 2 = attack, 3 = jump, 4 = jump attack, 5 = hurt, 6 = dead
		self.state = 0
		self.dir = 0 # direction facing, 0 for right, 1 for left, 2 up, 3 down
 
		# loading in walking animation
		self.walkImg = []
		for i in range(1, 7): # 6 frames
			self.loadImg = pygame.image.load('imgs/walk2/walk' + str(i) + '.png')
			self.walkImg.append(self.loadImg)

		self.atkImg = []
		for i in range(1, 6):
			self.loadImg = pygame.image.load('imgs/attack/attack' + str(i) + '.png')
			self.atkImg.append(self.loadImg)

		self.jumpImg = []
		for i in range(1, 8):
			self.loadImg = pygame.image.load('imgs/jump/jump' + str(i) + '.png')
			self.jumpImg.append(self.loadImg)		

		self.hurtImg = []
		for i in range(1, 5):
			self.loadImg = pygame.image.load('imgs/hurt/hurt' + str(i) + '.png')
			self.hurtImg.append(self.loadImg)		

		# default sprite rectangular size
		self.rect = self.img.get_rect()

		# where to place initial default sprite on the screen
		self.rect.centerx = self.screen_rect.centerx - 500
		self.rect.bottom = self.screen_rect.bottom - 200

		# holds current position
		self.posx = self.rect.centerx + 0.1
		self.posy = self.rect.bottom + 0.1

		self.hp = 100
		self.mp = 100

		# do not disturb flag - do not disturb if char is in certain animations
		self.dnd = False 

		# priority.  hurt > attack > jump > movement > idle
		self.is_hurt = False
		self.is_attacking = False
		self.is_jumping = False
		self.is_idle = True
		self.is_dead = False
		self.is_moving = False

		# holds movement direction
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

		# previous state to revert to when needed
		self.prevState = 0


	# after jump, attack, hurt, determine if char should be idle or walking
	def revertState(self):

		print("previous state was: " + str(self.prevState))
		self.state = self.prevState
		if self.state == 1:
			#print("previous state is walking tho")
			self.is_moving = True
			self.prevState = 0 # set previous state to default idle
		else:
			self.is_moving = False
		#self.prevState = 0


	# stop walking if character is attacking, or jumping, or hurt
	def stopMovement(self):

		self.is_moving = False
		# self.moving_up = False
		# self.moving_down = False
		# self.moving_left = False
		# self.moving_right = False

	def movingDir(self):

		print("moving up is " + str(self.moving_up))
		print("moving down is " + str(self.moving_down))
		print("moving left is " + str(self.moving_left))
		print("moving right is " + str(self.moving_right))
		print("movement flag is: " + str(self.is_moving))
		print("state is: " + str(self.state))

	def updateAnimationInt(self):

		#print("calling animation function with state: " + str(self.state))
		# idle animation

		if self.state == 0: # idle animations
			#print("state is 0 for some reason")
			if self.dir == 0: # idle image direction
				self.img = self.idleImg
			elif self.dir == 1:
				self.img = pygame.transform.flip(self.idleImg, True, False)


		elif self.state == 1: # walking animations
			#print("we're walking frame: " + str(self.frameCount[self.state]))
			if self.frameCount[self.state] >= 6: # hardcoded, walk has 6 images
				self.frameCount[self.state] = 0

			# only update to the next animation every 10th/integer moves
			if self.posx % 10 == 0 or self.posy % 10 == 0:
				if self.dir == 0:
					self.img = self.walkImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.walkImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1


		elif self.state == 2: # attack animation

			if self.frameCount[self.state] >= 5: # hardcoded, attack has 5 images
				self.frameCount[self.state] = 0
				self.is_attacking = False
				self.dnd = False
				#self.revertState()

			# slows down animation for attack
			if self.atkFrameSpeed % 10 == 0:

				# if finish attacking, reset to 0, end attack
				if self.dir == 0:
					self.img = self.atkImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.atkImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1
				self.atkFrameSpeed += 0.1
			else:
				self.atkFrameSpeed += 0.1
				self.atkFrameSpeed = round(self.atkFrameSpeed, 1)


		elif self.state == 3: # jump animation

			#print("we're jumping")
			# reset frames to 0 if we're at the last animation
			if self.frameCount[self.state] >= 7: # hardcoded, jump has 7 images

				#print("we're on the final jump frame")
				self.frameCount[self.state] = 0
				self.is_jumping = False
				self.dnd = False	
				#self.revertState()

			# slows down animation
			if self.jumpFrameSpeed % 10 == 0:
			
				if self.dir == 0:
					self.img = self.jumpImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.jumpImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1
				self.jumpFrameSpeed += 0.1
			else:
				self.jumpFrameSpeed += 0.1
				self.jumpFrameSpeed = round(self.jumpFrameSpeed, 1)

			# first 3 frames for jumping is up, latter 3 is down (middle stays in the air)
			if self.frameCount[self.state] == 1 or self.frameCount[self.state] == 2:
				self.posy -= 0.2
			elif self.frameCount[self.state] == 4 or self.frameCount[self.state] == 5:
				self.posy += 0.2

		elif self.state == 5: # hurt animations

			print("state is 5 is hurt frame: " + str(self.frameCount[self.state]))
			if self.frameCount[self.state] >= 4: # hardcoded, hurt has 4 images
				print("done hurt")
				self.frameCount[self.state] = 0
				self.is_hurt = False
				self.dnd = False
				self.revertState()
				print("state should be 0 but is: " + str(self.state))

			# only update to the next animation every 10th/integer moves
			if self.hurtFrameSpeed % 90 == 0:
				print("in the middle of hurt")
				if self.dir == 0:
					self.img = self.hurtImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.hurtImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1
				print("frame is now " + str(self.frameCount[self.state]))
				self.hurtFrameSpeed += 0.1
			else:
				self.hurtFrameSpeed += 0.1
				self.hurtFrameSpeed = round(self.hurtFrameSpeed, 1)

		# set the new mask image for collision detection
		self.maskImg = pygame.mask.from_surface(self.img)


	def blitChar(self):

		self.updateAnimationInt()

		# sets current sprite location to where its position is updated to
		self.rect.centerx = self.posx
		self.rect.bottom = self.posy
		self.screen.blit(self.img, self.rect)


	# updates character location, only applicable for walking, jumping
	def updateLoc(self):

	#	self.checkMovementPriorty()

		# halve the speed if the character is moving diagonally
		#if self.moving_right and self.moving_up or self.moving_right and self.moving_down or \
		#	self.moving_left and self.moving_up or self.moving_left and self.moving_down:
		#	speedFactor = 0.5

		if self.is_moving == False:
			#print("moving flag is false, not moving character")
			return

		# up down left right movement
		if self.moving_right and self.rect.right < self.screen_rect.right:
			#print("moving right")
			self.posx += 0.1 
			self.posx = round(self.posx, 1)
		if self.moving_left and self.rect.left > 0:
			#print("moving left")
			self.posx -= 0.1
			self.posx = round(self.posx, 1)
		if self.moving_up and self.rect.top > 215: # foreground upper bounds
			#print("moving up")
			self.posy -= 0.1
			self.posy = round(self.posy, 1)
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom - 115: # lower bounds
			#print("moving down")
			self.posy += 0.1 
			self.posy = round(self.posy, 1)