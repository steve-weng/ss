import pygame
import sys
from player import player

def checkKeys(p1):

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
	else:
		if p1.state == 2:
			p1.is_attacking = False
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


def init_game():

	pygame.init()
	screen = pygame.display.set_mode((1200,800))
	pygame.display.set_caption("LOOOL")
	red = [255, 0, 0]
	screen.fill(red)
	pygame.display.update()

	p1 = player(screen)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		checkKeys(p1)

		screen.fill(red)
		p1.updateLoc()
		p1.blitChar()
		pygame.display.flip()


init_game()