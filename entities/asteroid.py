"""
Asteroid class
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


def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L
    
# Base class
from entity import Entity

class Asteroid(Entity):

	HEALTH_MAX = ASTEROID_HEALTH_MAX

	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0, radius = 8200):
		super(Asteroid, self).__init__(x, y, r, g, b)
		self.drawn = False

		self.pauseFirst = True
		self.pauseLast = True

		self.theta = 0
		self.thetaRate = 0

		self.radius = radius
		self.collisionRadius = radius

		self.health = Asteroid.HEALTH_MAX

                # Create asteroid geometry
                minRadius = radius * 0.75
                maxRadius = radius
                granularity = 20.0
                minVary = 25
                maxVary = 75
                self.points = []
                
                for ang in frange(0.0, 2.0 * math.pi, 2.0 * math.pi / granularity):
                        angleVaryPc = random.uniform(minVary, maxVary)
                        angleVaryRadians = (2.0 * math.pi / granularity) * angleVaryPc / 100.0
                        angleFinal = ang + angleVaryRadians - (math.pi / granularity)
                        rad = random.uniform(minRadius, maxRadius)
                        px = math.sin(angleFinal) * rad
                        py = -math.cos(angleFinal) * rad
                        #print [px,py]
                        self.points.append([px,py])
                self.points.append(self.points[0])


	def subtract(self, health):
		self.health = max(self.health - health, 0)

	def produce(self):
		"""
		Generate the points of the circle.
		"""
		r, g, b = (0, 0, 0)

		# Generate points
		ed = self.radius

		pts = []
		pts.append({'x': ed, 'y': ed})
		pts.append({'x': -ed, 'y': ed})
		pts.append({'x': -ed, 'y': -ed})
		pts.append({'x': ed, 'y': -ed})

		# Rotate points
		for p in pts:
			x = p['x']
			y = p['y']
			p['x'] = x*math.cos(self.theta) - y*math.sin(self.theta)
			p['y'] = y*math.cos(self.theta) + x*math.sin(self.theta)

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

	def draw(self):
		"""
		Draw the asteroid shape
		"""
		# Generate points
                #print "drawing asteroid"
		ed = self.radius
                #print "asteroid radius = ", ed

                pts = []
		for pt in self.points:
                        pts.append(pt[:])
                #print pts
		#pts.append([ ed, ed])
		#pts.append([-ed, ed])
		#pts.append([-ed, -ed])
		#pts.append([ ed, -ed])
                #pts.append([ ed, ed])

		# Rotate points
		for p in pts:
			x = p[0]
			y = p[1]
			p[0] = x*math.cos(self.theta) - y*math.sin(self.theta)
			p[1] = y*math.cos(self.theta) + x*math.sin(self.theta)

		# Translate points
                #print "asteroid x,y = ", self.x, self.y
		for pt in pts:
                        #print pt
                	pt[0] += self.x
			pt[1] += self.y
                        #print pt

                ol.begin(ol.LINESTRIP)
                for p in pts:
                        ol.vertex(tuple(p), ol.C_WHITE)
                ol.end()

		self.drawn = True


