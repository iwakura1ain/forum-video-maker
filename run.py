#!/usr/bin/python

from Reddit.redditScrapper import RedditScrapper
from Video.video import Video
from Log.log import *


if __name__=="__main__":
    startLogger()

    scrapper = RedditScrapper("askreddit", "https://www.reddit.com/r/AskReddit/")
    video = Video()

    if not scrapper.loginReddit():
        quit()
        
    # scrapper.getPostListing(post_limit=1)
    # for i, post in enumerate(scrapper.post_listing):
    #     post.getPostContents(comment_limit=50)
    #     video.generateVideo(post)


    for post in scrapper.getPostListing(post_limit=5):
        post.getPostContents(comment_limit=50)
        video.generateVideo(post)
        
        
        

        
        

       
    
    










