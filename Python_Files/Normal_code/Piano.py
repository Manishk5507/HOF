import cv2
import pygame
from cvzone.HandTrackingModule import HandDetector

# Initialize pygame
pygame.mixer.init()

# Load sound for each white key
sound_q = pygame.mixer.Sound("sound_q.wav")  # Replace "sound_q.wav" with your sound file for key 'q'
sound_w = pygame.mixer.Sound("sound_w.wav")  # Replace "sound_w.wav" with your sound file for key 'w'
sound_e = pygame.mixer.Sound("sound_e.wav")  # Replace "sound_e.wav" with your sound file for key 'e'
sound_r = pygame.mixer.Sound("sound_r.wav")  # Replace "sound_r.wav" with your sound file for key 'r'
sound_t = pygame.mixer.Sound("sound_t.wav")  # Replace "sound_t.wav" with your sound file for key 't'
sound_y = pygame.mixer.Sound("sound_q.wav")  # Replace "sound_y.wav" with your sound file for key 'y'
sound_u = pygame.mixer.Sound("sound_w.wav")  # Replace "sound_u.wav" with your sound file for key 'u'

# Function to play sound based on the position of the rectangle
def play_sound(key):
    if key == 'q':
        sound_q.play()
    elif key == 'w':
        sound_w.play()
    elif key == 'e':
        sound_e.play()
    elif key == 'r':
        sound_r.play()
    elif key == 't':
        sound_t.play()
    elif key == 'y':
        sound_y.play()
    elif key == 'u':
        sound_u.play()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)
    
    # Draw white keys
    white_keys = {'q': (50, 400), 'w': (200, 400), 'e': (350, 400), 'r': (500, 400), 't': (650, 400),
                  'y': (800, 400), 'u': (950, 400)}
    for key, (rect_x, rect_y) in white_keys.items():
        rect_width, rect_height = 100, 200
        rect_color = (255, 255, 255)
        cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), rect_color, cv2.FILLED)
        
        # Add text
        cv2.putText(img, key, (rect_x + 40, rect_y + 50), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
    
    # Draw black keys
    black_keys = {(125, 400), (275, 400), (425, 400), (575, 400), (725, 400), (875, 400)}
    for rect_x, rect_y in black_keys:
        rect_width, rect_height = 60, 120
        rect_color = (0, 0, 0)
        cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), rect_color, cv2.FILLED)
    
    cv2.imshow("Image", img)
    
    # Call play_sound function when a hand is detected over a white key
    if hands:
        for hand in hands:
            hand_x, hand_y = hand["lmList"][8][0], hand["lmList"][8][1]  # Position of the tip of the index finger
            for key, (key_x, key_y) in white_keys.items():
                if key_x <= hand_x <= key_x + 100 and key_y <= hand_y <= key_y + 200:
                    play_sound(key)
    
    cv2.waitKey(1)