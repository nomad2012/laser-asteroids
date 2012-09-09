"""
Exploded Asteroid Entity
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

class AsteroidExplode(Entity):
	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0, radius = 1200):
		super(AsteroidExplode, self).__init__(x, y, r, g, b)
		self.radius = radius
		self.drawn = False

		self.pauseFirst = True
		self.pauseLast = True

		self.theta = 0

	def produce(self):
		"""
		Generate the points of the circle.
		"""
		r, g, b = (0, 0, 0)

		# Generate points
		ed = self.radius/2

		# Translate points
		for pt in pts:
			pt['x'] += self.x
			pt['y'] += self.y

		r = 0 if not self.r else int(self.r / LASER_POWER_DENOM)
		g = 0 if not self.g or LASER_POWER_DENOM > 4 else self.g
		b = 0 if not self.b else int(self.b / LASER_POWER_DENOM)

		def make_line(pt1, pt2, steps=200):
			xdiff = pt1['x'] - pt2['x']
			ydiff = pt1['y'] - pt2['y']
			line = []
			for i in xrange(0, steps, 1):
				j = float(i)/steps
				x = pt1['x'] - (xdiff * j)
				y = pt1['y'] - (ydiff * j)
				line.append((x, y, r, g, b)) # XXX FIX COLORS
			return line

		# DRAW THE SHAPE

		p = None # Save in scope

		for p in make_line(pts[0], pts[1], SQUARE_EDGE_SAMPLE_PTS):
			break
		for i in range(int(round(SQUARE_VERTEX_SAMPLE_PTS/2.0))):
			yield p
		for p in make_line(pts[0], pts[1], SQUARE_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SQUARE_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[1], pts[2], SQUARE_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SQUARE_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[2], pts[3], SQUARE_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SQUARE_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[3], pts[0], SQUARE_EDGE_SAMPLE_PTS):
			self.lastPt = p # KEEP BOTH
			yield p
		for i in range(int(round(SQUARE_VERTEX_SAMPLE_PTS/2.0))):
			self.lastPt = p # KEEP BOTH
			yield p

		self.drawn = True


