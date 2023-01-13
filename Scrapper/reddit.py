from .driver import getWebDriver, scrollScreen

from urllib.parse import urlsplit

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidArgumentException, StaleElementReferenceException, NoSuchElementException
)

import sys
sys.path.append("../Log")
from Log.log import *


class CommentData:
    level_xpath = ".//../../../.."
    upvote_xpath = ".//../../div[3]/div[1]/div[1]"
    comment_level = ["padding-left: 16px;", "padding-left: 37px;"]  # level1 , level2 
    
    def __init__(self, comment):
        self.text = [p.text for p in comment.find_elements(By.XPATH, ".//*")]
        self.level = self.getCommentLevel(comment)
        self.upvote = self.getUpvote(comment)

        self.audio = []
        
        
    def __str__(self):
        body = "\n".join(self.text)
        return f"upvote={self.upvote}  level={self.level} \n {body}"
    

    def getCommentLevel(self, comment):
        level = comment.find_element(By.XPATH, self.level_xpath)
        return self.comment_level.index(level.get_attribute("style"))

    
    def getUpvote(self, comment):
        upvote = comment.find_element(By.XPATH, self.upvote_xpath)
        return upvote.text
        
       
class PostData:
    title_xpath = ".//div[1]/div[1]/div[3]/div[2]/div[1]/a[1]/div[1]/h3[1]"
    link_xpath = ".//div[1]/div[1]/div[3]/div[2]/div[1]/a[1]"
    comment_xpath = ".//div[contains(@class, 'RichTextJSON-root')]"
    
    def __init__(self, post, driver=None):
        self.DRIVER = getWebDriver() if driver is None else driver
        
        self.title = post.find_element(By.XPATH, self.title_xpath).text
        self.link = post.find_element(By.XPATH, self.link_xpath).get_attribute("href")

        self.is_nsfw = False
        self.is_ad = False

        self.comment_limit = 0
        self.comments = {0: [], 1: []}
        
        
    def __str__(self):
        return self.title
    
    
    def getCommentsListing(self, comment_limit=10):
        self.comment_limit = comment_limit
        
        self.DRIVER.get(self.link)
        content = self.DRIVER.find_element(By.ID, "AppRouter-main-content")
        all_comments = self.getAllComments(content)

        self.getCommentData(all_comments)
        
        
    def getAllComments(self, content):
        all_comments = dict()
        while len(all_comments) < self.comment_limit:
            comments = content.find_elements(By.XPATH, self.comment_xpath)
            all_comments.update({c: None for c in comments})
            
            # all_comments.update(
            #     dict(content.find_elements(By.XPATH, self.comment_xpath))
            # )
            scrollScreen(self.DRIVER)
            
        return all_comments.keys()  #ignore first post for comment input
    

    def getCommentData(self, all_comments):
        for comment in all_comments:
            try:
                commentData = CommentData(comment)
                self.comments[commentData.level].append(commentData)
            except ValueError:
                pass

            
class RedditScrapper:
    def __init__(self, subreddit, driver=None):
        self.subreddit = subreddit
        self.DRIVER = getWebDriver() if driver is None else driver
    
        self.post_limit = 2
        self.post_count = 2
        self.post_listing = []
        
        
    def getPostListing(self, post_limit=0):
        self.post_limit += post_limit
        
        self.DRIVER.get(self.subreddit)
        content = self.DRIVER.find_element(By.ID, "AppRouter-main-content")
        all_posts = self.getAllPosts(content)
        
        for post in self.getPost(all_posts):
            try:
                postData = PostData(post)
                self.post_listing.append(postData)
                logInfo(f"scrapped: {postData}")
                
            except NoSuchElementException:
                logInfo(f"no post for {post.get_attribute('class')}")
            
            
    def getAllPosts(self, content):  # parent div of data-scroller-first
        xpath = ".//div[4]/div[1]/div[4]"
        return content.find_element(By.XPATH, xpath)
    

    def getPost(self, all_posts):  # iterate from 1
        while self.post_count <= self.post_limit:
            post = all_posts.find_element(By.XPATH, f".//div[{self.post_count}]")               
            yield post
                
            self.post_count += 1
            
            
    def isAdvertisement(self, post):
        xpath = ".//div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span[2]/span[1]"
        try:
            is_advertisement = post.find_element(By.XPATH, xpath)
            if is_advertisement.text == "promoted":
                return True
        
            return False

        except NoSuchElementException:
            return False
        
        
                 
if __name__=="__main__":
    subreddit = "https://reddit.com/r/AskReddit/"
    driver = getWebDriver()

    redditScrapper = RedditScrapper(subreddit, post_limit=0, driver=driver)
    redditScrapper.getPostListing()
    
    for post in redditScrapper.post_listing:
        logInfo("\n", post.title)
        post.getCommentsListing()

        for n, comment in enumerate(post.comments[0]):
            logInfo(n, comment)
       
    
    









