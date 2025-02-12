from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
from functions import functions
import constants
from selenium.webdriver.common.by import By
import time
from time import sleep
from datetime import timedelta
import pandas as pd
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
    time.sleep(1)
    # uses driver.get to navigate tot he time sheet for the day
    driver.get('https://c.myameego.com/manager/time-and-attendance.php?date='+str(date.today() - timedelta(days=1)))

    # the site saves all the schedule data in a table so we find the table and get the info from it
    table = driver.find_element('css selector', 'table')
    rows = table.find_elements('tag name', 'tr')
    
    # Create a dictionary to store the data
    schedule_data = {}
    

    # Iterate through the rows and extract the data
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements('tag name', 'td')
        if len(cells) > 1:
            name = cells[0].text
            wage = cells[1].text
            start_end = cells[2].text
            length = cells[3].text
            overtime = cells[4].text
            weekly_overtime = cells[5].text
            cost = cells[6].text
            # Split the start_end value into start and end times
            start_time, end_time = start_end.split('-')
            # Store the data in the dictionary
            schedule_data[name] = [name, wage, start_time, end_time, length, overtime, weekly_overtime, cost]
           
    
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(schedule_data, orient='index', columns=['name', 'Wage', 'Start', 'End', 'Length', 'Overtime', 'Weekly Overtime', 'Cost'])

    # Convert 'Length' column to float hours
    df['Length'] = df['Length'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) else x)
    df['Start'] = df['Start'].apply(lambda x: float(x.split(':')[0]) % 12 + (12 if 'pm' in x.lower() else 0) + float(x.split(':')[1][:2]) / 60)
    df['End'] = df['End'].apply(lambda x: float(x.split(':')[0]) % 12 + (12 if 'pm' in x.lower() else 0) + float(x.split(':')[1][:2]) / 60)
    
    for i in df.index:
        fullShift = df.loc[i]['End'] - df.loc[i]['Start']
        lenght = df.loc[i]['Length']
        #if the calculation is negative then that means its a midnight shift(this is how i will handle it for now)
        if fullShift < 0:
            fullShift = 24 - df.loc[i]['Start'] + df.loc[i]['End']
            breakTime = fullShift - lenght
            
        else:
            breakTime = fullShift - lenght
            

        if lenght >= 5.5 and breakTime != 0.5 and df.loc[i]['name'] != 'MichaelH':
            print(df.loc[i]['name'])
            # Find the row containing the name
            row_element = driver.find_element('xpath', f"//tr[td[contains(text(), '{df.loc[i]['name']}')]]")
            # Find the link in the same row with class 'text-center link hidden-print'
            link_element = row_element.find_element('tag name', 'i')
            link_element.click()
            # Wait for the popup to appear and find the edit link
            sleep(1)
            
            edit_links = driver.find_elements(By.CSS_SELECTOR, 'a.link.small')
            if len(edit_links)>1:
                edit_links[0].click()
                sleep(0.5)
                # Click the button after opening the first link
                button = driver.find_element(By.CSS_SELECTOR, 'button[data-ajax*="time-and-attendance.edit.break.php"][class*="btn-danger"]')
                button.click()
                sleep(0.5)
            edit_link = driver.find_element(By.CSS_SELECTOR, 'a.link.small')
            edit_link.click()
            sleep(0.5)
            time_in = driver.find_element(By.CSS_SELECTOR,  'input[name="adj_break[in_time]"]').get_attribute('value')
            time_out = driver.find_element(By.CSS_SELECTOR, 'input[name="adj_break[out_time]"]').get_attribute('value')
            time_in = float(time_in.split(':')[0]) + float(time_in.split(':')[1][:2]) / 60
            time_out = float(time_out.split(':')[0]) + float(time_out.split(':')[1][:2]) / 60
            break_total = time_out - time_in
            if break_total != 0.5:
                if break_total < 0.5:
                    print('Break time is less than 30 minutes')
                    
                    # Call the function to adjust the break time
                    functions.adjust_break_time(driver, time_in)
                elif break_total > 0.5:
                    print('Break time is more than 30 minutes')  
                    functions.adjust_break_time(driver, time_in)
                else:
                    print('Break time is correct you shouldnt be seeing this')
                
            

    # gets an input from the user tht will run driver.quit() if q is entered
    quit = input("press q to quit")
    if quit == 'q':
        driver.quit()
    
    
    

