from gtts import gTTS
from io import BytesIO

from multiprocessing import Process, Queue
from queue import Empty

import sys
sys.path.append("../Log")
from Log.log import *

#from moviepy.editor import *
import moviepy.editor as Movie

    
class Video:
    def __init__(self, background="./clip.mp4"):
        self.background = background
        
    def generateVideo(self, post, level=0):
        logInfo(f"generating video {post.title}")
        
        background_clip = Movie.VideoFileClip(self.background).subclip(0, 120).volumex(0.5)
        title_clip = self.generateTitleClip(post)
        comment_clip = Movie.concatenate_videoclips(
            [self.generateCommentClip(c) for c in post.comments[level]]
        )

        content_clip = Movie.concatenate_videoclips([title_clip, comment_clip]).set_pos('center')
        video = Movie.CompositeVideoClip([background_clip, content_clip])
        video.write_videofile(f"/tmp/{post.title}.mp4")
        logInfo(f"video done {post.title}")

    def generateCommentClip(self, comment):
        text_clip = self.generateTextClip(comment)
        voice_clip = self.generateVoiceClip(comment)

        retval = []
        for text, voice in zip(text_clip, voice_clip):
            t = text.set_pos("center").set_duration(voice.duration)
            t = t.set_audio(voice)
            retval.append(t)

        
        return Movie.concatenate_videoclips(retval)
        #return Movie.concatenate(retval, method="compose")

    def generateTitleClip(self, post):
        text_clip = Movie.TextClip(
            post.title,
            font="Cantarell-Extra-Bold",
            fontsize=40,
            stroke_width=1.5,
            method="caption",
            align="center",
            color="white"
        )

        tts = gTTS(post.title, lang="en")
        tts.save(f"/tmp/title-{post.title}.mp3")
        voice_clip = Movie.AudioFileClip(f"/tmp/title-{post.title}.mp3")

        t = text_clip.set_pos("center").set_duration(voice_clip.duration)
        t = t.set_audio(voice_clip)
        return t
            
    def generateTextClip(self, comment):
        retval = []
        for paragraph in comment.text:
            logInfo(f"generating textclip:\n{paragraph}")
            
            text_clip = Movie.TextClip(
                paragraph,
                font="Cantarell-Extra-Bold",
                fontsize=40,
                stroke_width=1.5,
                method="caption",
                align="center",
                color="white"
            )
            retval.append(text_clip)
            
        return retval

    def generateVoiceClip(self, comment):
        retval = []
        for i, paragraph in enumerate(comment.text):
            logInfo(f"generating audioclip:\n{paragraph}")

            tts = gTTS(paragraph, lang="en")
            tts.save(f"/tmp/voiceclip-{i}.mp3")
            voice_clip = Movie.AudioFileClip(f"/tmp/voiceclip-{i}.mp3")
            retval.append(voice_clip)
            
        return retval
