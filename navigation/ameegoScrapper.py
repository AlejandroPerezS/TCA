from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os

def ameegoScrap():
    # Path to the Chrome WebDriver (relative path)
    webdriver_path = os.path.join('chromedriver-win64', 'chromedriver.exe')
    # Set up the Chrome WebDriver service
    service = ChromeService(webdriver_path)

    # Set Chrome options
    options = Options()
    options.add_argument('--start-maximized')

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Open a website
    driver.get('https://login.myameego.com/')

    # Close the browser
    driver.quit()

