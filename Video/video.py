from gtts import gTTS
from io import BytesIO

from string import ascii_letters, printable
from re import compile, UNICODE

from os import listdir
from Log.log import *
from random import choice

from PIL import Image
from io import BytesIO
import base64

#from moviepy.editor import *
#import moviepy.editor as Movie

from moviepy.editor import (
    ImageClip,
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    concatenate_audioclips

)

    
class Video:
    dirtyText = "".join(
        [c for c in printable if c not in ascii_letters + ".?!~',& " + "0123456789"]
    )
    replacementText = {
        " tf ": " the fuck ",
        "AMA": "Ask me anything",
        "ELI5": "Explain like I'm 5",
        "TL;DR": "Too Long Didn't Read",
        "NSFW": "Not safe for work",
        "!!!": "!",
        "???": "?",
        "\n": "",
        "rAskReddit": "subreddit AskReddit"
    }
    emojiText = compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=UNICODE)

    
    def __init__(self):
        self.open_instances = []
        

    
    def generateVideo(self, post, outputDir="Clips/processed", level=0):
        logInfo(f"generating video {post.title}")
        
        backgroundClip = self.getBackgroundClip()
        titleClip = self.getClip([post.title], post.postImage)
        commentClip = concatenate_videoclips(
            [self.getClip(c.text, c.image) for c in post.comments[level]]
        )
        
        contentClip = concatenate_videoclips([titleClip, commentClip]).set_pos('center')
        video = CompositeVideoClip([backgroundClip, contentClip])
        video = video.set_duration(contentClip.duration)
    
        videoTitle = self.cleanText(post.title)
        video.write_videofile(f"{outputDir}/{videoTitle}.mp4", audio_bufsize=2048)
        logInfo(f"video done {videoTitle}.mp4")
        self.closeOpenInstances()
        

    def getBackgroundClip(self, backgroundDir="Clips/background"):
        background = backgroundDir + "/" + choice(listdir(backgroundDir))
        retval = VideoFileClip(background).volumex(0.5)
        self.open_instances.append(retval)
        return retval

    
    def getClip(self, text, image):
        logDebug(f"generating clip for:\n {text}")

        image = Image.open(BytesIO(base64.b64decode(image)))
        image.save("/tmp/imageclip.png")
        clip = ImageClip("/tmp/imageclip.png")

        voice = self.getVoiceClip(text)
        clip = clip.set_duration(voice.duration)
        clip = clip.set_audio(voice)

        return clip

        
    def getVoiceClip(self, text):
        voiceClips = []
        for n, paragraph in enumerate(text):
            tts = gTTS(
                paragraph,
                pre_processor_funcs=[self.cleanText],
                lang="en"
            )

            tts.save("/tmp/voiceclip.mp3")
            clip = AudioFileClip("/tmp/voiceclip.mp3", fps=31100, buffersize=10000000)
            self.open_instances.append(clip)
            voiceClips.append(clip)
        
        return concatenate_audioclips(voiceClips)
    
    
    def cleanText(self, text):    
        for t in self.dirtyText: 
            text = text.replace(t, "")
            
        for word, replacement in self.replacementText.items():
            text = text.replace(word, replacement)
            
        text = self.emojiText.sub(r'', text)
        
        return text    
    
    def closeOpenInstances(self):
        for instance in self.open_instances:
            instance.close()
        self.open_instances = []







