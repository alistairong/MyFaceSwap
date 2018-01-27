import sys
import time
import telepot
from telepot.loop import MessageLoop
import pprint
from PIL import Image
import requests 

class State:
    #isAnImageSet
    #settingMode
    def __init__(self, bool1, bool2):
        self.isAnImageSet = bool1
        self.settingMode = bool2

#state = State(False, False)

idList = {}

def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            if msg['text'] == "/start":
                idList[chat_id] = State(False, False)

            elif msg['text'] == "/set":
                idList[chat_id].settingMode = True

            elif msg['text'] == "/stop":
                idList[chat_id].isAnImageSet = False
                
                #Wipe the history.
            
            elif msg['text'] == "/help":
                SwapBot.sendMessage(chat_id, "1. Use set to set a mask that will be used on all subsequent images \n2. Send any photo you want after that to have the faces replaced by the masked. \n3. Profit???")
            else:
                SwapBot.sendMessage(chat_id, "I'd love to talk, but I'm a busy bot")
        
        elif content_type == 'photo' and idList[chat_id].settingMode == True:
            idList[chat_id].settingMode = False
            dloadID = (msg['photo'][0]['file_id'])
            fileObject = SwapBot.getFile(dloadID)
            filePath = fileObject['file_path']
            req = requests.get("https://api.telegram.org/file/bot<insert-bot_key>/" + filePath)
            if req.status_code == 200:
                with open("./mask" + str(chat_id) + ".jpg", 'wb') as f:
                    f.write(req.content)
                idList[chat_id].isAnImageSet = True

            
        
        elif content_type == 'photo' and idList[chat_id].isAnImageSet == True:
            print("whatever")
            #Business as usual

        elif content_type == 'photo' and not idList[chat_id].isAnImageSet == True:
            SwapBot.sendMessage(chat_id, "Great photo, but there is nothing I can swap onto it. Use the /set command first")

TOKEN = <insert-bot-key>
SwapBot = telepot.Bot(TOKEN)
MessageLoop(SwapBot, handle).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
