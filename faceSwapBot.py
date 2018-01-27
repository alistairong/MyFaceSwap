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

state = State(False, False)

def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            if msg['text'] == "/set":
                state.settingMode = True

            elif msg['text'] == "/stop":
                state.isAnImageSet = False
                
                #Wipe the history.
            
            elif msg['text'] == "/help":
                SwapBot.sendMessage(chat_id, "1. Use set to set a mask that will be used on all subsequent images \n2. Send any photo you want after that to have the faces replaced by the masked. \n3. Profit???")
            else:
                SwapBot.sendMessage(chat_id, "I'd love to talk, but I'm a busy bot")
        
        elif content_type == 'photo' and state.settingMode == True:
            state.settingMode = False
            dloadID = (msg['photo'][0]['file_id'])
            fileObject = SwapBot.getFile(dloadID)
            filePath = fileObject['file_path']
            req = requests.get("https://api.telegram.org/file/bot<insert-bot-token>/" + filePath)
            if req.status_code == 200:
                with open("./mask.jpg", 'wb') as f:
                    f.write(req.content)
                state.isAnImageSet = True

            
        
        elif content_type == 'photo' and state.isAnImageSet == True:
            print("whatever")
            #Business as usual

        elif content_type == 'photo' and not state.isAnImageSet == True:
            SwapBot.sendMessage(chat_id, "Great photo, but there is nothing I can swap onto it. Use the /set command first")

TOKEN = <insert-bot-token>
SwapBot = telepot.Bot(TOKEN)
MessageLoop(SwapBot, handle).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
