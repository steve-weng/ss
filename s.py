import pygame
import sys
from player import *
from pygame import gfxdraw

def checkKeys(p1, screen):

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
		#p1.fireBlast()
		return fireBlastObj(screen, "fireBlastObj", p1);
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
		p1.is_hurt = True
		p1.dnd = True
		p1.prevState = p1.state
		p1.state = 5
	else:
		if p1.state == 5:
			p1.is_hurt = False
			p1.revertState()

	return None


def orderObjectsAndBlit(objList):

	objList.sort(key = lambda x: x.posx)
	objList.sort(key = lambda x: x.posy)
	for x in objList:
		x.blitChar()


def offset(mask1, mask2):
	return int(mask2.posx - mask1.posx), int(mask2.posy - mask1.posy)

def checkObjHealth(objList):
	for i, obj in enumerate(objList):
		if (obj.hp <= 0):
			print("deleting")
			del objList[i]

def testCollision(p1,p2):

	if(p1.is_attacking and not p2.is_hurt):
		if p1.maskImg.overlap(p2.maskImg, offset(p1, p2)) and p1.owner != p2:
			p2.prevState = p2.state
			p2.state = 5
			p2.is_hurt = True
			p2.dnd = True
			print (p1)
			print (p2)
			print(str(p1.owner) + (' owner'))
			p2.processDamage(50)
			if (p1.owner != None):
				p1.hp = 0

def init_game():

	pygame.init()
	screen = pygame.display.set_mode((1200,720))
	pygame.display.set_caption("LOOOL")
	pygame.display.update()

	bg = pygame.image.load("imgs/bg.png")
	bg = pygame.transform.scale(bg, (1200,720))

	p1Hero = "dragon"
	#p2Hero = "mage"
	enemyHero = "dragon"

	# initialize original objects
	objList = []
	p1 = player(screen, p1Hero)
	objList.append(p1)
	#p2 = player(screen, p2Hero)
	#objList.append(p2)
	d1 = dragon(screen, enemyHero)
	objList.append(d1)

	# game loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		newObj = checkKeys(p1, screen)
		if (newObj!= None): # if we need to add a new attack obj (e.g., fire blast)
			objList.append(newObj)
			newObj = None

		screen.blit(bg, (0,0))
		#p2.updateLoc()
		p1.updateLoc()
		if (p1.hp > 0):
			pInfo = (p1.posx, p1.posy, p1.hp)

		#d1.AIMove(pInfo)
		d1.updateLoc()

		if (len(objList) >= 3):
			for a in objList:
				if (a.hero == "fireBlastObj"):
					a.move()

		#testCollision(p1, d1)
		for i in objList:
			for j in objList:
				if (i != j): # we dont want to test collision between same obj/player
					testCollision(i, j)

		#testCollision(d1, p1)
		checkObjHealth(objList)
		orderObjectsAndBlit(objList)
		pygame.display.flip()


init_game()