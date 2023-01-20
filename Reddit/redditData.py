from .driver import getWebDriver, scrollScreen, waitForPage

from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from Log.log import *

from hashlib import md5

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
        try:
            return self.comment_level.index(level.get_attribute("style"))
            #return 0

        except ValueError:
            return 2

    
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
        "post": "//div[@id='AppRouter-main-content']/div[1]/div[1]/div[2]/div[3]/div[1]/div[last()]"
    }

    
    def __init__(self, post, driver=None):
        self.DRIVER = getWebDriver() if driver is None else driver
        
        #post data from main page
        self.title, self.link, self.is_ad, self.is_nsfw = self.getPostData(post)

        #post data from post content page
        self.postTitle, self.postBody, self.postImage = None, None, None

        #comment data
        self.comments = {0: [], 1: [], 2: []}  # level1, level2, level3+
        
        
    def __str__(self):
        return self.title


    def getHash(self):
        return md5((self.title + self.link).encode('utf-8')).hexdigest()
        

    
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
    
    @logCall("retrieving post contents")
    def getPostContents(self, comment_limit=None):
        self.DRIVER.get(self.link)
        waitForPage(self.DRIVER, self.link)
        
        content = self.DRIVER.find_element(By.XPATH, self.xpath["post"])
        self.getTitleContents(content)

        isLess = (lambda cnt, total: cnt < total) if comment_limit else (lambda cnt, total: True)
        comments_listing, cnt = self.getCommentsDiv(content), 0
        
        while (isLess(cnt, comment_limit)
               and cnt < len(comments_listing.find_elements(By.XPATH, "./*"))):
            
            try:
                comment = comments_listing.find_element(By.XPATH, f"./div[{cnt+1}]")
                commentData = CommentData(comment, self.getImage(comment))
                self.comments[commentData.level].append(commentData)
                logDebug(f"comment{cnt}: {commentData}")    
                
            except NoSuchElementException:
                logDebug(f"no comment for comment{cnt}")    
                comment_limit += 1
                pass
            
            cnt += 1        
            
            
    def getImage(self, element): #TODO
        try:
            retval = element.screenshot_as_base64
        
            if element.size["height"] > self.DRIVER.get_window_size()["height"]:
                logDebug("element bigger than screen")
                return retval
            else:
                return retval

        except TimeoutException:
            return None
        
        
    def getTitleContents(self, content):
        postTitleDiv = content.find_element(By.XPATH, ".//div[1]")
        postContent = postTitleDiv.find_element(By.XPATH, ".//div[@data-test-id='post-content']")

        self.postTitle = postContent.find_element(By.XPATH, "./div[3]/div[1]/div[1]/h1").text
        self.postBody = postContent.find_element(By.XPATH, "./div[last()-1]/div[1]")
        self.postImage = self.getImage(postTitleDiv)

        print("post content title: ", self.postTitle)
        
            
    def getCommentsDiv(self, content):
        comments_listing = content.find_element(By.XPATH, "./div[last()]/div[1]/div[1]/div[1]")
        return comments_listing
        







