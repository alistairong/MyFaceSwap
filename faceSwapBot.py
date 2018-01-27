import sys
import time
import telepot
from telepot.loop import MessageLoop

def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        
        if content_type == 'text':
            SwapBot.sendMessage(chat_id, "I don't care, send me photos to eat")
        elif content_type == 'photo':
            SwapBot.sendMessage(chat_id, "Yup that's a photo")

TOKEN = '464773380:AAEYFPFNliELLz3DNJeHEAxa29cEas26ZnM'
SwapBot = telepot.Bot(TOKEN)
MessageLoop(SwapBot, handle).run_as_thread()
print ('Listening ...')

                            # Keep the program running.
while 1:
    time.sleep(10)
