from driver import getWebDriver, scrollScreen

from urllib.parse import urlsplit

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidArgumentException, StaleElementReferenceException, NoSuchElementException
)

from PIL import Image
from io import BytesIO

# import sys
# sys.path.append("../Log")
# from Log.log import *


class CommentData:
    comment_level = ["padding-left: 16px;", "padding-left: 37px;"]  # level1 , level2
    xpath = {
        "level": ".//../../../..",
        "upvote": ".//../../div[3]/div[1]/div[1]",   
    }
    
    def __init__(self, comment):
        self.text = [p.text for p in comment.find_elements(By.XPATH, ".//*")]
        self.level = self.getCommentLevel(comment)
        self.upvote = self.getUpvote(comment)

        self.audio = []
        
        
    def __str__(self):
        body = "\n".join(self.text)
        return f"upvote={self.upvote}  level={self.level} \n {body}"
    
    
    def getCommentLevel(self, comment):
        level = comment.find_element(By.XPATH, self.xpath["level"])
        return self.comment_level.index(level.get_attribute("style"))

    
    def getUpvote(self, comment):
        upvote = comment.find_element(By.XPATH, self.xpath["upvote"])
        return upvote.text
        
       
class PostData:
    xpath = {
        "base": ".//div[@data-adclicklocation='title']",
        "title": ".//div[1]/a[1]/div[1]/h3",
        "link": ".//div[1]/a[1]",
        "is_nsfw": ".//div[2]/div[2]/span",
        "is_ad": ".//div[3]/div[1]/div[1]/div[1]/div[1]/span[2]/span[1]"
    }

    
    def __init__(self, post, img, driver=None):
        self.DRIVER = getWebDriver() if driver is None else driver

        self.img = img
        self.title, self.link, self.is_ad, self.is_nsfw = self.getPostData(post)
        
        self.comments = {0: [], 1: []}
        
        
    def __str__(self):
        return self.title

    
    def getPostData(self, post):
        retval = [None, None, None, None] #title, link, is_ad, is_nsfw

        base = post.find_element(By.XPATH, self.xpath["base"])
        retval[0] = base.find_element(By.XPATH, self.xpath["title"]).text
        retval[1] = base.find_element(By.XPATH, self.xpath["link"]).get_attribute("href")
        
        try:
            retval[2] = (post.find_element(By.XPATH, self.xpath["is_ad"]).text == "promoted")
        except:
            retval[2] = False

        try:
            retval[3] = (base.find_element(By.XPATH, self.xpath["is_nsfw"]).text == "nsfw")
        except:
            retval[3] = False
            
        return retval

        
    def getCommentsListing(self, count=10):
        #self.comment_limit = comment_limit
        
        self.DRIVER.get(self.link)
        content = self.DRIVER.find_element(By.ID, "AppRouter-main-content")
        all_comments = self.getAllComments(content, count)

        self.getCommentData(all_comments)
        
        
    def getAllComments(self, content, count):
        all_comments = dict()
        while len(all_comments) < count:
            comments = content.find_elements(By.XPATH, self.comment_xpath)
            all_comments.update({c: None for c in comments})
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
    
        #self.post_limit = 2
        #self.post_count = 2
        self.post_listing = []
        
        
    def getPostListing(self, post_limit=None):
        
        
        self.DRIVER.get(self.subreddit)
        content = self.DRIVER.find_element(By.ID, "AppRouter-main-content")
        posts_div = self.getPostsDiv(content)

        for post, img in self.getPosts(posts_div, post_limit):
            postData = PostData(post, img)
            self.post_listing.append(postData)
            print(f"post: {postData.title}\n link: {postData.link}\n nsfw: {postData.is_nsfw}\n ad: {postData.is_ad}")

            

    def getPostsDiv(self, content):  # parent div of data-scroller-first
        xpath = ".//div[4]/div[1]/div[4]"
        return content.find_element(By.XPATH, xpath)

    
    def getPosts(self, all_posts, post_limit):
        isLess = (lambda cnt, total: cnt < total) if post_limit else (lambda cnt, total: True)

        prev_posts, cnt = [], 0
        while isLess(cnt, post_limit):
            posts = all_posts.find_elements(By.XPATH, ".//div[@data-testid='post-container']")
            curr_posts = [p for p in posts if p not in prev_posts]
            prev_posts = posts
            
            for n, p in enumerate(curr_posts):
                img = self.getPostImage(p)
                yield p, img

                
                scrollScreen(self.DRIVER)

            cnt += len(curr_posts)

            
    def getPostImage(self, post):
        coord = post.location
        size = post.size
        
        img = self.DRIVER.get_screenshot_as_png()
        img = Image.open(BytesIO(img))

        left, top, right, bottom = [
            coord["x"],
            coord["y"],
            coord["x"]+size["width"],
            coord["y"]+size["height"],
        ]

        return img.crop((left, top, right, bottom))

    # def getPost(self, all_posts):  # iterate from 1
    #     while self.post_count <= self.post_limit:
    #         post = all_posts.find_element(By.XPATH, f".//div[{self.post_count}]")               
    #         yield post
                
    #         self.post_count += 1
            
            
    # def isAdvertisement(self, post):
    #     xpath = ".//div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span[2]/span[1]"
    #     try:
    #         is_advertisement = post.find_element(By.XPATH, xpath)
    #         if is_advertisement.text == "promoted":
    #             return True
        
    #         return False

    #     except NoSuchElementException:
    #         return False
        
        
                 
if __name__=="__main__":
    subreddit = "https://reddit.com/r/AskReddit/"
    driver = getWebDriver()

    redditScrapper = RedditScrapper(subreddit, driver=driver)
    redditScrapper.getPostListing(post_limit=10)
    
    for post in redditScrapper.post_listing:
        post.img.save(f"/tmp/{post.title}.png")

        
        # post.getCommentsListing()

        # for n, comment in enumerate(post.comments[0]):
        #     print(n, comment)
       
    
    









