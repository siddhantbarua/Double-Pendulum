#!/usr/bin/env python3

import pygame
import os
from math import *
import random
import sys

# Centre Pygame window
os.environ["SDL_VIDEO_CENTERED"] = '1'

pygame.init()
pygame.mixer.music.load('claire.wav')
pygame.mixer.music.play(-1)

pygame.display.set_caption("Double Pendulum")
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

# Fonts
font = pygame.font.Font('freesansbold.ttf', 20)
param_font = pygame.font.Font('freesansbold.ttf', 12)

# Main message
text = font.render("p: Show final trajectory;     m: Stop Music;     Esc: Quit", True, (255, 255, 255), (0, 0, 0))
textRect = text.get_rect()
textRect.center = (1920 //2 , 25)

while run:
    clk.tick(fps)
    win.fill((0, 0, 30))

    # Text rectangles
    g_text = param_font.render("g = {}".format(g), True, (255, 255, 255), (0, 0, 0))
    g_textRect = g_text.get_rect()
    g_textRect.center = (30 , 20)

    l1_text = param_font.render("L1 = {}".format(l1), True, (255, 255, 255), (0, 0, 0))
    l1_textRect = l1_text.get_rect()
    l1_textRect.center = (90 , 20)

    l2_text = param_font.render("L2 = {}".format(l2), True, (255, 255, 255), (0, 0, 0))
    l2_textRect = l2_text.get_rect()
    l2_textRect.center = (150 , 20)

    m1_text = param_font.render("M1 = {}".format(m1), True, (255, 255, 255), (0, 0, 0))
    m1_textRect = m1_text.get_rect()
    m1_textRect.center = (210 , 20)

    m2_text = param_font.render("M2 = {}".format(m2), True, (255, 255, 255), (0, 0, 0))
    m2_textRect = m2_text.get_rect()
    m2_textRect.center = (270 , 20)

    win.blit(text, textRect)
    win.blit(g_text, g_textRect)
    win.blit(l1_text, l1_textRect)
    win.blit(l2_text, l2_textRect)
    win.blit(m1_text, m1_textRect)
    win.blit(m2_text, m2_textRect)


    # Sliders
    pygame.draw.rect(win , (255, 255, 255), pygame.Rect(20, g+100, 20, 5))
    pygame.draw.rect(win , (255, 255, 255), pygame.Rect(80, l1, 20, 5))
    pygame.draw.rect(win , (255, 255, 255), pygame.Rect(140, l2, 20, 5))
    pygame.draw.rect(win , (255, 255, 255), pygame.Rect(200, m1+50, 20, 5))
    pygame.draw.rect(win , (255, 255, 255), pygame.Rect(260, m2+50, 20, 5))

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

    if len(pts2) > 9:
        if (len(pts2)%10 == 0):
            clr = ((0.5*n)%255, (100-0.5*n)%255, (200-n)%255)
            clr2.append(clr)

        pygame.draw.lines(win, clr, False, pts2[-9:], 3)


    #if len(pts2) > 1:
    #    pygame.draw.lines(win, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), False, pts2)

    n += 1

    # Wires
    pygame.draw.line(win, (255,255, 255), (x0, y0), (x1, y1), 4)
    pygame.draw.line(win, (255, 255, 255), (x1, y1), (x2, y2), 4)

    # Bobs
    pygame.draw.circle(win, (150, 150, 150), (x1, y1), m1/4)
    pygame.draw.circle(win, (150, 150, 150), (x2, y2), m2/4)

    if len(pts1) > 1:
        pygame.draw.lines(win, (100, 100, 100), False, pts1)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # P to display final trajectory
            if event.key == pygame.K_p:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('bleed.wav')
                pygame.mixer.music.play(-1)
                win.fill((0, 0, 0))
                win.blit(text, textRect)
                pygame.draw.lines(win, (100, 100, 100), False, pts1)

                for i in range(0, len(clr2)):
                    pygame.draw.lines(win, clr2[i], False, pts2[i*10 : i*10+11], 2)
                run = False

            # Escape to close window
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # Stop music
            elif event.key == pygame.K_m:
                pygame.mixer.music.stop()

        elif event.type == pygame.QUIT:
            run = False

        # Update parameters based on sliders
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[0] >= 20 and pos[0] <= 40:
                g = pos[1]-100

            elif pos[0] >= 80 and pos[0] <= 100:
                l1 = pos[1]

            elif pos[0] >= 140 and pos[0] <= 160:
                l2 = pos[1]

            elif pos[0] >= 200 and pos[0] <= 220:
                m1 = pos[1]-50

            elif pos[0] >= 260 and pos[0] <= 280:
                m2 = pos[1]-50
    
    pygame.display.flip()

disp = True

while disp:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            disp = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_m:
                pygame.mixer.music.stop()

pygame.quit()


    

