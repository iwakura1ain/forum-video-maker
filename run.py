#!/usr/bin/python

from Scrapper.reddit import RedditScrapper
from Video.Voice import CommentToSpeech
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
            print(n, comment)
            logInfo(f"{n} : {comment}")

        
        print("generating voice...")
        voice = CommentToSpeech(post)
        voice.generateAllVoices()
    

if __name__=="__main__":
    main()

