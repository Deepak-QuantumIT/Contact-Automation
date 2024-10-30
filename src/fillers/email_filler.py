import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import human_sleep



class EmailFiller:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver
        
        self.email_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email') or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
            or
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
        ]/following-sibling::input 
        | 
        //label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email') or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
            or
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
        ]/following-sibling::*//input 
        | 
        //input[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
            or 
            contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or 
            contains(@type, 'email')
        ] 
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
        ]//ancestor::label//following-sibling::input
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail') 
        ]//preceding-sibling::input
        | 
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')
            or
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')
        ]
        """
            
        
    def fill(self, email:str, retries:int=2) -> None:
        """Find and fills the email to email field

        Args:
            email: User email
            retries: Retry number for retrying to load the page. 

        Raises:
            Exception: Raises the exception with catched exception message
            
        Returns:
            None: None
        """
        
        # print(f"Email fill called")
        
        counter = 0
        while counter < retries:
            try:
                email_field = self.search_space.find_element(By.XPATH, self.email_XPATH)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
                human_sleep(a=1, b=1)
            
                if email_field.is_displayed():
                    email_field.send_keys(email)
                    # print(f"email filled by selenium")
                    return
                else:
                    raise exceptions.ElementNotVisibleException(
                        "Email field is not interactable. Interactions with this field will hit another element due to paint order."
                    )
        
            except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException):
                raise Exception("Not found any field for Email!")
        
            except exceptions.ElementNotInteractableException:
                try:
                    self.driver.execute_script("arguments[0].value = arguments[1];", email_field, email)
                    # print(f"email filled by JS")
                    return
                except Exception:            
                    raise Exception("Email field is not interactable. Interactions with this field will hit another element due to paint order.")
                
            except exceptions.StaleElementReferenceException:
                counter += 1
                if counter >= retries:
                    # print(f"staled email filled")
                    raise Exception("No such email field is attached to DOM after several attempts!")
                    
            except Exception:
                raise Exception(f"Unexpected error occurred while working with email field.")

        
            