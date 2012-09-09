#!/usr/bin/env python

# STDLIB
import math
import random
import itertools
import sys
import thread
import time
from datetime import datetime, timedelta

# PYGAME
import pygame

# MY CODES
from daclib import dac
from daclib.common import *
from globalvals import *
from colors import *
from entities.ship import *
from entities.healthbar import *
from entities.asteroid import *
from entities.asteroidExplode import *
from entities.bullet import *
from pointstream import PointStream

"""
Main Program
"""

DRAW = None # Will be the global PointStream
bulletSpawnOk = True

class GameState(object):
	"""
	A simple structure to keep track of 'global' game state.
	"""
	def __init__(self):
		# Objects
		self.ship = None
		self.healthbar = None
		self.bullets = []
		self.asteroids = []

STATE = GameState()

class Player(object):
	"""
	Player (conflated)
		- Contain joystick ref
		- Contain visual object
	"""
	def __init__(self, joystick, radius=BALL_RADIUS, rgb=(CMAX, CMAX, CMAX)):
		self.js = joystick
		self.score = 0
		self.pid = 0

		# Joystick
		joystick.init()

		# debug
		numButtons = joystick.get_numbuttons()
		print joystick.get_name()
		print numButtons

		# Player Object
		self.obj = Ship(0, 0, r=rgb[0], g=rgb[1], b=rgb[2], radius=radius/2)
		self.healthbar = HealthBar(0, 0, r=0, g=CMAX, b=0, radius=radius/2)

		DRAW.objects.append(self.obj)
		DRAW.objects.append(self.healthbar)

		STATE.ship = self.obj
		STATE.healthbar = self.healthbar

	def __str__(self):
		return self.js.get_name()

"""
THREADS
"""

def dac_thread():
	global PLAYERS, DRAW

	while True:
		try:
			ps = PointStream()
			DRAW = ps

			d = dac.DAC(dac.find_first_dac())
			d.play_stream(ps)

		except Exception as e:

			import sys, traceback
			print '\n---------------------'
			print 'Exception: %s' % e
			print '- - - - - - - - - - -'
			traceback.print_tb(sys.exc_info()[2])
			print "\n"
			pass

			# In case we went off edge, recenter. 
			# XXX: This is just laziness
			for p in PLAYERS:
				p.obj.x = 0
				p.obj.y = 0

def joystick_thread():
	"""Manage the joysticks with PyGame"""
	global PLAYERS
	global bulletSpawnOk

	pygame.joystick.init()
	pygame.display.init()

	if not pygame.joystick.get_count():
		print "No Joystick detected!"
		sys.exit()

	p1 = Player(pygame.joystick.Joystick(0),
			rgb = COLOR_PINK)


	PLAYERS.append(p1)

	numButtons = p1.js.get_numbuttons() # XXX NO!
	bulletLastFired = datetime.now()

	while True:
		e = pygame.event.get()

		for p in PLAYERS:

			# Joysticks 
			lVert = p.js.get_axis(1)
			lHori= p.js.get_axis(0)
			rVert = p.js.get_axis(4)
			rHori= p.js.get_axis(3)

			if abs(rVert) > 0.2:
				y = p.obj.y
				y += -1 * int(rVert * SIMPLE_TRANSLATION_SPD)
				if MIN_Y < y < MAX_Y:
					p.obj.y = y

			if abs(rHori) > 0.2:
				x = p.obj.x
				x += -1 * int(rHori * SIMPLE_TRANSLATION_SPD)
				if MIN_X < x < MAX_X:
					p.obj.x = x

			# Player rotation
			t = math.atan2(lVert, lHori)
			p.obj.theta = t

			# Health Bar Location
			STATE.healthbar.x = p.obj.x
			STATE.healthbar.y = p.obj.y - 2500

			# Firing the weapon (Left Trigger)
			trigger = False if p.js.get_axis(2) in [0.0, -1.0] else True

			if bulletSpawnOk and trigger:
				td = timedelta(milliseconds=150) # TODO: Cache this.
				if datetime.now() > bulletLastFired + td:
					ang = p.obj.theta + math.pi
					b = Bullet(p.obj.x, p.obj.y, rgb=COLOR_BLUE, shotAngle=ang)
					DRAW.objects.append(b)
					STATE.bullets.append(b)
					bulletLastFired = datetime.now()

		time.sleep(0.02) # Keep this thread from hogging CPU


numEnemies = 0 # XXX: MOve to game state object... 
numBullets = 0 # XXX: MOve to game state object... 

def game_thread():
	global DRAW
	global STATE
	global numEnemies
	global numBullets
	global bulletSpawnOk

	def spawn_enemy():
		x = random.randint(ENEMY_SPAWN_MIN_X, ENEMY_SPAWN_MAX_X)
		y = random.randint(ENEMY_SPAWN_MIN_Y, ENEMY_SPAWN_MAX_Y)
		xVel = random.randint(ENEMY_SPAWN_MIN_X_VEL, ENEMY_SPAWN_MAX_X_VEL)
		yVel = random.randint(ENEMY_SPAWN_MIN_X_VEL, ENEMY_SPAWN_MAX_X_VEL)
		radius = random.randint(ENEMY_MIN_RADIUS, ENEMY_MAX_RADIUS)

		e = Enemy(x, y, r=CMAX, g=CMAX, b=0, radius=radius)
		e.velX = xVel
		e.velY = yVel
		e.thetaRate = random.uniform(-math.pi/100, math.pi/100)

		DRAW.objects.append(e)
		STATE.asteroids.append(e)

	def spawn_particles(x, y):
		np = random.randint(PARTICLE_SPAWN_MIN,
							PARTICLE_SPAWN_MAX)
		for i in range(np):
			p = Particle(x, y, CMAX, CMAX, CMAX)
			p.xVel = random.randint(PARTICLE_MIN_X_VEL,
									PARTICLE_MAX_X_VEL)
			p.yVel = random.randint(PARTICLE_MIN_Y_VEL,
									PARTICLE_MAX_Y_VEL)
			particles.append(p)
			DRAW.objects.append(p)


	while True:
		#print "GameThread objects: %d" % len(DRAW.objects)
		try:

			"""
			Game Events
			"""
			if numEnemies < MAX_NUM_ENEMIES: # and random.randint(0, 5) == 0:
				spawn_enemy()

			if numBullets < MAX_NUM_BULLETS:
				bulletSpawnOk = True
			else:
				bulletSpawnOk = False


			"""
			Collision Detection
			"""
			# Populate lists
			# TODO: Let's not have to continually rebuild these
			ship = None
			bullets = []
			enemies = []
			particles = []

			for obj in DRAW.objects:
				if type(obj) == Enemy:
					enemies.append(obj)
				elif type(obj) == Particle:
					particles.append(obj)
				elif type(obj) == Bullet:
					bullets.append(obj)
				elif type(obj) == Ship:
					ship = obj

			# Bullet-enemy collisions
			for b in bullets:
				for e in enemies:
					if e.checkCollide(b):
						e.destroy = True
						b.destroy = True
						spawn_particles(e.x, e.y)

			"""
			checkCollision = DRAW.objects[:]
			while len(checkCollision) > 1:
				a = checkCollision.pop(0)
				for b in checkCollision:
					if a.collides(b):
						print "COLLIDES"
			"""

			numEnemies = 0
			numBullets = 0

			"""
			Handle Onscreen Objects
			"""
			for i in range(len(DRAW.objects)):
				obj = DRAW.objects[i]

				# PLAYER
				if type(obj) == Ship:
					continue

				# BULLETS
				elif type(obj) == Bullet:
					# XXX Recounted each iter due to terrible design 
					numBullets += 1
					x = obj.x
					y = obj.y
					x += BULLET_SPEED * math.cos(obj.theta)
					y += BULLET_SPEED * math.sin(obj.theta)
					if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y :
						obj.destroy = True
						continue
					obj.x = x
					obj.y = y

				elif type(obj) == Enemy:
					# XXX Recounted each iter due to terrible design 
					numEnemies += 1
					x = obj.x
					y = obj.y
					x += obj.velX
					y += obj.velY
					if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y :
						obj.destroy = True
						continue
					obj.x = x
					obj.y = y
					obj.theta += obj.thetaRate

				elif type(obj) == Particle:
					x = obj.x
					y = obj.y
					x += obj.xVel
					y += obj.yVel

					if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y :
						obj.destroy = True
						continue
					obj.x = x
					obj.y = y

					obj.life -= 1
					if obj.life <= 0:
						obj.destroy = True
						continue

			time.sleep(0.02)

		except Exception as e:
			import sys, traceback
			print '\n---------------------'
			print 'GAME Exception: %s' % e
			traceback.print_tb(sys.exc_info()[2])
			print "---------------------\n"
			time.sleep(0.02)

thread.start_new_thread(dac_thread, ())
thread.start_new_thread(game_thread, ())
thread.start_new_thread(joystick_thread, ())

"""
UNUSED STUFF
"""

while True:
	time.sleep(200)


