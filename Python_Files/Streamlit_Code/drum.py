import numpy as np
import time
import cv2
from pygame import mixer
import streamlit as st

def state_machine(sumation, sound):
    # Check if blue color object present in the ROI
    yes = (sumation) > Hatt_thickness[0]*Hatt_thickness[1]*0.8

    # If present play the respective instrument.
    if yes and sound == 1:
        drum_clap.play()
    elif yes and sound == 2:
        drum_snare.play()
        time.sleep(0.001)
    elif yes and sound == 3:  # New condition for kick drum
        drum_kick.play()
    elif yes and sound == 4:
        drum_clap.play()

def ROI_analysis(frame, sound):
    # converting the image into HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # generating mask for
    mask = cv2.inRange(hsv, blueLower, blueUpper)

    # Calculating the number of white pixels depicting the blue color pixels in the ROI
    sumation = np.sum(mask)

    # Function that decides to play the instrument or not.
    state_machine(sumation, sound)

    return mask

Verbose = False

# Importing the audio files
mixer.init()
drum_clap = mixer.Sound('batterrm.wav')
drum_clap = mixer.Sound('hatt_copy.wav')

drum_snare = mixer.Sound('button-2.ogg')
drum_kick = mixer.Sound('kick.wav')  # New audio for kick drum

# HSV range for detecting blue color
blueLower = (80, 150, 10)
blueUpper = (120, 255, 255)

# Frame acquisition from webcam/USB camera
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
H, W = frame.shape[:2]

# Reading the image of hi-hat, snare, and kick for augmentation.
Hatt = cv2.resize(cv2.imread('Hatt.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
Hatt_copy = cv2.resize(cv2.imread('Hatt copy.png'), (200, 100), interpolation=cv2.INTER_CUBIC)

Snare = cv2.resize(cv2.imread('Snare.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
Kick = cv2.resize(cv2.imread('kick.png'), (200, 100), interpolation=cv2.INTER_CUBIC)  # New image for kick drum

# Setting the ROI area for blue color detection
Hatt_center = [np.shape(frame)[1]*1//8, np.shape(frame)[0]*6//8]
Snare_center = [np.shape(frame)[1]*3//8, np.shape(frame)[0]*6//8]
Kick_center = [np.shape(frame)[1]*5//8, np.shape(frame)[0]*6//8]
Hatt_copy_center = [np.shape(frame)[1]*6//8, np.shape(frame)[0]*6//8]


Hatt_thickness = [200, 100]
Hatt_top = [Hatt_center[0]-Hatt_thickness[0]//2, Hatt_center[1]-Hatt_thickness[1]//2]
Hatt_btm = [Hatt_center[0]+Hatt_thickness[0]//2, Hatt_center[1]+Hatt_thickness[1]//2]

Hatt_copy_thickness = [200, 100]
Hatt_copy_top = [Hatt_copy_center[0]-Hatt_copy_thickness[0]//2, Hatt_copy_center[1]-Hatt_copy_thickness[1]//2]
Hatt_copy_btm = [Hatt_copy_center[0]+Hatt_copy_thickness[0]//2, Hatt_copy_center[1]+Hatt_copy_thickness[1]//2]

Snare_thickness = [200, 100]
Snare_top = [Snare_center[0]-Snare_thickness[0]//2, Snare_center[1]-Snare_thickness[1]//2]
Snare_btm = [Snare_center[0]+Snare_thickness[0]//2, Snare_center[1]+Snare_thickness[1]//2]

Kick_thickness = [200, 100]
Kick_top = [Kick_center[0]-Kick_thickness[0]//2, Kick_center[1]-Kick_thickness[1]//2]
Kick_btm = [Kick_center[0]+Kick_thickness[0]//2, Kick_center[1]+Kick_thickness[1]//2]

st.title('Air Drums')

Verbose = st.checkbox('Display ROI')

stframe = st.image([])

# time.sleep(1)
time.sleep(1)



while True:
    # Grab the current frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    if not ret:
        break

    # Selecting ROI corresponding to snare
    snare_ROI = np.copy(frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]])
    mask = ROI_analysis(snare_ROI, 1)

    # Selecting ROI corresponding to Hi-hat
    hatt_ROI = np.copy(frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]])
    mask = ROI_analysis(hatt_ROI, 2)

    # Selecting ROI corresponding to Kick drum
    kick_ROI = np.copy(frame[Kick_top[1]:Kick_btm[1], Kick_top[0]:Kick_btm[0]])
    mask = ROI_analysis(kick_ROI, 3)  # Play kick drum audio

    Hatt_copy_ROI = np.copy(frame[Hatt_copy_top[1]:Hatt_copy_btm[1], Hatt_copy_top[0]:Hatt_copy_btm[0]])
    mask = ROI_analysis(Hatt_copy_ROI, 4)

    # Writing text on the image
    cv2.putText(frame, 'Project: Air Drums', (10, 30), 2, 1, (20, 20, 20), 2)

    # Display the ROI to view the blue colour being detected
    if Verbose:
        # Displaying the ROI in the Image
        frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]] = cv2.bitwise_and(
            frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]],
            frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]], mask=mask[Snare_top[1]:Snare_btm[1],
                                                                                   Snare_top[0]:Snare_btm[0]])
        frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]] = cv2.bitwise_and(
            frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]],
            frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]], mask=mask[Hatt_top[1]:Hatt_btm[1],
                                                                                 Hatt_top[0]:Hatt_btm[0]])
        frame[Kick_top[1]:Kick_btm[1], Kick_top[0]:Kick_btm[0]] = cv2.bitwise_and(
            frame[Kick_top[1]:Kick_btm[1], Kick_top[0]:Kick_btm[0]],
            frame[Kick_top[1]:Kick_btm[1], Kick_top[0]:Kick_btm[0]], mask=mask[Kick_top[1]:Kick_btm[1],
                                                                                 Kick_top[0]:Kick_btm[0]])
        
        frame[Hatt_copy_top[1]:Hatt_copy_btm[1], Hatt_copy_top[0]:Hatt_copy_btm[0]] = cv2.bitwise_and(
            frame[Hatt_copy_top[1]:Hatt_copy_btm[1], Hatt_copy_top[0]:Hatt_copy_btm[0]],
            frame[Hatt_copy_top[1]:Hatt_copy_btm[1], Hatt_copy_top[0]:Hatt_copy_btm[0]], mask=mask[Hatt_copy[1]:Hatt_copy_btm[1],
                                                                                Hatt_copy_top[0]:Hatt_copy_btm[0]])
    else:
        # Augmenting the image of the instruments on the frame
        frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]] = cv2.addWeighted(Snare, 1,
                                                                                      frame[Snare_top[1]:Snare_btm[1],
                                                                                      Snare_top[0]:Snare_btm[0]], 1, 0)
        frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]] = cv2.addWeighted(Hatt, 1,
                                                                                    frame[Hatt_top[1]:Hatt_btm[1],
                                                                                    Hatt_top[0]:Hatt_btm[0]], 1, 0)
        frame[Kick_top[1]:Kick_btm[1], Kick_top[0]:Kick_btm[0]] = cv2.addWeighted(Kick, 1,
                                                                                    frame[Kick_top[1]:Kick_btm[1],
                                                                                    Kick_top[0]:Kick_btm[0]], 1, 0)

        frame[Hatt_copy_top[1]:Hatt_copy_btm[1],Hatt_copy_top[0]:Hatt_copy_btm[0]] = cv2.addWeighted(Hatt_copy, 1,
                                                                                    frame[Hatt_copy_top[1]:Hatt_copy_btm[1],
                                                                                    Hatt_copy_top[0]:Hatt_copy_btm[0]], 1, 0)

    stframe.image(frame, channels="BGR")

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# Cleanup the camera and close any open windows
# camera.release()
# cv2.destroyAllWindows()