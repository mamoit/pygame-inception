import pygame, sys
from pygame.locals import *
from math import pi,cos,sin

class Game:
	# Init game
	def __init__(self):
		# Init pygame
		pygame.init()
		
		# Set clock
		self.fpsClock = pygame.time.Clock()
		
		# Set some options
		self.res = (640,480)
		self.maxFPS = 30
		self.title = "Test Game"
		
		# Create the window
		self.windowSurfaceObj = pygame.display.set_mode(self.res, RESIZABLE)
		pygame.display.set_caption(self.title)
		
		# enable key repetition for fast depth change
		pygame.key.set_repeat(100,10)
		
		self.black = (0,0,0)
		self.r = (255, 0, 0)
		self.g = (0, 255, 0)
		self.b = (0, 0, 255)
		self.colors = (self.r,self.g,self.b)
		self.ncolors = len(self.colors)
		
		self.mousex, self.mousey = 0, 0
		
		self.depth = 20
		
		self.ratio = 1.0/2
		
		# square calculation
		self.minSide = min(self.res)
		
		self.vertexes = 4
		self.center = (self.res[0]/2,self.res[1]/2)
		self.radius = min(self.center)
		
		self.squarePoints = []
		
		for v in xrange(self.vertexes):
			self.squarePoints.append((self.center[0]+self.radius*sin(v*2*pi/self.vertexes),self.center[1] + self.radius*cos(v*2*pi/self.vertexes)))
		
		# Start main loop
		self.loop()

	# Main loop
	def loop(self):
		while True:
			self.windowSurfaceObj.fill(self.black)
			lastPoints = self.squarePoints
			pygame.draw.aalines(self.windowSurfaceObj,self.r,True,self.squarePoints)
			for ind in xrange(self.depth):
				points = []
				for i in xrange(self.vertexes):
					j = i+1 if i<self.vertexes-1 else 0
					points.append((lastPoints[i][0]+self.ratio*(lastPoints[j][0] - lastPoints[i][0]), lastPoints[i][1]+self.ratio*(lastPoints[j][1] - lastPoints[i][1])))
				
				pygame.draw.aalines(self.windowSurfaceObj,self.colors[(ind+1)%self.ncolors],True,points)
				lastPoints = points
			
			# Handle events
			self.handleEvents()
			# Refresh Screen and keep FPS in check
			pygame.display.update()
			self.fpsClock.tick(self.maxFPS)

	# Event Handeling
	def handleEvents(self):
		for event in pygame.event.get():
			# Quit event
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == VIDEORESIZE:
				self.res = event.size
				self.windowSurfaceObj = pygame.display.set_mode(self.res, RESIZABLE)
				minSide = min(self.res)
				self.center = (self.res[0]/2,self.res[1]/2)
				self.radius = min(self.center)
				self.squarePoints = []
				for v in xrange(self.vertexes):
					self.squarePoints.append((self.center[0]+self.radius*sin(v*2*pi/self.vertexes),self.center[1] + self.radius*cos(v*2*pi/self.vertexes)))
			# mouse moved
			elif event.type == MOUSEMOTION:
				self.mousex, self.mousey = event.pos
				self.ratio = float(self.mousex)/(self.res[0]-1)
			# scroll handle
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 4: # up
					self.vertexes = self.vertexes + 1
				elif event.button == 5: # down
					self.vertexes = self.vertexes - 1 if self.vertexes - 1 >= 3 else 3
				
				# recalculate outter vertexes
				self.squarePoints = []
				for v in xrange(self.vertexes):
					self.squarePoints.append((self.center[0]+self.radius*sin(v*2*pi/self.vertexes), self.center[1] + self.radius*cos(v*2*pi/self.vertexes)))
			# key pressed
			elif event.type == KEYDOWN:
				# exit
				if event.key == K_ESCAPE or event.key == K_q:
					pygame.event.post(pygame.event.Event(QUIT))
				# increase drawing depth
				elif event.key == K_PLUS:
					self.depth += 1
				# decrease drawing depth
				elif event.key == K_MINUS:
					self.depth = self.depth - 1 if self.depth-1 > 1 else 1
				# Key pressed event
				elif event.type == KEYDOWN:
					# Key pressed with intention to quit
					if (event.key == K_ESCAPE or event.key == K_q):
						pygame.event.post(pygame.event.Event(QUIT))

