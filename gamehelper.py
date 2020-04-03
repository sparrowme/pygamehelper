import pygame
from pygame.locals import *
import os
import sys
import math
from PIL import Image

pygame.init()

class Player(object):
    
    def __init__(self, helper,x, y, width, height):
        print(x,y)
        self.helper=helper
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False 
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.yy=0
        self.run = [pygame.image.load(os.path.join(self.helper.resource,'images', 'player'+str(x) + '.png')) for x in range(1,5)]
    def draw(self,canvas):
        if self.falling:
            pass
        else:
            if self.runCount > 15:
                self.runCount = 0
            #print(self.runCount//4)
            canvas.blit(self.run[self.runCount//4], (self.x,self.y))
            self.runCount += 1
            #self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13)

class Helper():
    bg=None
    run=False
    bg1left=0
    bg2left=0
    framerate=10
    clock=None
    canvas=None
    showinfo=False
    infobox=None
    player=None
    resource=''
    def __init__(self):
        #start the clock
        self.clock=pygame.time.Clock()
        
    def engine(self):
        return pygame
    def setTitle(self,title):
        pygame.display.set_caption(title)
    def loadBackground(self,path=None):
        #use PIL to get image size
        if path==None:
            bgimg=os.path.join(self.resource,'images','bg.png')
        else:
            bgimg=path
        im = Image.open(bgimg)
        self.canvas=pygame.display.set_mode(im.size)
        #display must be set before image.load will work
        self.bg = pygame.image.load(bgimg).convert()
        self.bg1left=0
        self.bg2left=self.bg.get_width()
        

        
    def redraw(self):
        self.canvas.blit(self.bg, (self.bg1left, 0))  
        self.canvas.blit(self.bg, (self.bg2left, 0))      
        if self.showinfo:
            self.blit_alpha(self.canvas, self.infobox, (10, 10), 128)
        self.player.draw(self.canvas)
        pygame.display.update()
    def movebackground(self):
        bgwidth=self.bg.get_width()
        self.bg1left -= 1.4  # Move background images back
        self.bg2left -= 1.4
        if self.bg1left < bgwidth * -1:  # shift background back to start
            self.bg1left = bgwidth
        if self.bg2left < bgwidth * -1:
            self.bg2left = bgwidth
    def moveplayer(self):
        if self.player==None:
            self.player=Player(self,100,self.bg.get_height()-120,40,60)
            #self.player=Player(100,250,20,30)
        #self.player.draw(self.canvas)
    def nextframe(self):
        self.movebackground()
        self.updateinfo()
        self.moveplayer()
        self.redraw()
    def checkevents(self):
        for event in pygame.event.get():  # Loop through a list of events
            if event.type == pygame.QUIT or not self.run:  # See if the user clicks the red x 
                run = False    # End the loop
                pygame.quit()  # Quit the game
                #quit()
                sys.exit() #force python to end before next screen draw
            if event.type == pygame.KEYUP:
                pygame.key.set_repeat(0)
            if event.type == pygame.KEYDOWN:
                key=event.__dict__
                #print(key)
                char=key['unicode']
                if key['key']==27: #esc
                    self.run=False
                elif key['key']==282 or pygame.key.get_pressed()[pygame.K_F1]: #F1 
                    self.toggleinfo()
                elif char=='[':
                    print(pygame.key.get_repeat())
                    pygame.key.set_repeat(500,100)
                    print(pygame.key.get_repeat())
                    self.framerate-=1
                elif char==']':
                    pygame.key.set_repeat(500,100)
                    self.framerate+=1
                else:
                    print(char,'pressed.\n',key)
        keys = pygame.key.get_pressed()

        #if keys[pygame.K_ESCAPE]:
        #    self.run=False
    def toggleinfo(self):
        self.showinfo= not self.showinfo
    def updateinfo(self):
        infotext="""
F1  Info
F2  Inventory
ESC Quit
[   Decrease FPS
]   Increase FPS

FPS: {0}
        """.format(self.framerate)
        self.infobox=pygame.image.load(os.path.join(self.resource,'images','infobox.png'))
        largeFont = pygame.font.SysFont('comicsans', 20) # creates a font object
        c=0
        for line in infotext.split('\n'):
            info=largeFont.render(line,1,(255,255,255))
            self.infobox.blit(info,(20,c*20))
            c+=1
        #self.canvas.blit(self.infobox
    def play(self):
        self.run=True
        while self.run:
            self.nextframe()
            self.checkevents()
            self.clock.tick(self.framerate)
    def blit_alpha(self,target, source, location, opacity):
        """Thanks to https://nerdparadise.com/programming/pygameblitopacity"""
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)