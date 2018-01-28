import sys
import time
import os
import telepot
from telepot.loop import MessageLoop
import pprint
from PIL import Image
import requests
from recogniseFace import *
import cv2
from faceSwap_stable import *

class State:
    #isAnImageSet
    #settingMode
    def __init__(self, bool1, bool2):
        self.isAnImageSet = bool1
        self.settingMode = bool2

#state = State(False, False)

idList = {}

def handle(msg):
        print("a")
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        print("b")
        if content_type == 'text':
            if msg['text'] == "/start":
                idList[chat_id] = State(False, False)
                print("c")
            elif msg['text'] == "/set":
                idList[chat_id].settingMode = True
                SwapBot.sendMessage(chat_id, "Please wait at least 10 seconds after sending the first image")
                print("d")
            elif msg['text'] == "/stop":
                idList[chat_id].isAnImageSet = False
                print("e")
                #Wipe the history.

            elif msg['text'] == "/help":
                SwapBot.sendMessage(chat_id, "1. Use set to set a mask that will be used on all subsequent images \n2. Send any photo you want after that to have the faces replaced by the masked. \n3. Profit???")
            else:
                SwapBot.sendMessage(chat_id, "I'd love to talk, but I'm a busy bot")

        elif content_type == 'photo' and idList[chat_id].settingMode == True:
            print("f")
            idList[chat_id].settingMode = False
            dloadID = (msg['photo'][2]['file_id'])
            fileObject = SwapBot.getFile(dloadID)
            filePath = fileObject['file_path']
            req = requests.get("https://api.telegram.org/file/bot<INSERT-TOKEN-HERE>" + filePath)
            if req.status_code == 200:
                with open("./mask" + str(chat_id) + ".jpg", 'wb') as f:
                    f.write(req.content)
                idList[chat_id].isAnImageSet = True


        elif content_type == 'photo' and idList[chat_id].isAnImageSet == True:
            print("g")
            dloadID = (msg['photo'][2]['file_id'])
            fileObject = SwapBot.getFile(dloadID)
            filePath = fileObject['file_path']
            req = requests.get("https://api.telegram.org/file/bot<INSERT-TOKEN-HERE>" + filePath)
            if req.status_code == 200:
                with open("./blah" + str(chat_id) + ".jpg", 'wb') as f:
                    f.write(req.content)
                faceSwap("mask" + str(chat_id) + ".jpg", "blah" + str(chat_id) + ".jpg")
                # faceSwap("barack-obama.jpg", "yara.jpg")
                # SwapBot.sendPhoto(chat_id=chat_id, photo=open('./' + str(chat_id) + 'result.jpg'))
                SwapBot.sendPhoto(chat_id=chat_id, photo=open('./result.jpg', 'rb'))
                # os.remove('./' + 'result.jpg')
                os.remove("./blah" + str(chat_id) + ".jpg")


        elif content_type == 'photo' and not idList[chat_id].isAnImageSet == True:
            SwapBot.sendMessage(chat_id, "Great photo, but there is nothing I can swap onto it. Use the /set command first")

TOKEN = "<INSERT-TOKEN-HERE>"
SwapBot = telepot.Bot(TOKEN)
MessageLoop(SwapBot, handle).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
