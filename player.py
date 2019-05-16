import math
from pygame import Rect

# Player Class. Keeps track of position and velocity and other variables
class Player:
    def __init__(self, px = 100, py = 250, width = 56, height = 40, maxy = 800, gravity = 0, upVel = -7, maxVel = 20):
        self.px = px
        self.py = py
        self.gravity = gravity
        self.xvel = 0
        self.yvel = 0
        self.width = width
        self.height = height
        self.upVel = upVel
        self.maxVel = maxVel
        self.score = 0
        self.xVelMax = 5
        self.maxy = maxy
        self.xMove = False
        self.xdel = width/5
        self.rect = Rect(0,0,0,0)
        self.updateRect()

    #Updates the rect to its current position
    def updateRect(self):
        self.rect.x, self.rect.y = self.getDrawBoxTopLeft()
        self.rect.w, self.rect.h = self.getDim()

    def getRect(self):
        return self.rect

    def getSprite(self):
        return r"assets\Player.png"
    
    def getDrawBoxTopLeft(self):
        return self.px - self.width/2, self.py - self.height/2

    def getCenter(self):
        return self.px, self.py

    def getDim(self):
        return self.width, self.height

    #Move in x direction by a small amount dx. Check for collisions
    def incX(self,dx,bl):
        self.px += dx
        self.updateRect()
        #Check all the blocks for collisions
        for i in bl:
            if self.getRect().colliderect(i.getRect()):     #If there is a collision, set x to box boundary
                if dx >= 0:
                    self.px = i.getRect().x
                    self.vx = 0
                else:
                    self.px = i.getRect().x + i.getRect().w
                break
        self.updateRect()

    #Move in y direction by amount dy. Same as above
    def incY(self,dy,bl):
        self.py += dy
        self.updateRect()
        for i in bl:
            if self.getRect().colliderect(i.getRect()):
                if dy >= 0:
                    self.px = i.getRect().y
                else:
                    self.px = i.getRect().y + i.getRect().h
                self.xvel = 0
                break
        self.updateRect()

    #Updates the block to move left, right, up or down based on velocity
    def update(self, blockList):
        self.incX(self.xvel,blockList)
        self.incY(self.yvel,blockList)
        self.py = min(self.py,self.maxy)
        self.yvel = min(self.yvel+self.gravity, self.maxVel)
        if not self.xMove:
            self.xvel = 0
        self.xMove = False
        self.updateRect()

    def moveX(self,direction):
        self.xvel = self.xVelMax*direction
        self.xMove = True

    def jump(self):
        self.yvel = self.upVel

    def setDim(self,dim):
        self.width, self.height = dim

