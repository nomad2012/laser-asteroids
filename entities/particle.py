"""
Particle Entity
	TODO: DOC
"""

# STDLIB
import math
import random
import itertools
import sys
import thread
import time
import pygame
import pylase as ol

# GLOBALS 
from globalvals import *

# Base class
from entity import Entity

class Particle(Entity):
	def __init__(self, x=0, y=0, r=0, g=0, b=0):
		super(Particle, self).__init__(x, y, r, g, b)
		self.radius = 1
		self.drawn = False
		self.pauseFirst = True
		self.pauseLast = True

		# Particle Duration
		self.life = random.randint(PARTICLE_LIFE_MIN, PARTICLE_LIFE_MAX)
		self.xVel = 0
		self.yVel = 0

	def produce(self):
		for i in range(20):
			yield (self.x, self.y, self.r, self.g, self.b)

	def draw(self):
                #print ("drawing particle")
		ol.dot((self.x, self.y), 20, ol.C_WHITE)

