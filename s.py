import pygame
import sys
from player import player

def checkEvents(event, p1):

	if event.type == pygame.QUIT:
		sys.exit()


	elif event.type == pygame.KEYDOWN:

		if event.key == pygame.K_RIGHT:
			p1.moving_right = True
			p1.moving_left = False
			p1.state = 1
			p1.dir = 0
		elif event.key == pygame.K_LEFT:
			p1.moving_left = True
			p1.moving_right = False
			p1.state = 1
			p1.dir = 1
		elif event.key == pygame.K_UP:
			p1.moving_up = True
			p1.moving_down = False
			p1.state = 1
		elif event.key == pygame.K_DOWN:
			p1.moving_down = True
			p1.moving_up = False
			p1.state = 1


	elif event.type == pygame.KEYUP:

		#p1.animationInt = 0
		if event.key == pygame.K_RIGHT:
			p1.moving_right = False
			p1.state = 0
		elif event.key == pygame.K_LEFT:
			p1.moving_left = False
			p1.state = 0
		elif event.key == pygame.K_UP:
			p1.moving_up = False
			p1.state = 0
		elif event.key == pygame.K_DOWN:
			p1.moving_down = False
			p1.state = 0


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
			checkEvents(event, p1)

		screen.fill(red)
		p1.updateLoc()
		p1.blitChar()
		pygame.display.flip()


init_game()