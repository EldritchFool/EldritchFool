import sys
import time

import math
import pygame
import random

FPS = 30
EPSILON = 0.0001
FONT_SIZE = 20
font = None
WIREFRAME = False


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

    def ituple(self):
        return (int(self.x), int(self.y))

def dist(a, b):
    return (a - b).mag()

def world_to_screen_vec2f(pos, world_size, screen_size):
    lower_x = -world_size.x / 2
    x_rel_to_lower = pos.x - lower_x
    percent_x = x_rel_to_lower / world_size.x

    lower_y = -world_size.y / 2
    y_rel_to_lower = pos.y - lower_y
    percent_y = y_rel_to_lower / world_size.y
    return vec2f(percent_x * screen_size.x,
                 percent_y * screen_size.y)

def world_to_screen_float(val, world_size, screen_size):
    if world_size.x != world_size.y or \
       screen_size.x != screen_size.y:
        print('Error!  world_to_screen_float() only works on square views!')
        exit()

    percent = val / world_size.x
    return percent * screen_size.x

def init(size):
    global font
    passed, failed = pygame.init()
    print('passed, failed = ' + str((passed, failed)))
    pygame.display.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Bewildering Orbit Chronicles')
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    pygame.key.set_repeat(800, 10)

    return screen

class Orbiter(object):
    def __init__(self, myTheta, myOmega, myOrbitRadius, myRadius, myColor, myParent):
        self.theta=myTheta
        self.omega=myOmega
        self.orbitRadius=myOrbitRadius
        self.color=myColor
        self.parent=myParent
        self.pos = vec2f(0, 0)
        self.radius = myRadius

    def getPos(self):
        return self.pos

    def update(self,dt):
        if self.parent is None:
            self.theta +=dt * self.omega
            self.pos = vec2f(math.cos(self.theta) * self.orbitRadius,
                           math.sin(self.theta) * self.orbitRadius)
        else:
            self.theta += dt * self.omega
            self.pos = self.parent.getPos() + vec2f(math.cos(self.theta) * self.orbitRadius,
                                      math.sin(self.theta) * self.orbitRadius)
     
    

    def draw(self,screen,world_dims,screen_dims):
        planet_screen_pos = world_to_screen_vec2f(self.pos,
                                                  world_dims,
                                                  screen_dims)
        planet_screen_radius = world_to_screen_float(self.radius,
                                                     world_dims,
                                                     screen_dims)

        width=1 if WIREFRAME else 0
        pygame.draw.circle(screen,
                           self.color,
                           planet_screen_pos.ituple(),
                           planet_screen_radius, width)

        if WIREFRAME and self.parent:
            parent = self.parent
            parent_screen_pos = world_to_screen_vec2f(parent.pos,
                                                      world_dims,
                                                      screen_dims)
            pygame.draw.line(screen,
                             (255, 255, 255),
                             planet_screen_pos.ituple(),
                             parent_screen_pos.ituple())


def main():
    bg_color = (0, 0, 0)
    size = width, height = 900, 900
    clock = pygame.time.Clock()

    print('Initializing pygame...')
    screen = init(size)

    running = True

    t = 0
    dt = 0.1
    #init
        #myTheta, rotation speed, myOrbitRadius, myRadius, myColor, myParent

    planets = []
    planets.append(Orbiter(0, 0, 0, 0, (0,0,0), None))#0
    planets.append(Orbiter(0, .01, 400, 25, (255,255,0), planets[0]))#1 RhoAlpha
    
    planets.append(Orbiter(math.pi, .01, 400, 0, (0,0,0), planets[0]))#2 barycenter
    planets.append(Orbiter(0, 1, 15, 15,(255,255,0), planets[2]))#RhoBetta
    planets.append(Orbiter(math.pi, 1, 15, 15.2,(255,215,0), planets[2]))#RhoGamma

    planets.append(Orbiter(0, .7, 37.6, 5,(128,128,128), planets[1])) #sybsystem A
   # planets.append(Orbiter(0, .6, 44.4, 5,(100,100,150), planets[1]))
   # planets.append(Orbiter(0, .5, 52.7, 5,(100,100,150), planets[1]))
    planets.append(Orbiter(0, .4, 61.8, 10,(255,140,0), planets[1]))
   # planets.append(Orbiter(0, .3, 84.5, 5,(100,100,150), planets[1]))
    planets.append(Orbiter(0, .2, 131.8, 5,(128,128,128), planets[1]))
    planets.append(Orbiter(0, .1, 172.6, 10,(255,165,0), planets[1]))
    planets.append(Orbiter(0, .05, 250.2, 10,(255,165,0), planets[1]))

    planets.append(Orbiter(0, 6, 12, 5,(0,128,0), planets[6]))
    planets.append(Orbiter(0, 3, 18, 5,(0,0,128), planets[6]))



    planets.append(Orbiter(0, .5, 47.7, 5,(128,128,0), planets[2])) #subsystem BC
    planets.append(Orbiter(0, .4, 54.8, 5,(0,128,128), planets[2]))
    planets.append(Orbiter(0, .3, 71.9, 5,(128,128,128), planets[2]))
    planets.append(Orbiter(0, .2, 99.1, 10, (255,165,0), planets[2]))
    planets.append(Orbiter(0, .1, 160.6, 10,(255,165,0), planets[2]))
    planets.append(Orbiter(0, .05, 240.9, 10,(255,165,0), planets[2]))
    

    # render -view_radius <= x <= view_radius
    #        -view_radius <= y <= view_radius

    view_radius = 600
    world_dims = vec2f(2 * view_radius, 2 * view_radius)
    screen_dims = vec2f(width, height)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        # update
        t += dt
        for planet in planets:
            planet.update(dt)

        # draw
        screen.fill(bg_color)
        
        for planet in planets:
            planet.draw(screen, world_dims, screen_dims)


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
main()


    


