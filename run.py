#!/usr/bin/python

from Scrapper.reddit import RedditScrapper
from Video.Voice import CommentToVoice
from Log.log import *

def main():
    startLogger()

    logInfo("scrapper started")
    
    subreddit = "https://reddit.com/r/AskReddit/"
    redditScrapper = RedditScrapper(subreddit)
    redditScrapper.getPostListing(0)
        
    for post in redditScrapper.post_listing:
        print("\n", post.title)

        post.getCommentsListing(50)        
        for n, comment in enumerate(post.comments[0]):
            logInfo(f"{n} : {comment}")

        
        logInfo("generating voice...")
        voice = CommentToVoice()
        voice.generateAllVoices(post)
    

if __name__=="__main__":
    main()

