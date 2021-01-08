#!/usr/bin/env python3

import pygame
import os
from math import *
import random

# Centre Pygame window
os.environ["SDL_VIDEO_CENTERED"] = '1'

pygame.init()
pygame.mixer.music.load('claire.wav')
pygame.mixer.music.play(-1)

pygame.display.set_caption("p: Show trajectory map")
fps = 30

t_step = 0.3

win = pygame.display.set_mode((1920, 1080))
clk = pygame.time.Clock()

# Parameters
# Masses 
m1 = 30
m2 = 35
# Lengths
l1 = 150
l2 = 200
# Gravitational acceleration
g = 9.8

# Initial Conditions
# Angles
theta1 = pi/2
theta2 = pi/2
# Angular velocities
w1 = 0
w2 = 0
# Angular acceleration
alpha1 = 0.5
alpha2 = -0.5

# List of points
pts1 = []
pts2 = []
clr2 = []

# Fixed point
x0 = 1920 // 2
y0 = 1080 // 2

run = True
n = 20

while run:
    clk.tick(fps)
    win.fill((0, 0, 0))

    # Nerdy Stuff
    num1 = -g*(2*m1+m2)*sin(theta1) - m2*g*sin(theta1-2*theta2) - 2*sin(theta1-theta1)*m2*(w2*w2*l2+w1*w1*l1*cos(theta1-theta2))
    denom1 = l1*(2*m1+m2-m2*cos(2*theta1-2*theta2))

    num2 = 2*sin(theta1-theta2)*(w1*w1*l1*(m1+m2) + g*(m1+m2)*cos(theta1) + w2*w2*l2*m2*cos(theta1-theta2))
    denom2 = l2*(2*m1+m2-m2*cos(2*theta1-2*theta2))

    alpha1 = num1 / denom1
    alpha2 = num2 / denom2

    x1 = x0 + l1*sin(theta1)
    y1 = y0 + l1*cos(theta1)

    x2 = x1 + l2*sin(theta2)
    y2 = y1 + l2*cos(theta2)

    #Update coordinates
    w1 += t_step*alpha1
    w2 += t_step*alpha2
    theta1 = (theta1 + t_step*w1) % (2*pi)
    theta2 = (theta2 + t_step*w2) % (2*pi)

    pts1.append((x1, y1))
    pts2.append((x2, y2))


    #if len(pts2) > 1 and len(pts2) < 10:
    #    pygame.draw.lines(win, (), False, pts2)

    if len(pts2) > 9:
        if (len(pts2)%10 == 0):
            clr = ((0.5*n)%255, (100-0.5*n)%255, (200-n)%255)
            clr2.append(clr)

        pygame.draw.lines(win, clr, False, pts2[-9:], 3)


    #if len(pts2) > 1:
    #    pygame.draw.lines(win, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), False, pts2)

    # for pt in pts2:
    #     if len(pts2) > 1:
    #         pygame.draw.lines(win, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), False, pts2)
            #pygame.draw.line(win, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), pts2[n-1], pts2[n])


    n += 1

    # Wires
    pygame.draw.line(win, (255,255, 255), (x0, y0), (x1, y1), 4)
    pygame.draw.line(win, (255, 255, 255), (x1, y1), (x2, y2), 4)

    # Bobs
    pygame.draw.circle(win, (100, 100, 100), (x1, y1), 10)
    pygame.draw.circle(win, (150, 150, 150), (x2, y2), 10)

    if len(pts1) > 1:
        pygame.draw.lines(win, (100, 100, 100), False, pts1)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('bleed.wav')
                pygame.mixer.music.play(-1)
                win.fill((0, 0, 0))
                pygame.draw.lines(win, (100, 100, 100), False, pts1)
                for i in range(0, len(clr2)):
                    pygame.draw.lines(win, clr2[i], False, pts2[i*10 : i*10+11], 2)
                run = False

        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

disp = True
while disp:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            disp = False

pygame.quit()


    

