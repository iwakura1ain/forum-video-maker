from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from Driver.driver import *
from Log.log import *

class Uploader:
    def __init__(self, driver=None):
        self.DRIVER = getWebDriver(headless=False) if driver is None else driver

    def login(self):
        loginYT(self.DRIVER)
        

uploader = Uploader()
uploader.login()
