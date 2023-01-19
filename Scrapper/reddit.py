from driver import getWebDriver, scrollScreen

from urllib.parse import urlsplit

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    InvalidArgumentException, StaleElementReferenceException, NoSuchElementException
)

from PIL import Image
from io import BytesIO
import base64

# import sys
# sys.path.append("../Log")
# from Log.log import *


class CommentData:
    comment_level = ["padding-left: 16px;", "padding-left: 37px;"]  # level1 , level2
    xpath = {
        "base": ".//div[contains(@class, 'RichTextJSON-root')]",
        "level": "./../../../..",
        "upvote": ".//../../div[3]/div[1]/div[1]",   
    }
    
    def __init__(self, comment, image):
        comment = comment.find_element(By.XPATH, self.xpath["base"])

        #comment data
        self.text = [p.text for p in comment.find_elements(By.XPATH, ".//*")]
        self.level = self.getCommentLevel(comment)
        self.upvote = self.getUpvote(comment)

        #movie data
        self.image = image
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
        #post info
        "base": ".//div[@data-adclicklocation='title']",
        "title": ".//div[1]/a[1]/div[1]/h3",
        "link": ".//div[1]/a[1]",
        "is_nsfw": ".//div[2]/div[2]/span",
        "is_ad": ".//div[3]/div[1]/div[1]/div[1]/div[1]/span[2]/span[1]",

        #post contents
        #"post": ".//div[@data-testid='post-container']/..",
        "post": "//div[@id='AppRouter-main-content']/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]"
    }

    
    def __init__(self, post, driver=None):
        self.DRIVER = getWebDriver() if driver is None else driver

        #post data
        self.title, self.link, self.is_ad, self.is_nsfw = self.getPostData(post)
        self.image = None

        #comment data
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


    
    def getImage(self, element): #TODO
        retval = element.screenshot_as_base64
        
        if element.size["height"] > self.DRIVER.get_window_size()["height"]:
            return retval
        else:
            return retval

    def getPostTitleContents(self, content):
        print("class: ", content.get_attribute("class"))
        postTitle = content.find_element(By.XPATH, ".//div[1]")
        self.image = self.getImage(postTitle)

        return postTitle
        
    def getPostContentsDiv(self, content):
        comments_listing = content.find_element(By.XPATH, "./div[last()]/div[1]/div[1]/div[1]")
        return comments_listing
        
        
    def getPostContents(self, comment_limit=None):
        self.DRIVER.get(self.link)
        content = self.DRIVER.find_element(By.XPATH, self.xpath["post"])

        _ = self.getPostTitleContents(content)

        isLess = (lambda cnt, total: cnt < total) if comment_limit else (lambda cnt, total: True)
        comments_listing, cnt = self.getPostContentsDiv(content), 0
        while isLess(cnt, comment_limit):
            comment = comments_listing.find_element(By.XPATH, f"./div[{cnt+1}]")
            try:
                commentImg = self.getImage(comment)
                commentData = CommentData(comment, commentImg)
                self.comments[commentData.level].append(commentData)
                
                print(commentData)
                
            except:
                pass
            
            cnt += 1

            
class RedditScrapper:
    def __init__(self, subreddit, driver=None):
        self.subreddit = subreddit
        self.DRIVER = getWebDriver() if driver is None else driver
    
        self.post_listing = []
        
        
    def getPostListing(self, post_limit=None):
        self.DRIVER.get(self.subreddit)
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        
        content = self.DRIVER.find_element(By.ID, "AppRouter-main-content")
        content.screenshot("/tmp/main.png")
        posts_div = self.getPostsDiv(content)

        for post in self.getPosts(posts_div, post_limit):
            postData = PostData(post, driver=self.DRIVER)
            self.post_listing.append(postData)
            print(f"post: {postData.title}\n link: {postData.link}\n nsfw: {postData.is_nsfw}\n ad: {postData.is_ad}")
           

    def getPostsDiv(self, content):  # parent div of data-scroller-first
        xpath = ".//div[4]/div[1]/div[4]"
        return content.find_element(By.XPATH, xpath)

    
    def getPosts(self, all_posts, post_limit):
        isLess = (lambda cnt, total: cnt < total) if post_limit else (lambda cnt, total: True)
        prev_posts, cnt = [], 0
        while True:
            posts = all_posts.find_elements(By.XPATH, ".//div[@data-testid='post-container']")
            curr_posts = [p for p in posts if p not in prev_posts]
            prev_posts = posts

            scroll_amount = 0
            for n, p in enumerate(curr_posts):
                if not isLess(cnt, post_limit):
                    return
                
                scroll_amount += p.size["height"]
                cnt += 1
                yield p
                
                

            scrollScreen(self.DRIVER, scroll_amount)
            #cnt += len(curr_posts)

    def loginReddit(self, username="904ehd", passwd="912ehd406gh"):
        loginUrl = "https://www.reddit.com/login/"
        self.DRIVER.get(loginUrl)
        
        usernameField = self.DRIVER.find_element(By.ID, "loginUsername")
        usernameField.click()
        usernameField.clear()
        usernameField.send_keys(username)

        passwdField = self.DRIVER.find_element(By.ID, "loginPassword")
        passwdField.click()
        passwdField.clear()
        passwdField.send_keys(passwd)
        
        submit = self.DRIVER.find_element(By.XPATH, ".//button[@type='submit']")
        submit.click()
        
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        
        if self.DRIVER.find_element(By.CLASS_NAME, "AnimatedForm__errorMessage").text != "":
            return False
        
        return True
            

            
if __name__=="__main__":
    subreddit = "https://reddit.com/r/AskReddit/"
    driver = getWebDriver()

    redditScrapper = RedditScrapper(subreddit, driver=driver)

    #if not redditScrapper.loginReddit():
     #   print("login failed")
      #   quit()
            
    redditScrapper.getPostListing(post_limit=1)
    
    for i, post in enumerate(redditScrapper.post_listing):
        post.getPostContents(comment_limit=30)
        img = Image.open(BytesIO(base64.b64decode(post.image)))
        img.save(f"/tmp/post{i}.png")

        for j, comment in enumerate(post.comments[0]):
            img = Image.open(BytesIO(base64.b64decode(comment.image)))
            img.save(f"/tmp/post{i}-comment{j}.png")

        
        

       
    
    










