#!/usr/bin/python

from Reddit.redditScrapper import RedditScrapper
from Video.video import Video
from Log.log import *


if __name__=="__main__":
    startLogger()

    scrapper = RedditScrapper("askreddit", "https://www.reddit.com/r/AskReddit/")
    video = Video()

    for post in scrapper.getPostListing(post_limit=5):
        post.getPostContents(comment_limit=80)
        video.generateVideo(post)
        
        
        

        
        

       
    
    
