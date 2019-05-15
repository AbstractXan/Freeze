import pygame
from random import randint
from player import Player

# Class for stationary platforms
class Platform:
    # px, py are the top left corner coordinates
    # height and width are the dimensions of the block
    # rect is the pygame Rect representation of the block
    def __init__(self, px, py, width, height):
        self.px = px
        self.py = py
        self.width = width
        self.height = height
        self.rect = pygame.Rect(px,py,width,height)
    
    # Get the top left corner of the box
    def getDrawBoxTopLeft(self):
        return self.px, self.py

    #Get the center of the box
    def getCenter(self):
        return self.px + self.width/2, self.py + self.height/2

    def getDim(self):
        return self.width, self.height

    def setDim(self,dim):
        self.width, self.height = dim

    def getRect(self):
        return self.rect

# Global Game Parameters
FPS = 60
PLAYER_WIDTH = 56
PLAYER_HEIGHT = 40
PLAYER_JUMP = -8.2
GRAVITY = 1*30.0/FPS
PLAYER_STARTX = 220
PLAYER_STARTY = 320
PLAYER_MAX_Y = 630

# Class that holds the game state and information
class Game:

    def __init__(self):
        pygame.init()
        self.gameStart = False
        self.screen = pygame.display.set_mode((480,640))
        self.clock = pygame.time.Clock()
        self.spriteSheet = {}

    @staticmethod
    def isVisible(coord,dim):
        if 0 <= coord[0] - dim[0]/2 <= 480:
            return True
        if 0 <= coord[0] + dim[0]/2 <= 480:
            return True
        return False

    def loadSprite(self, t):
        if t not in self.spriteSheet:
            temp = pygame.image.load(t).convert_alpha()
            mask = pygame.mask.from_surface(temp)
            self.spriteSheet[t] = temp, mask

    def start(self):
        self.inGame = True
        self.player = Player(gravity=GRAVITY, upVel = PLAYER_JUMP,
                                         px = PLAYER_STARTX, py = PLAYER_STARTY,
                                         maxy = PLAYER_MAX_Y)
        self.boxList = []
        self.stageElementList = []
        self.stageElementList.append(Platform(60,490,100,30,))

    def drawPlatform(self,platform):
        pygame.draw.rect(self.screen,(0,0,0), platform.getRect())

    def drawPlayer(self):
        t = self.player.getSprite()
        self.loadSprite(t)
        cord = list(self.player.getCenter())
        temp = self.spriteSheet[t][0]
        box = temp.get_rect().width, temp.get_rect().height
        cord[0] = cord[0] - box[0]/2
        cord[1] = cord[1] - box[1]/2
        self.screen.blit(temp,cord)

    def draw(self):
        self.screen.fill((255,255,255))
        for i in self.stageElementList:
            self.drawPlatform(i)
        self.drawPlayer()
        pygame.display.flip()

    def wait(self,fps):
        self.clock.tick(fps)

    def destroy(self):
        pygame.quit()

    def isRunning(self):
        return self.inGame

    def update(self):
        if self.gameStart:
            self.player.update(self.stageElementList)

    def startGame(self):
        self.gameStart = True

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGame = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.player.jump()
            if not self.gameStart:
                self.startGame()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.moveX(-1)
        if keys[pygame.K_RIGHT]:
            self.player.moveX(1)

    def checkSingleCollision(self, player, platform):
        return player.getRect().colliderect(platform.getRect())

    def checkCollision(self):
        self.playerStageColl = []
        for i in self.stageElementList:
            if self.checkSingleCollision(self.player,i):
                self.playerStageColl.append(i)

    def dead(self):
        self.gameStart = False
        self.start()

game = Game()
game.start()
#game.startGame()
while game.isRunning():
    game.getInput()
    game.update()
    
    game.draw()
    game.wait(FPS)

game.destroy()
