from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from Driver.driver import *
from .redditData import *

from Log.log import *

import sqlite3


class RedditScrapper:
    def __init__(self, name, subreddit, dbfile="test.db", driver=None):
        self.subreddit = subreddit
        self.DRIVER = getWebDriver() if driver is None else driver

        self.db = DBConnection(dbfile)
        self.db.getTable(name)
        

    @logCall("retrieving post listing")
    def getPostListing(self, post_limit=None):
        getPage(self.DRIVER, self.subreddit)
    
        content = self.DRIVER.find_element(By.ID, "AppRouter-main-content")
        posts_div = self.getPostsDiv(content)

        postContentDriver = getWebDriver()
        for post in self.getPosts(posts_div, post_limit):
            postData = PostData(post, driver=postContentDriver)

            if self.savePost(postData):
                logDebug(
                    f"post: {postData.title}\n"
                    f"link: {postData.link}\n"
                    f"nsfw: {postData.is_nsfw}\n"
                    f"ad: {postData.is_ad}"
                )

                yield postData
            else:
                logDebug(
                    f"existing post {postData.title}"
                )
            
            
    def getPostsDiv(self, content):  # parent div of data-scroller-first
        xpath = ".//div[4]/div[1]/div[last()-1]"
        return content.find_element(By.XPATH, xpath)

    
    def getPosts(self, all_posts, post_limit=None):
        isLess = (lambda cnt, total: cnt < total) if post_limit else (lambda cnt, total: True)
        cnt = 0
        
        while True:
            posts = all_posts.find_elements(By.XPATH, ".//div[@data-testid='post-container']")
            scrollAmount = 0
            for p in posts:
                if not isLess(cnt, post_limit):
                    return
                
                scrollAmount += p.size["height"]
                cnt += 1
                yield p
                
            scrollScreen(self.DRIVER, scrollAmount)
                
            # curr_posts = [p for p in posts if p not in prev_posts]
            # prev_posts = posts

            # scroll_amount = 0
            # for n, p in enumerate(curr_posts):
            #     if not isLess(cnt, post_limit):
            #         return
                
            #     scroll_amount += p.size["height"]
            #     cnt += 1
            #     yield p
            
            #cnt += len(curr_posts)

    def savePost(self, postData):
        #return self.db.insertValue(postData.getHash())
        return self.db.insertValue(postData)

        


class DBConnection:
    def __init__(self, dbFile):
        self.connection = sqlite3.connect(dbFile)
        self.cur = self.connection.cursor()
        self.tableName = None
        

    def execute(self, sql):
        return self.cur.execute(sql)
        
        
    def getTable(self, tableName):
        table = self.execute(
            f"SELECT * FROM sqlite_master "
            f"WHERE type='table' AND name='{tableName}';"
        )
        if table.fetchone() is None:
            self.execute(
                f"CREATE TABLE {tableName}(hash varchar(32));"
            )
            
        self.tableName = tableName
        
        
    def checkValueExists(self, value):
        value = self.execute(
            f"SELECT hash FROM {self.tableName} "
            f"WHERE hash='{value}'"
        )
        if value.fetchone() is None:
            return False
        return True 
    
    
    def insertValue(self, value):
        value = value.getHash()
        
        if self.checkValueExists(value):
            return False
        
        self.execute(
            f"INSERT INTO {self.tableName} VALUES "
            f"('{value}')"
        )
        self.connection.commit()
        return True

        
# if __name__=="__main__":
#     subreddit = "https://www.reddit.com/r/AskReddit/"
#     driver = getWebDriver()

#     redditScrapper = RedditScrapper(subreddit, driver=driver)

#     if not redditScrapper.loginReddit():
#         quit()
            
#     redditScrapper.getPostListing(post_limit=1)
    
#     for i, post in enumerate(redditScrapper.post_listing):
#         post.getPostContents(comment_limit=50)
#         img = Image.open(BytesIO(base64.b64decode(post.postImage)))
#         img.save(f"/tmp/post{i}.png")

#         for j, comment in enumerate(post.comments[0]):
#             img = Image.open(BytesIO(base64.b64decode(comment.image)))
#             img.save(f"/tmp/post{i}-comment{j}.png")

        
        

       
    
    










