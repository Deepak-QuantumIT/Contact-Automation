import time
import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import human_sleep


class ReCaptcha:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver
        
        self.reCaptcha_XPATH = """//input[
            (
                contains(@class, 'captcha') 
                or 
                contains(@id, 'captcha') 
                or 
                contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')
            ) 
            and 
            @type='checkbox'
        ]"""
        
    def verify(self) -> None:
        """Handles the captchas(currently only click captcha)
        
        Args:
            None

        Raises:
            Exception: Raises the exceptions with catched exceptions message
            
        Returns:
            None: None
        """
        
        try:
            captcha = self.search_space.find_element(By.XPATH, self.reCaptcha_XPATH)
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", captcha)
            human_sleep(a=1, b=1)    
            
            if captcha.is_displayed():
                captcha.click()
            else:
                raise exceptions.ElementNotVisibleException("Captcha not intetectable or selected wrong element as captcha!")
        
        except exceptions.StaleElementReferenceException:
            raise Exception("No longer any captcha attached to DOM")
        
        except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException):
            raise Exception("No such reCaptcha found!")
        
        except exceptions.ElementClickInterceptedException:
            try:
                self.driver.execute_script("arguments[0].click();", captcha)
            except Exception:
                raise Exception("Captcha verification failed! Becuase the field/element is obscured or blocked by another element due to overlapping or something else.")
        
        except exceptions.ElementNotInteractableException:
            raise Exception("Captcha verfication failed! Becuase interactions with this element will hit another element due to paint order.")
                
        except Exception:
            raise Exception("Unidentified error occured while working with captcha verification!")
        
        
        
            