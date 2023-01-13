from gtts import gTTS
from io import BytesIO

from multiprocessing import Process, Queue
from queue import Empty

import sys
sys.path.append("../Log")
from Log.log import *


class CommentToVoice:
    def __init__(self, level=0):
        self.post = None
        self.level = level


    def generateAllVoices(self, post):
        for comment in post.comments[self.level]:
            self.generateVoice(comment)
            
            
    def generateVoice(self, comment):
        for p in comment.text:
            logInfo(f"generating text:\n{p}")
            stream = BytesIO()
            tts = gTTS(p, lang="en")
            tts.write_to_fp(stream)
            tts.save(f"/tmp/{p}.mp3")
            comment.audio.append(stream)
            logInfo("generation complete")
        
            
    


