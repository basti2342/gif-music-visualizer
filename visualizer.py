#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, numpy, time
from recorder import *
import pygame, pygame.mouse, logging, os, subprocess, sys
from pygame.locals import *

class Visualization:
	def __init__(self, filename, minNum, maxNum):
		"Ininitializes a new pygame screen using the framebuffer"

		self.w = 800
		self.h = 600
		self.filename = filename
		self.minNum = minNum
		self.maxNum = maxNum

		self.initPygame()
		self.initRecorder()

	def initPygame(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.w, self.h))
		pygame.mouse.set_visible(False)
		self.clock = pygame.time.Clock()

	def initRecorder(self):
		self.SR = SwhRecorder()
		self.SR.setup()
		self.SR.continuousStart()

	def translate(self, value, leftMin, leftMax, rightMin, rightMax):
		# Figure out how 'wide' each range is
		leftSpan = leftMax - leftMin
		rightSpan = rightMax - rightMin

		# Convert the left range into a 0-1 range (float)
		valueScaled = float(value - leftMin) / float(leftSpan)

		# Convert the 0-1 range into a value in the right range.
		return rightMin + (valueScaled * rightSpan)

	def scalePercentage(self, surface, perc):
		screenRect = self.screen.get_rect()
		surface = pygame.transform.scale(surface, (int(perc*screenRect.width),
		int(perc*screenRect.height)))
		return surface

	def show(self):
		run = True
		maxAvg = 1
		lastMapped = 0
		tendency = 0
		mapped = 0
		while run:
			try:
				#self.clock.tick(20)
				# quit on "window close" and Escape
				for evt in pygame.event.get():
					if evt.type == KEYDOWN:
						if evt.key == K_ESCAPE:
							run = False
						elif evt.key == K_F11:
							pygame.display.toggle_fullscreen()
					elif evt.type == QUIT:
						run = False

				if self.SR.newAudio:
					# fourier transformation
					fft = self.SR.fft()[1]
					self.SR.newAudio = False

					avg = reduce(lambda x, y: x + y, fft) / len(fft)

					# dynamic maximum
					if avg > maxAvg:
						maxAvg = avg

					# translate range into number of frames
					mapped = self.translate(avg, 0, maxAvg, self.minNum, self.maxNum)

					# do not update if image does not change
					if mapped == lastMapped:
						continue
					elif mapped > lastMapped:
						tendency = 1
					elif mapped < lastMapped:
						tendency = -1

					# smooth transition
					if lastMapped - mapped > 2:
						mapped = lastMapped - ((lastMapped - mapped)/2)

					# save last image
					lastMapped = mapped
					#print "calcd"
				else:
					mapped = lastMapped + tendency
					if not self.minNum <= mapped <= self.maxNum:
						continue
					#print "tendency"

				# display image
				#print self.filename % mapped
				img = pygame.image.load(self.filename % mapped).convert()

				# use whole screen
				img = self.scalePercentage(img, 1)
				self.screen.blit(img, (0, 0))
				pygame.display.update()

				# give it a second until the audio buffer is filled up
				time.sleep(0.01)
			except:
				break
		self.SR.close()

if __name__ == "__main__":
	#v = Visualization("frames/dough/teig-%d.jpg", 0, 66)
	v = Visualization("frames/melon/melon-%d.jpg", 9, 108)
	v.show()
	pygame.quit()


