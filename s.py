import pygame
import sys
from player import player

def checkKeys(p1):

	if p1.dnd:
		return

	keys = pygame.key.get_pressed()

	if keys[pygame.K_RIGHT]:
		p1.is_moving = True
		p1.moving_right = True
		p1.state = 1
		p1.dir = 0
	else:
		p1.moving_right = False

	if keys[pygame.K_LEFT]:
		p1.is_moving = True
		p1.moving_left = True
		p1.state = 1
		p1.dir = 1
	else:
		p1.moving_left = False

	if keys[pygame.K_UP]:
		p1.is_moving = True
		p1.moving_up = True
		p1.state = 1
	else:
		p1.moving_up = False

	if keys[pygame.K_DOWN]:
		p1.is_moving = True
		p1.moving_down = True
		p1.state = 1
	else:
		p1.moving_down = False

	# if no directional keys are pressed then char is not moving
	if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
		p1.is_moving = False
		p1.state = 0
		p1.prevState = 0

	# attack
	if keys[pygame.K_a]:
		p1.is_attacking = True
		p1.prevState = p1.state # save current state to return to after attack
		p1.state = 2
		p1.dnd = True
	else:
		if p1.state == 2:
			p1.is_attacking = False
			p1.revertState()

	# jump
	if keys[pygame.K_s]:
		p1.is_jumping = True
		p1.prevState = p1.state # save current state to return to after attack
		p1.state = 3
		p1.dnd = True
	else:
		if p1.state == 3:
			p1.is_jumping = False
			p1.revertState()

	# hurt
	if keys[pygame.K_h]:
		print("hurt key")
		p1.is_hurt = True
		p1.dnd = True
		p1.prevState = p1.state
		p1.state = 5
	else:
		if p1.state == 5:
			p1.is_hurt = False
			p1.revertState()

	#print("no keys pressed, moving flag to false")

	# elif keys[pygame.K_a]:
	# 	p1.prevState = p1.state
	# 	p1.state = 2
	# 	p1.is_attacking = True
	# 	p1.dnd = True
	# 	p1.stopMovement()

	# elif keys[pygame.K_j]:
	# 	p1.prevState = p1.state
	# 	p1.state = 3
	# 	p1.is_jumping = True
	# 	p1.dnd = True
	# 	p1.stopMovement()

	# elif event.type == pygame.KEYUP:

	# 	if event.key == pygame.K_RIGHT:
	# 		p1.moving_right = False
	# 	elif event.key == pygame.K_LEFT:
	# 		p1.moving_left = False
	# 	elif event.key == pygame.K_UP:
	# 		p1.moving_up = False
	# 	elif event.key == pygame.K_DOWN:
	# 		p1.moving_down = False
	# 	elif event.key == pygame.K_a or event.key == pygame.K_j:
	# 		p1.revertState()

	# 	if not (p1.moving_down or p1.moving_up or p1.moving_left or p1.moving_right):
	# 		p1.is_moving = False
	# 		print("stop walking")
	# 		p1.revertState()
	# 		print("reverted")
	# 		p1.movingDir()


def orderObjectsAndBlit(objList):

	objList.sort(key = lambda x: x.posx)
	objList.sort(key = lambda x: x.posy)
	for x in objList:
		x.blitChar()


def offset(mask1, mask2):
	return int(mask2.posx - mask1.posx), int(mask2.posy - mask1.posy)


def testCollision(p1,p2):

	if(p1.is_attacking and not p2.is_hurt):
		if p1.maskImg.overlap(p2.maskImg, offset(p1, p2)):
			print("collision - setting previous state to: " + str(p2.state))
			p2.prevState = p2.state
			p2.state = 5
			p2.is_hurt = True
			p2.dnd = True
		else:
			print("no collision")

def init_game():

	pygame.init()
	screen = pygame.display.set_mode((1200,720))
	pygame.display.set_caption("LOOOL")
	pygame.display.update()

	bg = pygame.image.load("imgs/bg.png")
	bg = pygame.transform.scale(bg, (1200,720))

	p1hero = "knight"
	p2hero = "mage"

	objList = []
	p1 = player(screen, p1hero)
	objList.append(p1)
	p2 = player(screen, p2hero)
	objList.append(p2)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		checkKeys(p1)

		screen.blit(bg, (0,0))
		p2.updateLoc()
		p1.updateLoc()

		testCollision(p1, p2)

		orderObjectsAndBlit(objList)

		pygame.display.flip()


init_game()