
from selenium.webdriver.common.by import By
from time import sleep

def convert_to_am_pm(time_float):
    hours = int(time_float)
    minutes = int((time_float - hours) * 60)
    period = 'AM' if hours < 12 else 'PM'
    if hours > 12:
        hours -= 12
    elif hours == 0:
        hours = 12
    return f"{hours:02}:{minutes:02} {period}"
def adjust_break_time(driver, time_in):
    
    time_out = time_in + 0.5
    break_end = driver.find_element(By.CSS_SELECTOR, 'input[name="adj_break[out_time]"]')
    break_end.clear()
    time_out = convert_to_am_pm(time_out)
    break_end.send_keys(time_out)
    break_end.send_keys('\n')
    driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]').click()
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]').click()
