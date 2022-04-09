import sys
import time

import math
import pygame
import random

FPS = 30
EPSILON = 0.0001
FONT_SIZE = 20
font = None
sizeX = 26
sizeY = 16


def draw_string(dst, msg, p, color):
    text = font.render(msg, True, color)
    dst.blit(text, p)

def hue_to_rgb(hue, val):
    c = (hue // 60) % 6
    f = hue / 60.0 - int(hue / 60.0)
    
    r = 0
    g = 0
    b = 0
    
    if c == 0:
        r = 1
        g = f
        b = 0
    if c == 1:
        r = 1 - f
        g = 1
        b = 0
    if c == 2:
        r = 0
        g = 1
        b = f
    if c == 3:
        r = 0
        g = 1 - f
        b = 1
    if c == 4:
        r = f
        g = 0
        b = 1
    if c == 5:
        r = 1
        g = 0
        b = 1 - f
    
    return (int(r * val * 255), int(g * val * 255), int(b * val * 255))

class vec2f(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, rhs):
        return vec2f(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return vec2f(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, rhs):
        return vec2f(rhs * self.x, rhs * self.y)

    def __rmul__(self, lhs):
        return vec2f(lhs * self.x, lhs * self.y)

    def __truediv__(self, rhs):
        return vec2f(self.x / rhs, self.y / rhs)

    def dot(self, rhs):
        return self.x * rhs.x + self.y * rhs.y

    def cross(self, rhs):
        return self.x * rhs.y - self.y * rhs.x

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def unit(self):
        if self.mag() > EPSILON:
            return self / self.mag()
        else:
            return vec2f(0, 0)

    def rotate(self, theta):
        ret = vec2f(0, 0)
        ret.x = self.x * math.cos(theta) - self.y * math.sin(theta)
        ret.y = self.x * math.sin(theta) + self.y * math.cos(theta)
        return ret

    def __str__(self):
        return str((self.x, self.y))

def dist(a, b):
    return (a - b).mag()

class Grid(object):
    def __init__ (self,w,h):
        self.w,self.h=w,h
        self.data = []
        for _ in range(w):
            row = []
            for _ in range(h):
                row += [None]
            self.data += [row]

    def InsertIt (self,Entity,location):
        x,y=location
        self.data[x][y]=Entity
        Entity.location=location

    def MoveIt (self,Entity,location):
        x,y=Entity.location
        self.data[x][y]=None
        x,y=location
        self.data[x][y]=Entity
        Entity.location=location

    def KillIt (self,entity):
        self.data[entity.location[0]][entity.location[1]]=None
    
        

    def Draw (self,screen):
        for x in range (self.w):
            for y in range (self.h):
                if self.data[x][y] is not None:
                    self.data[x][y].Draw(screen,(FONT_SIZE*x,FONT_SIZE*y))
            

class Entity(object):
    def __init__ (self,symbol,grid):
        self.symbol=symbol
        self.location=(-1,-1)
        self.grid =grid
        self.alive=True

    def Draw(self,screen,location):
        draw_string(screen,self.symbol,location,(255,255,255))

    def update(self):
        return
        

class Player(Entity):
    def __init__ (self,grid):
         Entity.__init__(self,"@",grid)
        
    def key_pressed(self,key):
        pressed=True
        if key == pygame.K_LEFT:
            if self.location[0]>0:
                if self.grid.data[self.location[0]-1][self.location[1]] == None: 
                    self.grid.MoveIt(self,(self.location[0]-1,self.location[1]))
                    
                elif self.location[0]>1 and self.grid.data[self.location[0]-1][self.location[1]].__class__.__name__ == "Cheese":
                    if self.grid.data[self.location[0]-2][self.location[1]] == None:
                        cheese=self.grid.data[self.location[0]-1][self.location[1]]
                        self.grid.MoveIt(cheese,(cheese.location[0]-1,cheese.location[1]))
                        self.grid.MoveIt(self,(self.location[0]-1,self.location[1]))
                    
        elif key == pygame.K_UP:
            if self.location[1]>0:
                if self.grid.data[self.location[0]][self.location[1]-1] == None:
                    self.grid.MoveIt(self,(self.location[0],self.location[1]-1))

                elif self.location[1]>1 and self.grid.data[self.location[0]][self.location[1]-1].__class__.__name__ == "Cheese":
                        if self.grid.data[self.location[0]][self.location[1]-2] == None:
                            cheese=self.grid.data[self.location[0]][self.location[1]-1]
                            self.grid.MoveIt(cheese,(cheese.location[0],cheese.location[1]-1))
                            self.grid.MoveIt(self,(self.location[0],self.location[1]-1))


        elif key == pygame.K_DOWN:
            if self.location[1]<sizeY-1:
                if self.grid.data[self.location[0]][self.location[1]+1] == None:
                    self.grid.MoveIt(self,(self.location[0],self.location[1]+1))

                elif self.location[1]+2<sizeY and self.grid.data[self.location[0]][self.location[1]+1].__class__.__name__ == "Cheese":
                    if self.grid.data[self.location[0]][self.location[1]+2] == None:
                        cheese=self.grid.data[self.location[0]][self.location[1]+1]
                        self.grid.MoveIt(cheese,(cheese.location[0],cheese.location[1]+1))
                        self.grid.MoveIt(self,(self.location[0],self.location[1]+1))


        elif key == pygame.K_RIGHT:
            if self.location[0]<sizeX-1:
                if self.grid.data[self.location[0]+1][self.location[1]] == None:
                    self.grid.MoveIt(self,(self.location[0]+1,self.location[1]))
            
                elif self.location[0]+2<sizeX and self.grid.data[self.location[0]+1][self.location[1]].__class__.__name__ == "Cheese":
                    if self.grid.data[self.location[0]+2][self.location[1]] == None:
                        cheese=self.grid.data[self.location[0]+1][self.location[1]]
                        self.grid.MoveIt(cheese,(cheese.location[0]+1,cheese.location[1]))
                        self.grid.MoveIt(self,(self.location[0]+1,self.location[1]))

        return pressed


 
class Mouse(Entity):
    def __init__ (self,grid):
        Entity.__init__(self,"a",grid)
        self.stomachMax=4
        self.stomach=self.stomachMax

    def update(self,entities):
        if self.stomach>0:
            FW=random.randint(1,4)
            if FW==1:
               if self.location[0]-1 > 0 and self.grid.data[self.location[0]-1][self.location[1]] == None:
                    self.grid.MoveIt(self,(self.location[0]-1,self.location[1]))
            elif FW==2:
                if self.location[1]+1 < sizeY and self.grid.data[self.location[0]][self.location[1]+1] == None:
                    self.grid.MoveIt(self,(self.location[0],self.location[1]+1))
            elif FW==3:
                if self.location[0]+1 < sizeX and self.grid.data[self.location[0]+1][self.location[1]] == None:
                    self.grid.MoveIt(self,(self.location[0]+1,self.location[1]))
            elif FW==4:
                if self.location[1]-1 > 0 and self.grid.data[self.location[0]][self.location[1]-1] == None:
                    self.grid.MoveIt(self,(self.location[0],self.location[1]-1))
        if 2 > random.randint (1,5):
            self.stomach = self.stomach-1

    def feed(self,entities):
        self.stomach=self.stomachMax
        self.stomachMax=self.stomachMax+1
        if self.stomachMax==20:
            if self.location[1]>0 and self.grid.data[self.location[0]][self.location[1]-1] == None:
                mouse3=Mouse(self.grid)
                self.grid.InsertIt(mouse3,(self.location[0],self.location[1]-1))
                entities+=[mouse3]
            elif self.location[1]>0 and self.grid.data[self.location[0]-1][self.location[1]-1] == None:
                mouse3=Mouse(self.grid)
                self.grid.InsertIt(mouse3,(self.location[0]-1,self.location[1]-1))
                entities+=[mouse3]
            elif self.location[1]>0 and self.grid.data[self.location[0]+1][self.location[1]-1] == None:
                mouse3=Mouse(self.grid)
                self.grid.InsertIt(mouse3,(self.location[0]+1,self.location[1]-1))
                entities+=[mouse3]
            self.stomachMax=4


class Plant(Entity):
    def __init__ (self,grid):
        Entity.__init__(self,"V",grid)
        self.growth =0
        self.growthMax = 24
        
    def update(self,entities):
        if self.growth==self.growthMax:
            self.growth=1
            self.grow(entities)
        else:
            self.growth=self.growth+1

    def grow(self,entities):
        if self.location[1]>0 and self.grid.data[self.location[0]][self.location[1]-1] == None:
            cheese2=Cheese(self.grid)
            self.grid.InsertIt(cheese2,(self.location[0],self.location[1]-1))
            entities+=[cheese2]
            
            


class Cheese(Entity):
    def __init__ (self,grid):
        Entity.__init__(self,"O",grid)
        self.size=4

    def update(self,entities):
        self.grid.data[self.location[0]][self.location[1]] 
        newX = random.randint (1,sizeX-2)
        newY = random.randint (1,sizeY-2)
        while self.grid.data[newX][newY]!=None:
                    newX = random.randint (1,sizeX-2)
                    newY = random.randint (1,sizeY-2)


        if self.location[0]==0:
            self.grid.MoveIt(self,(newX,newY))
        if self.location[0]==sizeX-1:
            self.grid.MoveIt(self,(newX,newY))
        if self.location[1]==0:
            self.grid.MoveIt(self,(newX,newY))
        if self.location[1]==sizeY-1:
            self.grid.MoveIt(self,(newX,newY))  

        if self.size>0:
            if self.location[0]+1<sizeX and self.grid.data[self.location[0]+1][self.location[1]].__class__.__name__ == "Mouse":
                HappyMouse=self.grid.data[self.location[0]+1][self.location[1]] 
                HappyMouse.feed(entities)
                self.size-=1

            if self.location[1]+1 <sizeY and self.grid.data[self.location[0]][self.location[1]+1].__class__.__name__ == "Mouse":
                HappyMouse=self.grid.data[self.location[0]][self.location[1]+1] 
                HappyMouse.feed(entities)
                self.size-=1

            if self.location[1]-1>0 and self.grid.data[self.location[0]][self.location[1]-1].__class__.__name__ == "Mouse":
                HappyMouse=self.grid.data[self.location[0]][self.location[1]-1] 
                HappyMouse.feed(entities)
                self.size-=1

            if self.location[0]-1>0 and self.grid.data[self.location[0]-1][self.location[1]].__class__.__name__ == "Mouse":
                HappyMouse= self.grid.data[self.location[0]-1][self.location[1]] 
                HappyMouse.feed(entities)
                self.size-=1

        else:
            self.alive=False

        return
            
        
def init(size):
    global font
    passed, failed = pygame.init()
    print('passed, failed = ' + str((passed, failed)))
    pygame.display.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Bewildering Sewer Chronicles')
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    pygame.key.set_repeat(800, 10)

    return screen

def main():
    bg_color = (0, 0, 0)
    size = width, height = 900, 900
    clock = pygame.time.Clock()

    print('Initializing pygame...')
    screen = init(size)

    running = True
  

    grid = Grid(sizeX,sizeY)
    player=Player(grid)
    mouse1=Mouse(grid)
    mouse2=Mouse(grid)
    cheese1=Cheese(grid)
    plant1=Plant(grid)
    entities=[mouse1,mouse2,plant1,cheese1]
    
    
    grid.InsertIt(player,(8,4))
    grid.InsertIt(plant1,(10,4))
    grid.InsertIt(mouse1,(1,6))
    grid.InsertIt(mouse2,(9,7))
    grid.InsertIt(cheese1,(10,3))


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                result=player.key_pressed(event.key)
                if result:
                    new_entities=[]
                    for entity in entities:
                        entity.update(entities)
                        if entity.alive==False:
                            entity.grid.KillIt(entity)
                        else:
                            new_entities+=[entity]
                    entities=new_entities



        #game.update()
        screen.fill(bg_color)
        grid.Draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()
