#python3
'''
project idea
bullet hell shooter

player can go left, right, up, and down across the screen
shoots enemies and bosses
if it gets hit by an enemies bullet player takes damage
enemies swarm and shoot

main function will be game
can input a number to select a level

'''
import pygame
import math
from pygame.locals import *
import time
import random

pygame.init()
clock = pygame.time.Clock()
class bullet():
	x=0
	y=0
	d=0
	speed =0

	hit = False
	owner = False
	xSpeed=0
	ySpeed=0
	
	def move(self):
		self.xSpeed = (math.sin(self.d))*self.speed
		self.ySpeed = (math.cos(self.d))*self.speed

		self.x += self.xSpeed
		self.y += self.ySpeed



class player():
		'''
		player class, 
		has health, location, upgrades
		holds movement functions for player
		'''
		hp=50

		invincibility = False
		invincTime = True

		#starting positions
		x=50
		y=50


		def moveLeft(self):
			player.x -=5
		def moveRight(self):
			player.x+=5
		def moveDown(self):
			player.y+=5
		def moveUp(self):
			player.y-=5  
class enemy():
		hp=1



		#starting positions
		x=50
		y=50
		speed = 1
		direction = 0
		frequency = 1
		def move(self):
			self.xSpeed = (math.sin(self.direction))*self.speed
			self.ySpeed = (math.cos(self.direction))*self.speed


			self.x += self.xSpeed
			self.y += self.ySpeed
		def shoot(self):
			createBullet(random.randrange(-math.pi/2, -3*math.pi/2), random.randint(1,3), self.x, self.y, True)

def spriteMovement():
	for i in bulletList:
		i.move()
	for j in enemyList:
		j.move()
def createBullet(direction, speed, startx, starty, owner):
	tempB = bullet()
	tempB.d = direction
	tempB.x = startx
	tempB.y = starty
	tempB.speed = speed
	tempB.owner=owner
	bulletList.append(tempB)



def printScreen(img , imgbul, imgEn,lg):
	color = (0, 128, 255)
	screen.blit(lg,(0,0))

	screen.blit(img,(player.x, player.y))
	if len(bulletList) >0:
		for i in bulletList:
			screen.blit(imgbul,(i.x, i.y))
	if len(enemyList) >0:
		for j in enemyList:
			screen.blit(imgEn,(j.x, j.y))
	health = "Hp:" +str(player.hp)
	
	label = myfont.render(health, 10, (255,255,0))
	screen.blit(label, (100, 100))

	pygame.display.flip()

def check_keys(screenx, screeny):
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]: #making sure the player does not go past the screen
		if not player.y < 0:
			player.moveUp()
	if pressed[pygame.K_DOWN]: 
		if not player.y+60 > screeny:
			player.moveDown()
	if pressed[pygame.K_LEFT]: 
		if not player.x < 0:
			player.moveLeft()
	if pressed[pygame.K_RIGHT]: 
		if not player.x+60 > screenx:
			player.moveRight()
	if pressed[pygame.K_SPACE] and (int(round(time.time()*100)) % 5 ==0): 
		createBullet(math.pi, 3, player.x+30, player.y, False)


def spriteCollision(screenx, screeny):
	#checking bullet collision with edge of screen
	if len(bulletList) >0:
		for i in bulletList:
			if i.x<0 or i.x>1080 or i.y<0 or i.y > 720:
				bulletList.remove(i)
		for i in bulletList:#checking with player
			if (i.x >= player.x and i.x<=player.x+60 and i.y >= player.y and i.x<=player.x+60 and i.owner)  and not player.invincibility:
				bulletList.remove(i)
				player.invincTime = int(round(time.time()))
				player.invincibility = True
				print("bullet hit player")
				player.hp-=1

	if len(enemyList)>0:
		for i in enemyList:
			if ((i.x >= player.x and i.x<=player.x+60) and (i.y >= player.y and i.x<=player.x+60)) or ((i.x+20 >= player.x and i.x+20<=player.x+60) and (i.y+20 >= player.y and i.x+20<=player.x+60)) and not player.invincibility:
				enemyList.remove(i)# if the enemy and the player touch, the enemy is destroyed and the player takes damage
				player.hp-=1
				player.invincibility = True
				player.invincTime = int(round(time.time()))

		for i in enemyList:#checking screen
			if i.x<0 or i.x>1080 or i.y > 720:
				enemyList.remove(i)
		for i in enemyList:
			if len(bulletList) >0:
				for j in bulletList:
					if ((j.x >= i.x and j.x<=i.x+20) and (j.y >= i.y and j.y<=i.y+20) and not j.owner):
					#if the bullet is inside the enemy and not an enemy's bullet
						enemyList.remove(i)
						bulletList.remove(j)



def creatEnemy(ti, created):
	if ti %10==0 and not ti == created:
		created = ti
		i=0
		t = int(round(time.time()))
		while i< 10:#creating enemy   
			tempE = enemy()
			tempE.x = 100*random.randrange(1,8)
			tempE.y=0
			tempE.speed = 1
			tempE.direction = 0
			tempE.frequency = random.randint(1,2)
			enemyList.append(tempE)
			i+=1
def enemyShoot():
	if (len(enemyList)>0):
		for i in enemyList:
			if (int(round(time.time()*100)) % 100 ==0):
				createBullet(random.uniform(-1,1), i.frequency*1.5, i.x+10, i.y, True)

def check_invincibility():
	if player.invincibility:
		if int(round(time.time())) - player.invincTime > 3:
			player.invincibility = False 







myfont = pygame.font.SysFont("monospace", 15)
screenx=1080
screeny=720
screen = pygame.display.set_mode((screenx, screeny))
done = False
player = player()
bulletList = []#creating null bullet
enemyList = []#creating a null list of enemies
t1 = int(round(time.time()*100))
created =0
bulletTime = 0
img=pygame.image.load('ssprit.png')
img = pygame.transform.scale(img,(60,60))
imgbul = pygame.image.load('bci.png')
imgbul = pygame.transform.scale(imgbul,(5,5))
imgEn=  pygame.image.load('enS.png')
imgEn = pygame.transform.scale(imgEn,(20,20))
lg=  pygame.image.load('lg.jpg')
lg = pygame.transform.scale(lg,(screenx,screeny))
pygame.display.set_caption("The Last Judgment")

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        check_keys(screenx, screeny)
        spriteMovement()    
        check_invincibility()
        

        dt = (int(round(time.time()*100))-t1)
        creatEnemy(float (dt/100), created)
        enemyShoot()
        spriteCollision(screenx, screeny)
        printScreen(img, imgbul, imgEn, lg)
        #print(dt)
        if player.hp <= 0:
        	print ("you died")
        	done = True

        






