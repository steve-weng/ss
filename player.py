import pygame
from settings import settings

class player():
	
	def __init__(self, screen, hero):

		self.hero = hero
		self.settings = settings()

		self.atkRange = None
		self.owner = None # atk objects have owner to not dmg them
		# screen rectangle size setup
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# used to keep track of which frame the current animation is on for each state
		self.frameCount = [0, 0, 0, 0, 0, 0, 0]
		self.atkFrameSpeed = float(0.1)
		self.jumpFrameSpeed = float(0.1)
		self.hurtFrameSpeed = float(0.1)

		self.walkImg = []
		self.atkImg = []
		self.jumpImg = []
		self.hurtImg = []

		# num of frames for each animation for each hero
		self.numFrames = self.settings.frames(self.hero)
		self.loadImgs()

		# holds current image, default is the idle
		self.img = self.idleImg
		self.maskImg = pygame.mask.from_surface(self.img)

 		# default sprite rectangular size
		self.rect = self.img.get_rect()

		# where to place initial default sprite on the screen
		self.rect.centerx = self.screen_rect.centerx - 500
		self.rect.bottom = self.screen_rect.bottom - 200

		# holds current position, the 0.1 is a temp solution for flickering animations
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

		# holds current state
		# 0 = idle, 1 = walk, 2 = attack, 3 = jump, 4 = jump attack, 5 = hurt, 6 = dead
		self.state = 0

		# previous state to revert to when needed
		self.prevState = 0
		self.dir = 0 # direction facing, 0 for right, 1 for left, 2 up, 3 down


	def loadImgs(self):

		self.idleImg = pygame.image.load('imgs/' + self.hero + '/' + self.hero + '.png')

		# loading in walking animation
		for i in range(1, self.numFrames[0] + 1):
			self.loadImg = pygame.image.load('imgs/' + self.hero + '/walk/walk' + str(i) + '.png')
			self.walkImg.append(self.loadImg)

		# attack
		for i in range(1, self.numFrames[1] + 1):
			self.loadImg = pygame.image.load('imgs/' + self.hero + '/attack/attack' + str(i) + '.png')
			self.atkImg.append(self.loadImg)

		if self.hero != "dragon":
			# jump
			for i in range(1, self.numFrames[2] + 1):
				self.loadImg = pygame.image.load('imgs/' + self.hero + '/jump/jump' + str(i) + '.png')
				self.jumpImg.append(self.loadImg)		

		# empty jump attack

		# hurt
		for i in range(1, self.numFrames[4] + 1):
			self.loadImg = pygame.image.load('imgs/' + self.hero + '/hurt/hurt' + str(i) + '.png')
			self.hurtImg.append(self.loadImg)

		# empty dead


	# after jump, attack, hurt, determine if char should be idle or walking
	def revertState(self):

		self.state = self.prevState
		if self.state == 1:
			self.is_moving = True
			self.prevState = 0 # set previous state to default idle
		else:
			self.is_moving = False

	
	def processDamage(self, dmg):
		self.hp = self.hp - dmg
		print("took " + str(dmg) +" dmg, " + str(self.hp) + "hp left")
		if (self.hp <= 0):
			self.is_dead = True


	def updateAnimationInt(self):

		# idle animation

		if self.state == 0: # idle animations
			if self.dir == 0: # idle image direction
				self.img = self.idleImg
			elif self.dir == 1:
				self.img = pygame.transform.flip(self.idleImg, True, False)


		elif self.state == 1: # walking animations

			if self.frameCount[self.state] >= self.numFrames[0]: # when it reaches last animation
				self.frameCount[self.state] = 0

			# only update to the next animation every 10th/integer moves
			if self.posx % 10 == 0 or self.posy % 10 == 0:
				if self.dir == 0:
					self.img = self.walkImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.walkImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1


		elif self.state == 2: # attack animation

			if self.frameCount[self.state] >= self.numFrames[1]:
				self.frameCount[self.state] = 0
				self.is_attacking = False
				self.dnd = False

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

			# reset frames to 0 if we're at the last animation
			if self.frameCount[self.state] >= self.numFrames[2]:
				self.frameCount[self.state] = 0
				self.is_jumping = False
				self.dnd = False	

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

			if self.frameCount[self.state] >= self.numFrames[4]: # hardcoded, hurt has 4 images
				self.frameCount[self.state] = 0
				self.is_hurt = False
				self.dnd = False
				self.revertState()

			# only update to the next animation every 10th/integer moves
			if self.hurtFrameSpeed % 10 == 0:
				if self.dir == 0:
					self.img = self.hurtImg[self.frameCount[self.state]]
				elif self.dir == 1:
					self.img = pygame.transform.flip(self.hurtImg[self.frameCount[self.state]], True, False)
				self.frameCount[self.state]+=1
				self.hurtFrameSpeed += 0.1
			else:
				self.hurtFrameSpeed += 0.1
				self.hurtFrameSpeed = round(self.hurtFrameSpeed, 1)

		# set the new mask image for collision detection
		self.maskImg = pygame.mask.from_surface(self.img)


	def blitChar(self):

		if (self.owner == None):
			self.updateAnimationInt() # we dont update animations for atk objs

		# sets current sprite location to where its position is updated to
		self.rect.centerx = self.posx
		self.rect.bottom = self.posy
		self.screen.blit(self.img, self.rect)


	# updates character location, only applicable for walking, jumping
	def updateLoc(self):

		if self.is_moving == False:
			return

		# up down left right movement
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.posx += 0.1 
			self.posx = round(self.posx, 1)
		if self.moving_left and self.rect.left > 0:
			self.posx -= 0.1
			self.posx = round(self.posx, 1)
		if self.moving_up and self.rect.top > 215: # foreground upper bounds
			self.posy -= 0.1
			self.posy = round(self.posy, 1)
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom - 115: # lower bounds
			self.posy += 0.1 
			self.posy = round(self.posy, 1)


#class knight(player):

#	def __init__(self, screen):

# fire blast object
class fireBlastObj(player):

	def __init__(self, screen, hero, p1):
		super().__init__(screen, hero)

		self.hero = hero
		self.owner = p1

		self.rect.centerx = p1.rect.centerx
		self.rect.bottom = p1.rect.bottom

		# holds current position
		self.posx = self.rect.centerx + 0.1
		self.posy = self.rect.bottom + 0.1
		self.hp = 100000 # fireball "dies" upon collision
		self.dir = p1.dir
		self.is_attacking = True #att objs are always dmg on
		self.dnd = True
		#self.state = 2 #att state
		

	def move(self):
		if (self.dir == 0):
			self.posx = self.posx + 0.5
		else:
			self.posx = self.posx - 0.5

		# change hp to 0 to del if outside of screen
		if (self.posx > pygame.display.get_window_size()[0]
	  		or self.posx < 0):
			self.hp = 0


class dragon(player):

	def __init__(self, screen, hero):
		super().__init__(screen, hero)
		self.atkRange = 50
		# where to place initial default sprite on the screen
		self.rect.centerx = self.screen_rect.centerx - 300
		self.rect.bottom = self.screen_rect.bottom - 300

		# holds current position
		self.posx = self.rect.centerx + 0.1
		self.posy = self.rect.bottom + 0.1
		

	# trying to create dragon blast attack, has to be another obj
	#def fireBlast(self):
		# later add in checks for range (when blast/when melee)
		# attack animation already loaded, but this adds the
		# fire blast obj img, and obj returned


	# move ai until in attack range of player position
	# each turn, check if in range, if so, attack
	def move(self, p1):

		# move closer to player
		if (self.posx + 10 < p1[0]):
			self.posx += 0.1
			self.is_moving = True
			self.moving_right = True
			self.state = 1
			self.dir = 0
			#self.moving_left = False
		elif (self.posx - 10 > p1[0]):
			self.posx -= 0.1
			self.is_moving = True
			self.moving_left = True
			self.state = 1
			self.dir = 1
			#self.moving_right = False
		
		if (self.posy + 10 < p1[1]):
			self.posy += 0.1
			self.is_moving = True
			self.moving_down = True
			self.state = 1
			#self.moving_up = False
		elif (self.posy - 10 > p1[1]):
			self.posy -= 0.1
			self.is_moving = True
			self.moving_up = True
			self.state = 1
			#self.moving_down = False

		# if ai is within its attack range of player, attack
		if (self.posy < p1[1] < self.posy + 50):
			if (self.dir == 0): # facing right	
				if (self.posx < p1[0] < self.posx + self.atkRange):
					self.is_attacking = True
			elif (self.dir == 1):
				if (self.posx > p1[0] > self.posx - self.atkRange):
					self.is_attacking = True
