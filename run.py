#!/usr/bin/python

from Scrapper.reddit import RedditScrapper
from Video.video import Video
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

        
        logInfo("generating video...")
        video = Video()
        video.generateVideo(post)
        

if __name__=="__main__":
    main()

