import sys
import time
import random
import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import human_sleep


class EnquiryFiller:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver
        
        self.enquiry_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'help')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
        ]/following-sibling::select 
        |
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'help')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
        ]/following-sibling::*//select 
        | 
        //select[
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'help') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'help')
            or
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
        ] 
        | 
        //input[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
        ]
        | 
        //label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
        ]/following-sibling::input 
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
        ]//ancestor::label//following-sibling::input
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') 
        ]//preceding-sibling::input 
        | 
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enquiry') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')
        ]
        """
                
        
    def fill(self, enquiry:str) -> None:
        """Find and fills the enquiry/subject to related fields

        Args:
            enquiry: User enquiry/subject

        Raises:
            Exception: Raises exception with catched exceptions message
            
        Returns:
            None: None
        """
        try:
            enquiry_field = self.search_space.find_element(By.XPATH, self.enquiry_XPATH)

            # scroll till field, if located
            self.driver.execute_script("arguments[0].scrollIntoView(true);", enquiry_field)
            human_sleep(a=1, b=1)
        
            if not enquiry_field.is_displayed():
                raise exceptions.ElementNotVisibleException("Enquiry field found but not interactable.")
            
            if enquiry_field.tag_name == 'input' or enquiry_field.tag_name == 'textarea':
                enquiry_field.send_keys(enquiry)

            elif enquiry_field.tag_name == 'select':
                all_options = enquiry_field.find_elements(By.TAG_NAME, 'option')
                for option in all_options[1:]:
                    if option.text == enquiry:
                        option.click()
                        break
                else:
                    random.choice(all_options[1:]).click()
            else:
                raise Exception("Unsupported element type for Enquiry/Subject field: {}".format(enquiry_field.tag_name))
    
        except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException):
            raise Exception("Enquiry/Comments/Subject field not found.")
    
        except exceptions.ElementNotInteractableException:
            try:
                if enquiry_field.tag_name == "input":
                    self.driver.execute_script("arguments[0].value = arguments[1];", enquiry_field, enquiry)
            except Exception:
                raise Exception("Subject/Enquiry filling failed! Becuase interactions with this element will hit another element due to paint order.")
        
        except exceptions.StaleElementReferenceException:
            raise Exception("No such enquiry/subject fields is attached to DOM.")
        
        except exceptions.ElementClickInterceptedException:
            raise Exception("Enquiry/Subject filling failed! Becuase the field/element is obscured or blocked by another element due to overlapping or something else.")
            
        except Exception as e:
            raise Exception("An unexpected error occurred while working with enquiry/subject field")

        
        
        