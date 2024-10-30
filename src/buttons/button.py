import sys
import time
import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from src.utils import human_sleep
from src.custum_exception import CustomSeleniumException


class SubmitButton:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver

        self.button_XPATH = """//
        button[
            contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
            or 
            contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')
        ]
        |
        //div[
            @role='button' 
            and 
            (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
            or 
            contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send'))
        ]
        |
        //*[ 
            (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
            or 
            contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')) 
            and 
            (ancestor::button or ancestor::a)
        ]
        |
        //input[
            (@type='button' or @type='submit') 
            and 
            (
                contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
                or 
                contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send') 
                or 
                contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
                or 
                contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')
            )
        ]
        |
        //*[ 
            (@aria-label or @title or @placeholder)
            and 
            (contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
            or 
            contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send') 
            or 
            contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
            or 
            contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')) 
        ]
        """
        
    def click(self) -> None:
        """Clicks on buttons
        
        Args:
            None

        Raises:
            Exception: Raises the exception with catched exceptions message

        Returns:
            None: None
        """
        
        try:
            # Locate the button element within the search_space (form element)
            button = self.search_space.find_element(By.XPATH, self.button_XPATH)

            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            human_sleep(a=1, b=1)    

            # Check if the button is visible before proceeding
            if button.is_displayed() and button.is_enabled():
                button.submit()
                return None
            else:
                if not button.is_enabled():
                    return CustomSeleniumException("Form submission failed! Becuase not all required fields are filled!")
                raise exceptions.ElementNotVisibleException("Submit button is not displayed within the form.")
            
        except (exceptions.NoSuchElementException, exceptions.ElementNotVisibleException):
            raise Exception("Form submission failed! Becuase submit button not found within the search space.")
            
        except exceptions.StaleElementReferenceException:
            raise Exception("No any submit found attached to DOM or selected the wrong button which is no longer available.")
        
        except (exceptions.ElementClickInterceptedException, exceptions.ElementNotInteractableException, exceptions.WebDriverException):
            try:
                id = button.get_attribute('id')
                if id:
                    button = self.search_space.find_element(By.ID, id)
                    self.driver.execute_script("arguments[0].click();", button)
                else:
                    self.driver.execute_script("arguments[0].click();", button)
                return
            except Exception:
                raise Exception("Submit click failed! Becuase by clicking this button another element will hit due to paint order.")
            
        except CustomSeleniumException as e:
            raise Exception(f"{str(e)}")
            
        except Exception:
            raise Exception(f"Unexpected error occurred while working with Submit Button.")