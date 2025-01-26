from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
import constants
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
    
    # Find the username field
    username_field = driver.find_element('id', 'username')
    # Find the password field
    password_field = driver.find_element('id','password')
    # Find the client id field  
    client_id_field = driver.find_element('id','client-id')
    
    # Type the username
    username_field.send_keys(constants.AMEEGO_USER)
    # Type the password
    password_field.send_keys(constants.AMEEGO_PASS)
    # Type the client id
    client_id_field.send_keys(constants.AMEEGO_ID)
    
    # Find the sign in button
    sign_in_button = driver.find_element('css selector', 'button[type="submit"]')
    sign_in_button.click()
    
    # listen for a key press, if i press shift + q it will run driver.quit()
    
    # Close the browser
    driver.quit()

