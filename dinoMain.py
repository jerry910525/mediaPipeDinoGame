#讀取圖片
from PIL import Image
from matplotlib import pyplot as plt
import time
import random

import cv2
import mediapipe as mp
import numpy as np
import math
import time

#def for handRec
def calNewPos(ori,tar,speed):
    if tar>ori:
        ori+=speed
    else:
        ori-=speed
    return ori
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
center_coordinates =(0,0)
    # Radius of circle
radius = 20
# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2
#model_complexity of mp.Pose to 0.

# mp.Pose.model_complexity = 0
# cap = cv2.VideoCapture(0)


# 定義圖片、加載圖片 不可使用def
cactus = Image.open("Assets\Cactus\LargeCactus1.png")
dino = Image.open('Assets\Dino\DinoJump.png')  # 圖片路徑
# dittoa = Image.open('百百.png')
# ball = Image.open('球.png')
# balla = Image.open('球球.png')
# blue_ball = Image.open('藍球.png')

def input_image(input_path,output_path,resize_image,width,height):
    image = Image.open(input_path)
    resized_image = image.resize((width, height))
    resized_image.save(output_path)
    resize_image = Image.open(output_path)

input_image('Assets\Dino\DinoJump.png','Assets\Dino\DinoJump.png',dino,80,80)
# input_image('百百.png','百百(1).png',dittoa,80,80)
# input_image('球.png','球(1).png',ball,50,50)
# input_image('球球.png','球球(1).png',balla,50,50)
# input_image('藍球.png','藍球(1).png',blue_ball,50,50)

# 定義圖片、加載圖片 不可使用def
dino = Image.open('Assets\Dino\DinoJump.png')  # 圖片路徑


# 顯示圖片
def show_image(image):
    plt.imshow(image)
    plt.axis('off')  # 不顯示座標軸
    plt.show()
# show_image(ditto)
# show_image(dittoa)
# show_image(ball)
# show_image(balla)
# show_image(blue_ball)

####################
#使圖片在視窗中移動
import pygame

# 初始化pygame
pygame.init()

# 視窗大小
window_width = 1000
window_height = 600

# 創建視窗
window =pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Moving Image')
#重新定義圖片，以pygame
dino = pygame.image.load('Assets\Dino\DinoJump.png')  # 替換為你的圖片路徑
cactus = pygame.image.load("Assets\Cactus\LargeCactus1.png")

dino_width = dino.get_width()
dino_height = dino.get_height()
cactus_width = cactus.get_width()
cactus_height = cactus.get_height()


# 圖片初始位置
dino_x = random.randint(dino_width, window_width - dino_height)
dino_y = 260
cactus_x = window_width

high = 550
width = 50
times=0
op=0
site_x = 500
site_y = 300
# blue_blue移動速度
speeda_x = random.randint(1, 2)
speeda_y = random.randint(1, 2)
# 遊戲主迴圈
cap = cv2.VideoCapture(0)

########
running = True
hands = mp_hands.Hands(
        min_detection_confidence=0.9,
        min_tracking_confidence=0.5)
closed = True
jump = 0
jumping = 0
target = 0
up = 0
speed = 50
ori_target = 260
cactusMoving = False
########
while running:
    start = time.time()
    if not cactusMoving:
        test = random.uniform(0,50)
        # print(test)
        if 12==int(test):
            print("!!!!!!!!!!!!")
            cactusMoving = True
            cactus_x = window_width
        else:
            cactus_x = -1000
    success, image = cap.read()
    image_size=image.shape
    image_height=image_size[0]
    image_width=image_size[1]
    # print("test")
    if not success:
        print("Ignoring empty camera frame.")
        continue
    # else:
        # print("get")
    
    
   
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    handIn = False
    # print("!!!!")
    if not jumping:
        if results.multi_hand_landmarks:
            handIn = True
            for hand_landmarks in results.multi_hand_landmarks:
                
                
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y

                sx = int(x * image_width)
                xy = int(y * image_height)

                x1, y1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

                if y1>y: #closed
                    if not closed:
                        jump = 1
                        jumping = 1
                        up = 1
                    closed = True
                else:
                    closed = False
    else: #jumping
        if dino_y<=target:
            up = False
        if up:
            dino_y = calNewPos(dino_y,target,speed)
        else:
            dino_y = calNewPos(dino_y,ori_target,speed)

            if dino_y>=ori_target:
                jumping = False
    if cactusMoving:
        cactus_x  = calNewPos(cactus_x,0,random.uniform(30,30))
        if cactus_x<=0:
            cactusMoving = False
        if cactus_x<window_width/2+30 and cactus_x>=window_width/2-30 and dino_y>100:
            print("dead")
    # print(cactus_x)
    # cv2.imshow('MediaPipe Hands', image)

            # mp_drawing.draw_landmarks(
            #     image,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style())

            
            # mp_drawing.draw_landmarks( image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    if handIn:
        # print("!!!")
        # if closed:
        #     print("closed")
        # else:
        #     print("opened")
        image = cv2.circle(image, center_coordinates, radius, color, thickness)
    else:
        image = cv2.circle(image, (373,328), radius, color, thickness)
    if jump:
        jump=0
        print("jump!")
    # 事件處理
    
    # 移動速度
    
    window.fill((0, 0, 0))

    # 繪製圖片
    
    bg = pygame.image.load("bg.png")
    bg = pygame.transform.scale(bg, (window_width, window_height))
    window.blit(bg, (0, 0))
    window.blit(cactus,(cactus_x,window_height/2-random.uniform(55,55)))
    window.blit(dino,  (window_width/2,dino_y))
    #INSIDE OF THE GAME LOOP
    
        # time.sleep(1)
    # print(dino_y)
    # window.blit(dittoa, (dittoa_x, dittoa_y))
    # window.blit(ball,(ball_x, ball_y))
    # window.blit(balla,(balla_x, balla_y))
    # window.blit(blue_ball,(blue_ball_x, blue_ball_y))
    # 更新視窗
    pygame.display.flip()
# 退出遊戲
pygame.quit()