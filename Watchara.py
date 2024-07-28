
import pygame 
import cv2    
from cvzone.HandTrackingModule import HandDetector 
import numpy 
import random
import time 
pygame.init()
fps = 30
clock = pygame.time.Clock()
cap = cv2.VideoCapture(0)
cap.set(3,800) 
cap.set(4,600) 
detector = HandDetector(detectionCon=0.8,maxHands=1)
screen = pygame.display.set_mode((800,600))
title = pygame.display.set_caption('Lucky Game')
meteor1 = pygame.image.load('sprite/Meteors/Meteor_07.png')
meteor1 = pygame.transform.scale(meteor1,(100,100))

meteor1_pos_x = random.randint(100,700)
meteor1_pos_y = 500

font1 = pygame.font.Font('font/RobotoMono-Regular.ttf',30)

score = 0
Hp = 10
score_text = font1.render('SCORE: {}'.format(score),True,(255,255,255))
Hp_text = font1.render('HP: {}'.format(Hp),True,(255,255,255))

running = True
start_time = time.time()
final_time = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            cap.release()
    time_remain = int(final_time - (time.time()-start_time))
    if time_remain <=0 or Hp == 0:
        screen.fill((0,0,0))
        game_over_text = font1.render('Game Over!',True,(255,0,0))
        score_text = font1.render('Your Score: {}'.format(score),True,(0,0,0))
        screen.blit(game_over_text,(275,100))
        screen.blit(score_text,(250,150))
        cap.release()
    else:
        ret,frame = cap.read()
        frame = cv2.flip(frame,1)
        hands,frame = detector.findHands(frame, flipType=False)
        meteor1_hit_point = pygame.Rect(meteor1_pos_x,meteor1_pos_y,100,100)
       
        if meteor1_pos_y < -100:
            meteor1_pos_y = 500
            meteor1_pos_x = random.randint(100,700)
        else:
            meteor1_pos_y -= 2
        
        if hands:
            hand1 = hands[0]
            hand_x,hand_y,hand_z = hand1['lmList'][8]
            hand_hit_point = pygame.Rect(hand_x,hand_y,100,100)
            if hand_hit_point.colliderect(meteor1_hit_point):
                score += random.randint(-10,10)
                if score == 10:
                    score += random.randint(2,5)
                if score == 25:
                    score *= random.randint(1,2)
                if score == 50:
                    score *=random.randint(1,3)
                    Hp /= random.randint(1,2)
                if score == 65:
                    score += random.randint(2,5)
                    Hp -= random.randint(-1,1)
                if score == 80:
                    score += random.randint(2,5)
                    Hp -= random.randint(-1,1)
                if score == 90:
                    score += random.randint(2,5)
                    Hp -= random.randint(-1,1)
                if score == 99:
                    score -= random.randint(-1,5)
                    Hp -= random.randint(-1,5)
                
                score_text = font1.render('SCORE: {}'.format(score),True,(255,255,255))
                
                meteor1_pos_y = 500
                meteor1_pos_x = random.randint(100,700)
                
                
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frameRGB = numpy.rot90(frameRGB)
        
        img = pygame.surfarray.make_surface(frameRGB).convert()
        img = pygame.transform.flip(img,True ,False )
        img = pygame.transform.scale(img,(800,600))
        
        
        screen.blit(img,(0,0))
        screen.blit(score_text,(0,0))
        screen.blit(Hp_text,(0,50))
        time_text = font1.render('Time: {}'.format(time_remain),True,(255,255,255))
        screen.blit(time_text,(500,0))
        screen.blit(meteor1,(meteor1_pos_x,meteor1_pos_y))

    pygame.display.update()
    clock.tick(fps)           
pygame.quit()
    