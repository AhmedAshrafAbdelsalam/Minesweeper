#
#	A module to handle the internals of tiles 
#


from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QLabel
import random
import sys

class TileLabel(QPushButton):
	lost = pyqtSignal()
	random = pyqtSignal(int,int)
	voidFound = pyqtSignal(int,int)
	isFirstTile = True
	isNotFlagged = True
	isMine = False
	num = 0
	xpos = 0
	ypos = 0

	def __init__(self,window,i,j):
		super(TileLabel,self).__init__(window)
		self.xpos = i
		self.ypos = j
		self.setStyleSheet("border-image : url(Minesweeper/Minesweeper_0.svg)")
		self.setEnabled(False)
		self.clicked.connect(self.click)

	def click(self):
		if TileLabel.isFirstTile == True:
			self.random.emit(self.xpos,self.ypos)
			TileLabel.isFirstTile == False
		if self.num == 0:
			self.voidFound.emit(self.xpos,self.ypos)
		if self.isMine == True and self.isNotFlagged:
			self.setStyleSheet("border-image : url(Minesweeper/Minesweeper_RedMine.png)")
			self.lost.emit()
	
	def toggleClickablility(self,state):
		self.isNotFlagged = state

class TileButton(QPushButton):
	won = pyqtSignal()
	flag = pyqtSignal(bool)
	flagState = True
	minesLeft = 0
	boxesLeft = 0

	def __init__(self,window):
		super(TileButton,self).__init__(window)
		self.setStyleSheet("border-image : url(Minesweeper/Minesweeper_unopened_square.svg)")
		self.clicked.connect(self.click)
		self.flag.connect(self.flagged)

	def mousePressEvent(self, e):
		if e.button() == Qt.RightButton:
			self.flag.emit(not (self.flagState))
		elif e.button() == Qt.LeftButton:
			self.clicked.emit()

	def click(self):
		if(self.flagState == True):
			self.hide()
			TileButton.boxesLeft -=1

			if TileButton.boxesLeft == 0:
				self.won.emit()
	
	def flagged(self):
		self.flagState = not (self.flagState)
		if self.flagState == False:
			self.setStyleSheet("border-image : url(Minesweeper/Minesweeper_flag.svg)")
			TileButton.minesLeft -= 1
		elif self.flagState == True:
			self.setStyleSheet("border-image : url(Minesweeper/Minesweeper_unopened_square.svg)")
			TileButton.minesLeft += 1