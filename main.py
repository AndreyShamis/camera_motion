#!/usr/bin/env python

from gpiozero import MotionSensor
import cv2
import pygame
import pygame.camera
import telepot
import time
import glob
import os

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


def telegram_photo_file(file_path):
    bot = telepot.Bot(token)
    bot.sendPhoto(chat_id=chat_id_value, photo=open(file_path, 'rb'))


def telegram_message_file(file_path):
    bot = telepot.Bot(token)
    bot.sendPhoto(chat_id=chat_id_value, photo=open(file_path, 'rb'))


def telegram_send_all_images(folder,remove=False):
    l = glob.iglob(folder+'/*.jpg')
    for t in l:
        telegram_photo_file(t)
        file_name = os.getcwd() + "/" + t
        pprint(file_name)
        if remove == True:
            os.remove(file_name)


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


def main():
    file = '/home/pi/alarms/'
    counter = 0
    threshhold = 5
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
        if counter >= threshhold: telegram_send_all_images("pics/",True)
    except Exception as e:
        print('Something is wrong.', e)
        #camera.release()


if __name__ == "__main__":
    main()
