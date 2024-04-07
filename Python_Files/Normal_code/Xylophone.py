import numpy as np
import time
import cv2
from pygame import mixer
import pickle


def state_machine(sumation, sound):
    # Check if blue color object present in the ROI
    yes = (sumation) > A1_thickness[0]*A1_thickness[1]*0.8

    # If present play the respective instrument.
    if yes and sound == 1:
        xylo_A1.play()
    elif yes and sound == 2:
        xylo_A2.play()
    elif yes and sound == 3:  # New condition for A4 drum
        xylo_A3.play()
    elif yes and sound == 4:
        xylo_A4.play()
    elif yes and sound == 5:
        xylo_A5.play()
    elif yes and sound == 6:
        xylo_A6.play()
    elif yes and sound == 7:
        xylo_A7.play()

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
def camera_access(frame):
    
    # ret,buffer=cv2.imencode('.jpg',frame)
    #         frame=buffer.tobytes()

    #     yield(b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # while True:
            
    #     ## read the camera frame
    #     success,frame=camera.read()
    #     if not success:
    #         break
    #     else:
    #         ret,buffer=cv2.imencode('.jpg',frame)
    #         frame=buffer.tobytes()

    #     yield(b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    Verbose = False

    mixer.init()
    xylo_A1 = mixer.Sound('A1new.mp3')
    xylo_A2 = mixer.Sound('A2new.mp3')
    xylo_A3 = mixer.Sound('A3new.mp3')
    xylo_A4 = mixer.Sound('A4new.mp3')
    xylo_A5 = mixer.Sound('A5.wav')
    xylo_A6 = mixer.Sound('A6.wav')
    xylo_A7 = mixer.Sound('A7.wav')

    blueLower = (80, 150, 10)
    blueUpper = (120, 255, 255)

    # camera = cv2.VideoCapture(0)
    # ret, frame = camera.read()
    # H, W = frame.shape[:2]

    A1 = cv2.resize(cv2.imread('A1.png'), (300, 150), interpolation=cv2.INTER_CUBIC)
    A2 = cv2.resize(cv2.imread('A2.png'), (300, 150), interpolation=cv2.INTER_CUBIC)
    A3 = cv2.resize(cv2.imread('A3.png'), (300, 150), interpolation=cv2.INTER_CUBIC)
    A4 = cv2.resize(cv2.imread('A4.png'), (300, 150), interpolation=cv2.INTER_CUBIC)
    A5 = cv2.resize(cv2.imread('A5.png'), (300, 150), interpolation=cv2.INTER_CUBIC)
    A6 = cv2.resize(cv2.imread('A6.png'), (300, 150), interpolation=cv2.INTER_CUBIC)
    A7 = cv2.resize(cv2.imread('A7.png'), (300, 150), interpolation=cv2.INTER_CUBIC)

    A1_center = [np.shape(frame)[1]*1//8, np.shape(frame)[0]*6//8]
    A2_center = [np.shape(frame)[1]*2//8, np.shape(frame)[0]*6//8]
    A3_center = [np.shape(frame)[1]*3//8, np.shape(frame)[0]*6//8]
    A4_center = [np.shape(frame)[1]*4//8, np.shape(frame)[0]*6//8]
    A5_center = [np.shape(frame)[1]*5//8, np.shape(frame)[0]*6//8]
    A6_center = [np.shape(frame)[1]*6//8, np.shape(frame)[0]*6//8]
    A7_center = [np.shape(frame)[1]*7//8, np.shape(frame)[0]*6//8]

    A1_thickness = [300, 150]
    A1_top = [A1_center[0]-A1_thickness[0]//2, A1_center[1]-A1_thickness[1]//2]
    A1_btm = [A1_center[0]+A1_thickness[0]//2, A1_center[1]+A1_thickness[1]//2]

    A2_thickness = [300, 150]
    A2_top = [A2_center[0]-A2_thickness[0]//2, A2_center[1]-A2_thickness[1]//2]
    A2_btm = [A2_center[0]+A2_thickness[0]//2, A2_center[1]+A2_thickness[1]//2]

    A3_thickness = [300, 150]
    A3_top = [A3_center[0]-A3_thickness[0]//2, A3_center[1]-A3_thickness[1]//2]
    A3_btm = [A3_center[0]+A3_thickness[0]//2, A3_center[1]+A3_thickness[1]//2]

    A4_thickness = [300, 150]
    A4_top = [A4_center[0]-A4_thickness[0]//2, A4_center[1]-A4_thickness[1]//2]
    A4_btm = [A4_center[0]+A4_thickness[0]//2, A4_center[1]+A4_thickness[1]//2]

    A5_thickness = [300, 150]
    A5_top = [A5_center[0]-A5_thickness[0]//2, A5_center[1]-A5_thickness[1]//2]
    A5_btm = [A5_center[0]+A5_thickness[0]//2, A5_center[1]+A5_thickness[1]//2]

    A6_thickness = [300, 150]
    A6_top = [A6_center[0]-A6_thickness[0]//2, A6_center[1]-A6_thickness[1]//2]
    A6_btm = [A6_center[0]+A6_thickness[0]//2, A6_center[1]+A6_thickness[1]//2]

    A7_thickness = [300, 150]
    A7_top = [A7_center[0]-A7_thickness[0]//2, A7_center[1]-A7_thickness[1]//2]
    A7_btm = [A7_center[0]+A7_thickness[0]//2, A7_center[1]+A7_thickness[1]//2]

    time.sleep(1)

    while True:
        # Grab the current frame
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            break

        # Selecting ROI corresponding to A1
        A1_ROI = np.copy(frame[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]])
        mask = ROI_analysis(A1_ROI, 1)

        # Selecting ROI corresponding to A2
        A2_ROI = np.copy(frame[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]])
        mask = ROI_analysis(A2_ROI, 2)

        # Selecting ROI corresponding to A3
        A3_ROI = np.copy(frame[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]])
        mask = ROI_analysis(A3_ROI, 3)  # Play A3 audio

        # Selecting ROI corresponding to A4
        A4_ROI = np.copy(frame[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]])
        mask = ROI_analysis(A4_ROI, 4)  # Play A4 audio

        # Selecting ROI corresponding to A5
        A5_ROI = np.copy(frame[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]])
        mask = ROI_analysis(A5_ROI, 5)  # Play A5 audio

        # Selecting ROI corresponding to A6
        A6_ROI = np.copy(frame[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]])
        mask = ROI_analysis(A6_ROI, 6)  # Play A6 audio

        # Selecting ROI corresponding to A7
        A7_ROI = np.copy(frame[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]])
        mask = ROI_analysis(A7_ROI, 7)  # Play A7 audio

        # Writing text on the image
        cv2.putText(frame, 'Project : Airial Xylophone', (10, 30), 2, 1, (20, 20, 20), 2)

        # Display the ROI to view the blue colour being detected
        if Verbose:
            # Displaying the ROI in the Image
            frame[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]] = cv2.bitwise_and(
                frame[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]],
                frame[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]], mask=mask[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]])
            frame[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]] = cv2.bitwise_and(
                frame[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]],
                frame[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]], mask=mask[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]])
            frame[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]] = cv2.bitwise_and(
                frame[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]],
                frame[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]], mask=mask[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]])
            frame[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]] = cv2.bitwise_and(
                frame[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]],
                frame[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]], mask=mask[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]])
            frame[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]] = cv2.bitwise_and(
                frame[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]],
                frame[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]], mask=mask[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]])
            frame[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]] = cv2.bitwise_and(
                frame[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]],
                frame[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]], mask=mask[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]])
            frame[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]] = cv2.bitwise_and(
                frame[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]],
                frame[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]], mask=mask[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]])

        else:
            # Augmenting the image of the instruments on the frame
            frame[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]] = cv2.addWeighted(A1, 1,
                                                                            frame[A1_top[1]:A1_btm[1], A1_top[0]:A1_btm[0]], 1, 0)
            frame[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]] = cv2.addWeighted(A2, 1,
                                                                            frame[A2_top[1]:A2_btm[1], A2_top[0]:A2_btm[0]], 1, 0)
            frame[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]] = cv2.addWeighted(A3, 1,
                                                                            frame[A3_top[1]:A3_btm[1], A3_top[0]:A3_btm[0]], 1, 0)
            frame[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]] = cv2.addWeighted(A4, 1,
                                                                            frame[A4_top[1]:A4_btm[1], A4_top[0]:A4_btm[0]], 1, 0)
            frame[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]] = cv2.addWeighted(A5, 1,
                                                                            frame[A5_top[1]:A5_btm[1], A5_top[0]:A5_btm[0]], 1, 0)
            frame[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]] = cv2.addWeighted(A6, 1,
                                                                            frame[A6_top[1]:A6_btm[1], A6_top[0]:A6_btm[0]], 1, 0)
            frame[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]] = cv2.addWeighted(A7, 1,
                                                                            frame[A7_top[1]:A7_btm[1], A7_top[0]:A7_btm[0]], 1, 0)
        cv2.imshow('Output', frame)
        key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # Cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()


    pickle.dump(frame, open("model.pkl", "wb"))