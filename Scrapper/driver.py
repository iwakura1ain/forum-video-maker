from selenium import webdriver

def getWebDriver():
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("--disable-notifications")
    OPTIONS.add_argument("--disable-popup-blocking")
    OPTIONS.add_argument("--headless")
    OPTIONS.add_argument("--disable-gpu")

    DRIVER = webdriver.Chrome(options=OPTIONS)
    DRIVER.implicitly_wait(10)

    return DRIVER

def scrollScreen(driver, amount):
    #screen_height = driver.execute_script("return window.screen.height;")
    driver.execute_script(
        f"window.scrollTo(0, {amount})"
    )



