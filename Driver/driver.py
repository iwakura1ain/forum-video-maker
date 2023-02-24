from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium_stealth import stealth
from selenium.webdriver.firefox.options import Options

from Log.log import *

from time import sleep

def getWebDriver(headless=True):
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("--disable-notifications")
    OPTIONS.add_argument("--disable-popup-blocking")
    
    if headless:    
        OPTIONS.add_argument("--headless")
        OPTIONS.add_argument("--disable-gpu")

    DRIVER = webdriver.Chrome(options=OPTIONS)
    DRIVER.implicitly_wait(5)

    stealth(
        DRIVER,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )
    return DRIVER

    # if loginReddit(DRIVER):
    #     return DRIVER
    # return None


    
    

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
    getPage(driver, loginUrl)

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
        #logInfo("login succeeded")
        return True    

    #logInfo("login failed")
    return False

def loginYT(driver, username="ernie937", passwd="dksckddjs1!"):
    getPage(driver, "https://www.youtube.com")
    login = driver.find_element(By.ID, "masthead")
    login = login.find_element(
        By.XPATH,
        ".//div[@id='container']/div[@id='end']/div[@id='buttons']/ytd-button-renderer[1]"
    )
    loginUrl = login.find_element(By.XPATH, ".//a").get_attribute("href")

    getPage(driver, loginUrl)
    emailField = driver.find_element(By.XPATH, ".//input[@type='email']")
    emailField.click()
    emailField.clear()
    emailField.send_keys(username)

    sleep(2)
    
    nextButton = driver.find_element(
        By.XPATH,
        ".//c-wiz[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]"
    )
    nextButton.click()
   

    # passwdField = driver.find_element(By.XPATH, ".//input[@type='password']")
    # passwdField.click()
    # passwdField.clear()
    # passwdField.send_keys(passwd)

    # nextButton = driver.find_element(
    #     By.XPATH,
    #     ".//c-wiz[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/button[1]"
    # )
    # print(nextButton.get_attribute("class"))
    # nextButton.click()

    

