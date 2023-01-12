from gtts import gTTS
from io import BytesIO

from multiprocessing import Process, Queue
from queue import Empty

import sys, os
sys.path.append("../Log")
from Log import log


class CommentToSpeech:
    def __init__(self, post, level=1, process_cnt=1):
        print(log.logger)
        
        self.process_cnt = process_cnt

        self.queues = [
            Queue() for i in range(0, process_cnt)
        ]
        self.populateQueue(post.comments[level], process_cnt)

        self.retQueue = Queue()
        self.processes = [
            Process(
                target=self.generateVoice,
                args=(self.queues[i], log.logger)
            ) for i in range(0, process_cnt)
        ]
        
        
    def populateQueue(self, comments, process_cnt):
        current = 0
        block_len = int(len(comments) / process_cnt)
        for i in range(0, process_cnt):
            nxt = block_len*(i+1)
            
            comments_block = comments[current:nxt]
            map(self.queues[i].put, comments_block)                
            
            current = next
            
            
    def generateAllVoices(self):
        for p in self.processes:
            p.start()
            
        for p in self.processes:
            p.join()

            
    @staticmethod
    def generateVoice(queue, passed_logger):
        global logger
        log.logger = passed_logger
        log.logInfo("worker started")
        
        while True:
            try:
                comment = queue.get()
                
                audio = []
                for p in comment.text:
                    log.logInfo(f"generating voice for {p}")
                    
                    stream = BytesIO()
                    tts = gTTS(p, lang="en")
                    tts.write_to_fp(stream)
                    audio.append(stream)
                    
                    #tts.save(f"/tmp/{p}.mp3")

                    log.logInfo(f"generation complete")
                comment.audio = audio
                
            except Empty:
                log.logInfo("queue empty, quitting")
                break

            except Exception as e:
                log.logInfo(f"error: {e}")
                break
            
        log.logInfo("worker finished")
        return
        
        

    

# if __name__=="__main__":
#     subreddit = "https://reddit.com/r/AskReddit/"
#     redditScrapper = RedditScrapper(subreddit, post_limit=0)
#     redditScrapper.getPostListing()

        
#     for post in redditScrapper.post_listing:
#         print("\n", post.title)
#         post.getCommentsListing(10)

#         voice = CommentToSpeech(post)
        
#         for n, comment in enumerate(post.comments[0]):
#             print(n, comment)

#         voice.generateAllSpeeches()
            
    


