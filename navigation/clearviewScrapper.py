from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
import constants,functions
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import date, timedelta

def clearviewScrap():
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
    driver.get('https://qssweb.com/')
    
    user_input = driver.find_element(By.CLASS_NAME, 'textEntry')
    password_input = driver.find_element(By.CLASS_NAME, 'passwordEntry')
    user_input.send_keys(constants.CLEARVIEW_USER)
    password_input.send_keys(constants.CLEARVIEW_PASS)
    driver.find_element(By.CLASS_NAME, 'login-btn').click()
    # Calculate the date for two days ago
    target_date = date.today() - timedelta(days=2)
    formatted_date = target_date.strftime('%Y%m%d')

    # Use driver.get to navigate to the time sheet for the calculated day
    driver.get(f'https://qssweb.com/clearview/daily/timecards.aspx?stdDateStart={formatted_date}&stdDateEnd={formatted_date}&storeArea=&store=1846&timeframe=D&year={target_date.year}&week_ending=&month={target_date.month}&accPeriod=&daytype=C')
    
    # The site saves all the schedule data in a table so we find the table and get the info from it
    table = driver.find_element('css selector', 'table')
    rows = table.find_elements('tag name', 'tr')
    # Create a dictionary to store the data
    time_card_data = {}
    # Iterate through the rows and extract the data
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements('tag name', 'td')
        employee = cells[1].text
        job = cells[2].text
        type = cells[3].text
        time_in = cells[4].text  # Skip index 2
        time_out = cells[5].text
        payable_hours = cells[6].text
        flags = cells[7].text
        
        # Store the data in the dictionary
        time_card_data[employee] = {
            'Job': job,
            'Type': type,
            'Time In': time_in,
            'Time Out': time_out,
            'Payable Hours': payable_hours,
            'Flags': flags
        }
    #convert the dictionary to a pandas dataframe
    time_card_df = pd.DataFrame(time_card_data).T
    print(time_card_df)
    
    # gets an input from the user tht will run driver.quit() if q is entered
    quit = input("press q to quit")
    if quit == 'q':
        driver.quit()

