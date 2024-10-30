import time
import random
import uuid
import selenium
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait



def get_page(driver: selenium.webdriver.remote.webdriver.WebDriver, URL:str, timeout:int=30, retries:int=2)-> None:
    """Attempts to load the website in the passed browser instance

    Args:
        driver: Browser instance[Firefox, Chrome etc.]
        URL: Website link/url
        timeout: Time limit to wait for the website to load completely
        retries: Retry number for retrying to load the website.

    Raises:
        Exception: Timeout Error! When website took too long to load, excceds time limit.
        Exception: When failed in loading the website after total retires.

    Returns:
        None: None
    """
    
    counter = 0
    while counter < retries:
        try:
            driver.get(URL)
            WebDriverWait(driver, timeout).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            return
        except exceptions.TimeoutException:
            raise Exception("Timeout! The website took too long to load, excceds time limit.")
        except exceptions.WebDriverException:
            counter += 1
            if counter == retries:
                raise Exception("Failed to load the webpage after retries! The provided URL may be Broken/Temporarily Unavailable/Network Issue/404 or something else.")
            else:
                # wait for 1 second and retry to load the page
                human_sleep(a=1, b=1)
                

def human_sleep(a:int=1, b:int=2) -> None:
    """Sleeps the code execution for random time in given second range

    Args:
        a: Upper limit
        b: Lower limit
        
    Returns:
        None: None
    """
    time.sleep(random.randint(a, b))
    
    
def get_random_name(ext:str='.csv') -> str:
    """Generates the random file name with passed file extension

    Args:
        ext: File extension(ex. .csv, .pdf etc.)

    Returns:
        filename: Random uuid file name
    """
    filename = f"{uuid.uuid4()}{ext}"
    return filename
    