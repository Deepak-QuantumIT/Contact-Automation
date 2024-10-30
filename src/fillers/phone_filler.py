import time
import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import human_sleep


class PhoneFiller:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver
        
        self.contact_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mobile') or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')
        ]/following-sibling::input 
        | 
        //input[
            @type='tel' 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mobile') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') 
            or     
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')
            or 
            contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')
            or 
            contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')
        ]
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mobile')
        ]//ancestor::label//following-sibling::input
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mobile') 
        ]//preceding-sibling::input
        |  
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')
            or
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')
            or
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mobile')
        ]
        """
                
        self.c_code_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'country') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'code')
        ]/following-sibling::select 
        | 
        //select[
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'country') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'country') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'country') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'country') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'code') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'code') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'code') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'code')
        ]
        """
                
                
    def fill(self, phone:str) -> None:
        """Find and fills the phone number to contact field
        
        Args:
            phone: User phone/contact number

        Raises:
            Exception: Raises the exception with catched exception message
            
        Returns:
            None: None
        """
        
        try:
            contact_number = ''
            splits = phone.split(' ', 1)
        
            # check if country code
            if len(splits) == 2:
                country_code, phone_number = splits[0], splits[1]

                try:
                    c_code_field = self.search_space.find_element(By.XPATH, self.c_code_XPATH)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", c_code_field)
                    human_sleep(a=1, b=1)    
                    if c_code_field.is_displayed():
                        all_codes = c_code_field.find_elements(By.TAG_NAME, 'option')

                        for code in all_codes:
                            if code.text == country_code:
                                code.click()
                                break
                        else:
                            contact_number = country_code + " "
                    else:
                        raise exceptions.ElementNotVisibleException("Country code dropdown is not interactable.")

                except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException, exceptions.ElementNotInteractableException, exceptions.StaleElementReferenceException, exceptions.ElementClickInterceptedException):
                    contact_number = country_code + " "
        
            else:
                phone_number = splits[0]

            try:
                p_number_field = self.search_space.find_element(By.XPATH, self.contact_XPATH)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", p_number_field)
                human_sleep(a=1, b=1)
                if p_number_field.is_displayed():
                    contact_number += phone_number
                    p_number_field.send_keys(contact_number)
                else:
                    raise exceptions.ElementNotVisibleException("Phone number field is not interactable.")
        
            except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                raise Exception("Phone number field not found.")
            
            except exceptions.ElementNotInteractableException:
                try:
                    self.driver.execute_script("arguments[0].value = arguments[1];", p_number_field, phone_number)
                except Exception:
                    raise Exception("Phone number filling failed! Becuase interactions with that element will hit another element due to paint order.")
                        
            # except exceptions.ElementClickInterceptedException:
            #     raise Exception("Phone Number filling failed! Becuase the field/element is obscured or blocked by another element due to overlapping or something else.")

        except Exception as e:
            raise Exception(f"Unexpected error occurred while processing the phone number.")

