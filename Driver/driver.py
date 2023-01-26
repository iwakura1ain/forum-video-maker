from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from Log.log import *

def getWebDriver(headless=True):
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("--disable-notifications")
    OPTIONS.add_argument("--disable-popup-blocking")
    
    if headless:    
        OPTIONS.add_argument("--headless")
        OPTIONS.add_argument("--disable-gpu")

    DRIVER = webdriver.Chrome(options=OPTIONS)
    DRIVER.implicitly_wait(5)

    if loginReddit(DRIVER):
        return DRIVER
    return None


def getPage(driver, url):
    driver.get(url)
    return waitForPage(driver, url)


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
        

def loginReddit(driver, username="904ehd", passwd="912ehd406gh"):
        loginUrl = "https://www.reddit.com/login/"
        driver.get(loginUrl)
        waitForPage(driver, loginUrl)
        
        usernameField = driver.find_element(By.ID, "loginUsername")
        usernameField.click()
        usernameField.clear()
        usernameField.send_keys(username)

        passwdField = driver.find_element(By.ID, "loginPassword")
        passwdField.click()
        passwdField.clear()
        passwdField.send_keys(passwd)
        
        submit = driver.find_element(By.XPATH, ".//button[@type='submit']")
        submit.click()
        
        if waitForPage(driver, "https://www.reddit.com/"):
            logInfo("login succeeded")
            return True    

        logInfo("login failed")
        return False


