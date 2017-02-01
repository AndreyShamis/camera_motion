#!/usr/bin/env python

from gpiozero import MotionSensor
from multiprocessing import Process, Queue

import cv as cv2
import pygame
import pygame.camera
import telepot
import time
import glob
import os
import argparse
import datetime
import imutils
import threading

from datetime import datetime
from pprint import pprint

# http_proxy = "http://proxy...com:"
# https_proxy = "https://proxy...com:"
# socks_proxy = "socks://proxy...com:"
#
# proxyDict = {
#     "http": http_proxy,
#     "https": https_proxy,
#     "socks": socks_proxy
# }

# werd_chat_id = -1001117363466
# milena =
# andrey =290710006
chat_id_value = '290710006'
token = '248037479:AAELGWsUIUkrhTTRpkotL1j2P--26Sfkov4'

#lock = threading.Lock()
semaphore = threading.BoundedSemaphore(1)
lock_w = False

def telegram_photo_file(file_path,remove=False):
    bot = telepot.Bot(token)
    file_name = os.getcwd() + "/" + file_path

    if os.path.isfile(file_name):
        bot.sendPhoto(chat_id=chat_id_value, photo=open(file_name, 'rb'))
        #pprint(file_name)
        if remove == True:
            os.remove(file_name)


def telegram_message_file(file_path):
    bot = telepot.Bot(token)
    bot.sendPhoto(chat_id=chat_id_value, photo=open(file_path, 'rb'))


def telegram_send_all_images(folder,remove=False):
    #lock.acquire()
    global semaphore
    global lock_w
    semaphore.acquire()
    while lock_w == True:
       time.sleep(0.01)
    lock_w = True
    try:
        l = glob.iglob(folder+'/*.jpg')
        for t in l:
            telegram_photo_file(t,True)
            #file_name = os.getcwd() + "/" + t
            #pprint(file_name)
            #if remove == True:
            #    os.remove(file_name)
    finally:
        #lock.release()
        lock_w = False
        semaphore.release()


def telegram_send(input_file):
    # werd_chat_id = -1001117363466
    # milena =
    # andrey =290710006
    l = glob.iglob('pics/*.jpg')
    # file = max(glob.iglob('pics/*.jpg'), key=os.path.getctime)

    bot = telepot.Bot(token)
    bot.sendMessage(chat_id=chat_id_value, text=input_file)
    for t in l:
        bot.sendPhoto(chat_id=chat_id_value, photo=open(t, 'rb'))
        file_name = os.getcwd() + "/" + t
        pprint(file_name)
        os.remove(file_name)


def main_func():
    file = '/home/pi/alarms/'
    counter = 0
    threshhold = 2
    # pir = MotionSensor(4)
    # Telegram_send('/home/werd/milena')
    # exit()
    try:
        #camera = cv2.VideoCapture('/dev/video0')
        pygame.camera.init()
        #pygame.camera.list_cameras()
        # cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam = pygame.camera.Camera("/dev/video0", (1280, 720))
        patt = '%m%d-%H%M%S.%f'
        cam.start()
        time.sleep(0.1)
        while counter <= threshhold:
            # time.sleep(0.1)
            if 1 == 1:  # pir.motion_detected:
                #cam.start()
                time.sleep(0.1)  # You might need something higher in the beginning
                time_now = datetime.utcnow().strftime(patt)
                #print("Motion detected at " + str(time_now))
                #if not camera.isOpened():
                #    camera.open('/dev/video0')
                #    print ("Camera not loaded")
                #    result, image = camera.read()
                #    # print result
                #else:
                #    result, image = camera.read()

                img = cam.get_image()

                pygame.image.save(img, "pics/" + time_now + ".jpg")

                #cv2.imwrite(file + str(time.strftime("%Y%m%d-%H%M%S")) + '.jpg', image)
                counter += 1
                telegram_send_all_images("pics/", True)
        cam.stop()
        if counter >= threshhold:
            telegram_send_all_images("pics/",True)
    except Exception as e:
        print('Something is wrong.', e)
        #camera.release()


def main_dva():
    import cv2
    queue = Queue()
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=20, help="minimum area size")
    ap.add_argument("-s", "--send-pics", default='No', help="Send pics")
    args = vars(ap.parse_args())
    pprint(args)
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        camera = cv2.VideoCapture(-1)
        print (camera.isOpened())
        time.sleep(0.25)
        print ("----------")
        print ("Video 0")
    # otherwise, we are reading from a video file
    else:
        camera = cv2.VideoCapture(args["video"])

    IMAGE_SIZE=400
    # initialize the first frame in the video stream
    firstFrame = None
    #(grabbed, firstFrame) = camera.read()
    #firstFrame = imutils.resize(firstFrame, width=IMAGE_SIZE)
    #pprint(camera)
    # loop over the frames of the video
    count = 0
    trashhold=0
    exec_path = os.getcwd()
    print ("Exec path " + exec_path)
    while True:
        count=count+1
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, rframe) = camera.read()
        time.sleep(0.01)
        (grabbed2, sec_frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            print ("Camera not grabed")
            pprint(frame)
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(rframe, width=IMAGE_SIZE)
        sec_frame = imutils.resize(sec_frame , width=IMAGE_SIZE)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        gray2 = cv2.cvtColor(sec_frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        #print "Here2"
        # if the first frame is None, initialize it
        if firstFrame is None:
            print ("Set first frame to be gray")
            firstFrame = gray
            continue
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(gray2, gray)
        #newFrame = cv2.absdiff(frame,frame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)


        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            text = "Occupied"

        time_str = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")

        # draw the text and timestamp on the frame
        cv2.putText(frame, "STAT: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, time_str, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        if text == "Occupied":
            trashhold=trashhold+1

            try:
                f_image_path = os.path.join(exec_path, "pic_detect", '%d.jpg') % count
                s_image_path = os.path.join(exec_path, "pic_detect", '%d_delta.jpg') % count

                if trashhold == 2:
                    cv2.imwrite(f_image_path, sec_frame)
                if trashhold >= 4 and trashhold%2==0:

                    cv2.imwrite(f_image_path, sec_frame)
                    #cv2.imwrite(s_image_path, frameDelta)
                    if args['send_pics'] == 'Yes':
                        #t = threading.Thread(target=telegram_send_all_images, args=("pic_detect", True))
                        #t.start()

                        p = Process(target=telegram_send_all_images, args=("pic_detect", True,))
                        print("Send image [Image path=" + f_image_path + "]")
                        p.start()
                        #queue.p
                        #telegram_send_all_images("pic_detect", True)
            except:
                pass
        else:
            trashhold=0

        if trashhold>=8:
            trashhold = 0

        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        #cv2.imshow("new Frame", newFrame)
        key = cv2.waitKey(1) & 0xFF
        if trashhold > 0:
            print(trashhold)
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break
        if text == "Occupied":
            try:
                pass
                #firstFrame = rframe
            except:
                pass
            #print ("Here")
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #main_func()
    main_dva()