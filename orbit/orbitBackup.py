import sys
import time

import math
import pygame
import random

FPS = 30
EPSILON = 0.0001
FONT_SIZE = 20
font = None
sizeX = 40
sizeY = 30


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

def main():
    bg_color = (0, 0, 0)
    size = width, height = 900, 900
    clock = pygame.time.Clock()

    print('Initializing pygame...')
    screen = init(size)

    running = True

    t = 0
    dt = 0.1

    planet_theta = 0
    planet_omega = 0.1
    moon_theta = 0
    moon_omega = 0.3
  
    planet_pos = vec2f(0, 0)
    planet_radius = 5
    planet_orbit_radius = 20
    planet_color = (255, 0, 0)

    moon_pos = vec2f(0, 0)
    moon_radius = 1
    moon_orbit_radius = planet_radius + 2
    moon_color = (0, 0, 255)

    # render -view_radius <= x <= view_radius
    #        -view_radius <= y <= view_radius
    view_radius = 40
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
        
        planet_theta = t * planet_omega
        planet_pos = vec2f(math.cos(planet_theta) * planet_orbit_radius,
                           math.sin(planet_theta) * planet_orbit_radius)

        moon_theta = t * moon_omega
        moon_pos = planet_pos + vec2f(math.cos(moon_theta) * moon_orbit_radius,
                                      math.sin(moon_theta) * moon_orbit_radius)

        # draw
        screen.fill(bg_color)
        planet_screen_pos = world_to_screen_vec2f(planet_pos,
                                                  world_dims,
                                                  screen_dims)
        planet_screen_radius = world_to_screen_float(planet_radius,
                                                     world_dims,
                                                     screen_dims)
        moon_screen_pos = world_to_screen_vec2f(moon_pos,
                                                world_dims,
                                                screen_dims)
        moon_screen_radius = world_to_screen_float(moon_radius,
                                                   world_dims,
                                                   screen_dims)
        pygame.draw.circle(screen,
                           planet_color,
                           planet_screen_pos.ituple(),
                           planet_screen_radius)
        pygame.draw.circle(screen,
                           moon_color,
                           moon_screen_pos.ituple(),
                           moon_screen_radius)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()
