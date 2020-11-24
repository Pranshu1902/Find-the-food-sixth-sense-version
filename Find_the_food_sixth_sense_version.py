# Made by Pranshu Aggarwal

# Find the food sixth sense verion game

import pygame
import random
import numpy as np
import cv2 as cv

green = [0,255,0]
red = [255,0,0]
# creating the list of random values for the food
a = []
b = []

for i in range(25,485,10):
    a.append(i)
for i in range(75,485,10):
    b.append(i)

# initialization

pygame.init()

dis = pygame.display.set_mode((500,500))

pygame.display.set_caption("Find The Food")

img = pygame.image.load('intro.png')
dis.blit(img, (10,100))
font = pygame.font.Font('freesansbold.ttf', 40)


text = font.render('Start', True, green, red)

textRect = text.get_rect()  
textRect.center = (190, 35)

dis.blit(text, textRect)

pygame.display.update()

white = [255,255,255]
green = (0, 255, 0) 
blue = (0, 0, 128)


# text

font = pygame.font.Font('freesansbold.ttf', 20) 
text = font.render('Welcome! Use arrows to move. If you go out of the screen then you lose', True, green, blue) 

text2 = font.render('Press Q to quit and R to restart', True, green, blue)


textRect = text.get_rect()  
textRect.center = (350, 15)

textrect = text2.get_rect()
textrect.center = (150,50)

x = 100
y = 100

pygame.display.update()

score = 0

pxx = 0
pyy = 0

px = 205
py = 205
# sixth sense

cam = cv.VideoCapture(0)

lower_value = np.array([20,100,100])
upper_value = np.array([40,255,255])

# main gane loop


run = True

def mainloop(run, x, y, px, py):
    global score
    while run:
        pygame.time.delay(100)
        ret,frame = cam.read()
        frame = cv.flip(frame,1)
    
        w = frame.shape[1]
        h = frame.shape[0]
    
        image_smooth = cv.GaussianBlur(frame,(7,7),0)

        mask = np.zeros_like(frame)

        mask[50:350,30:350] = [255,255,255]

        image_roi = cv.bitwise_and(image_smooth,mask)
        cv.rectangle(frame,(50,50),(350,350),(0,0,255),2)
        cv.line(frame,(150,50),(150,350),(0,0,255),1)
        cv.line(frame,(250,50),(250,350),(0,0,255),1)
        cv.line(frame,(50,150),(350,150),(0,0,255),1)
        cv.line(frame,(50,250),(350,250),(0,0,255),1)


        image_hsv = cv.cvtColor(image_roi,cv.COLOR_BGR2HSV)
        image_threshold = cv.inRange(image_hsv,lower_value,upper_value)
    
        contours, hierachy = cv.findContours(image_threshold,\
                                             cv.RETR_TREE,\
                                             cv.CHAIN_APPROX_NONE)

        if(len(contours)!=0):
           areas = [cv.contourArea(c) for c in contours]
           max_index = np.argmax(areas)
           cnt = contours[max_index]

           M = cv.moments(cnt)
           if(M['m00']!=0):
               cx = int(M['m10']/M['m00'])
               cy = int(M['m01']/M['m00'])
               cv.circle(frame,(cx,cy),4,(0,0,255),-1)
               if cx in range(150,250):
                   if cy<150 and y > 60:
                       y-=10
                   elif cy>250 and y < 490:
                       y+=10
               if cy in range(150,250):
                   if cx<150 and x > 0:
                       x-=10
                   elif cx>250 and x < 490:
                       x+=10

           cv.imshow('Object_Detection',frame)


        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        x1 = x+5 # x coordinate of center of rectangle
        y1 = y+5 # y coordinate of center of rectangle
        dis.fill(white)
    
        # stop the game if the player goes out of screen
        if x>790 or x<0 or y>590 or y<0 or keys[pygame.K_q]:
            run = False

        # restart after pressing "R"
        if keys[pygame.K_r]:
            score = 0
            mainloop(True, 100,100,205,205)
    
    # for the first default position of the food
        if x1 == 205 and y1 == 205:
            px = random.choice(a)
            py = random.choice(b)
            dis.fill(white)
            score+=1
            x+=10
     
    # general for all positions of the food

        if x1 == px and y1 == py:
            px = random.choice(a)
            py = random.choice(b)
            dis.fill(white)
            score+=1
            x+=10

        # displaying the score
        value = font.render("Your Score: " + str(score), True, green, blue)
        dis.blit(value, [360, 35])
    
        pygame.draw.circle(dis, [255,0,0],[px,py], 5, 0)
        pygame.draw.rect(dis, [0, 255, 0], [x,y, 10, 10])
        dis.blit(text, textRect)
        dis.blit(text2, textrect)
        pygame.display.update()

    cam.release()
    pygame.quit()

game = True

while game:
    x, y = pygame.mouse.get_pos()
    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= 300 and x >= 110 and y <= 60 and y >= 10:
                dis.fill([255,255,255])
                pygame.display.update()
                mainloop(True, 100, 100, 205, 205)
