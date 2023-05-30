# print("test")
def getPos():
    import cv2
    import mediapipe as mp
    import numpy as np
    import math
    import time

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    center_coordinates =(0,0)
            # Radius of circle
    radius = 20

    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        min_detection_confidence=0.9,
        min_tracking_confidence=0.5) as hands:
        closed = True
        jump = 0
        while cap.isOpened():
            start = time.time()
            success, image = cap.read()
            image_size=image.shape
            image_height=image_size[0]
            image_width=image_size[1]
            if not success:
                print("Ignoring empty camera frame.")
                break
                
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            handIn = False
            
            
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
                        closed = True
                    else:
                        closed = False

                    

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
            # print("hello")
            end = time.time()
            # print(end - start)
            # print(center_coordinates)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
if __name__ == '__main__':
    getPos()