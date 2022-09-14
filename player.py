import pygame

class player():
	
	def __init__(self, screen):

		# screen rectangle size setup
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# used to keep track of which count the current animation is on
		self.animationInt = 0

		self.idleImg = pygame.image.load('imgs/w/knight.png')
		# holds current image, default is the idle
		self.img = self.idleImg



		# holds current state
		# 0 = idle, 1 = walk, 2 = attack, 3 = jump, 4 = hurt
		self.state = 0
		self.dir = 0 # direction facing, 0 for right, 1 for left, 2 up, 3 down

		# loading in walking animation
		self.walkImg = []
		for i in range(1, 7):
			self.loadImg = pygame.image.load('imgs/w/Walk/walk' + str(i) + '.png')
			self.walkImg.append(self.loadImg)

		# default sprite rectangular size
		self.rect = self.img.get_rect()

		# where to place initial default sprite on the screen
		self.rect.centerx = self.screen_rect.centerx - 500
		self.rect.bottom = self.screen_rect.bottom - 30

		# holds current position
		self.posx = self.rect.centerx + 0.1
		self.posy = self.rect.bottom + 0.1

		# holds movement direction
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False


	def updateAnimationInt(self):

		# set up which animation
		if self.state == 0: # idle animations
			if self.dir == 0: # idle image direction
				self.img = self.idleImg
			elif self.dir == 1:
				self.img = pygame.transform.flip(self.idleImg, True, False)

		elif self.state == 1: # walking animations

			print("state is 1")
			print(self.moving_left)
			print(self.moving_right)
			print(self.moving_up)
			print(self.moving_down)
			print(self.posx)
			print(self.posy)

			# only update to the next animation every 10th/integer moves
			if self.posx % 10 == 0 or self.posy % 10 == 0:
				print("conditions met")
				if self.animationInt >= 6: # hardcoded, walk has 6 images
					self.animationInt = 0
				if self.dir == 0:
					self.img = self.walkImg[self.animationInt]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.walkImg[self.animationInt], True, False)
				self.animationInt+=1


	def blitChar(self):

		self.updateAnimationInt()

		# sets current sprite location to where its position is updated to
		self.rect.centerx = self.posx
		self.rect.bottom = self.posy
		self.screen.blit(self.img, self.rect)


	def updateLoc(self):

		
		# halve the speed if the character is moving diagonally
		#if self.moving_right and self.moving_up or self.moving_right and self.moving_down or \
		#	self.moving_left and self.moving_up or self.moving_left and self.moving_down:
		#	speedFactor = 0.5

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