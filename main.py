#!/usr/bin/env python

#from gpiozero import MotionSensor
# import cv2
import telepot
import time

http_proxy = "http://proxy.iil.intel.com:911"
https_proxy = "https://proxy.iil.intel.com:911"
socks_proxy = "socks://proxy.iil.intel.com:1080"

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "socks"   : socks_proxy
            }

def Telegram_send(input_file):
    #import glob
    #import os
    chat_id_value = 'AAAAAEKZnQqBhiFSUbjgMg'
    #file=max(glob.iglob(input_file+'*.jpg'),key=os.path.getctime)

    bot = telepot.Bot('248037479:AAELGWsUIUkrhTTRpkotL1j2P--26Sfkov4')
    bot.sendMessage(chat_id=chat_id_value, text='Motion detected!')
    #bot.sendPhoto(chat_id=chat_id_value, photo=open(file,'rb'))

def main():
    file = '/home/pi/alarms/'
    counter = 0
    threshhold = 10
    #pir = MotionSensor(4)
    Telegram_send('as')
    # try:
    #     camera=cv2.VideoCapture(0)
    #     while counter<=threshhold:
    #         if pir.motion_detected:
    #             print("Motion detected at "+str(time.strftime("%Y%m%d-%H%M%S")))
    #             if not camera.isOpened():
    #                 camera.open(0)
    #                 result,image=camera.read()
    #             else:
    #                 result,image=camera.read()
    #             cv2.imwrite(file+str(time.strftime("%Y%m%d-%H%M%S"))+'.jpg',image)
    #             counter+=1
    #     if counter >=threshhold: Telegram_send(file)
    # except Exception as e:
    #     print('Something is wrong.',e)
    #     camera.release()

if __name__=="__main__":
   main()