from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *

def getWebDriver(headless=True):
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("--disable-notifications")
    OPTIONS.add_argument("--disable-popup-blocking")
    
    if headless:    
        OPTIONS.add_argument("--headless")
        OPTIONS.add_argument("--disable-gpu")

    DRIVER = webdriver.Chrome(options=OPTIONS)
    DRIVER.implicitly_wait(5)

    return DRIVER

def scrollScreen(driver, amount=None):
    if amount is None:
        amount = driver.execute_script("return window.screen.height;")
        
    driver.execute_script(
        f"window.scrollTo(0, {amount})"
    )

def waitForPage(driver, url):
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(lambda d: d.current_url == url)
        return True
    
    except TimeoutException:
        return False
        



