import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from src.utils import human_sleep

class NameFiller:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver
        
        # XPaths for first and last name
        self.f_name_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first name') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fname')
        ]/following-sibling::input 
        | 
        //label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first name')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fname')
        ]/following-sibling::*//input 
        | 
        //input[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first name') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fname')
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'firstname')
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fname')
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'firstname')
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fname') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'firstname') 
            or 
            contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first name')
        ] 
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first name') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
        ]//ancestor::label//following-sibling::input
        | 
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first name')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first')
        ]//preceding-sibling::input
        |
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'first') 
        ]
        """
        
        self.l_name_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last name') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lname')
        ]/following-sibling::input 
        | 
        //label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last name')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lname')
        ]/following-sibling::*//input 
        | 
        //input[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last name') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lname')
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lastname')
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lname')
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lastname')
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lname') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lastname') 
            or 
            contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last name')
        ] 
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last name') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
        ]//ancestor::label//following-sibling::input
        | 
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last name')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last')
        ]//preceding-sibling::input
        |
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'last') 
        ]
        """
        
        self.full_name_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name') 
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fullname')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')
        ]/following-sibling::input 
        | 
        //label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fullname')
            or 
            contains(translate(@for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')
        ]/following-sibling::*//input 
        | 
        //input[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fullname') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fullname') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'fullname') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name') 
            or 
            contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name')
        ] 
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name') 
        ]//ancestor::label//following-sibling::input
        | 
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')
        ]//preceding-sibling::input
        |
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'full name') 
        ]"""
        

    def fill(self, f_name:str, l_name:str, retries:int=2) -> None:
        """Find and fills the name to name fields

        Args:
            f_name: First name
            l_name: Last name
            retries: Retry number for retrying to load the page
            
        Raises:
            Exception: Raises the exception with catched exception message
            
        Returns:
            None: None
        """
        
        # print(f"Name fill called")
        
        counter = 0
        while counter < retries:
            # print(f"First loop: {counter}")
            try:
                f_name_field = self.search_space.find_element(By.XPATH, self.f_name_XPATH)
                l_name_field = self.search_space.find_element(By.XPATH, self.l_name_XPATH)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", f_name_field)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", l_name_field)
                human_sleep(a=1, b=2)
                
            
                # print(f"Name field found")

                if f_name_field.is_displayed() and l_name_field.is_displayed():
                    # print(f"F Name & L Name Elment visible")
                    f_name_field.send_keys(f_name)
                    l_name_field.send_keys(l_name)
                    # print(f"F Name & L Name Elment interectable by selenium")
                    return 
                else:
                    counter += 1
                    # print(f"Name field not displayed")

            except exceptions.ElementNotInteractableException:
                try:
                    self.driver.execute_script("arguments[0].value = arguments[1];", f_name_field, f_name)
                    self.driver.execute_script("arguments[0].value = arguments[1];", l_name_field, l_name)
                    # print(f"F Name & L Name Elment interectable by JS")
                    return
                except Exception as e:
                    # print(e)
                    raise Exception("First name & Last name field found! But fields are not intereactable. Interactions with this element/field will hit the another element due to paint order.")
            
            except exceptions.StaleElementReferenceException as e:
                # print(str(e))
                counter += 1
                if counter >= retries:
                    break
            
            except (exceptions.NoSuchElementException, exceptions.WebDriverException) as e:
                # print(str(e))
                break
        
            except Exception as e:
                # print(str(e))
                break
            
        # print(f"Name fill called")
            
        counter = 0
        while counter < retries:
            # print(f"Second loop: {counter}")
            try:
                full_name_field = self.search_space.find_element(By.XPATH, self.full_name_XPATH)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", full_name_field)
                human_sleep(a=1, b=2)
    
                if full_name_field.is_displayed():
                    # print(f"Full Name Elment visible")
                    full_name = f_name + " " + l_name
                    full_name_field.send_keys(full_name)
                    # print(f"Full Name Elment interectable by selenium")
                    return
                else:
                    raise exceptions.ElementNotVisibleException("Full name is found! But not interactable.")

            except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException):
                raise Exception("Website does not have a contact form. Instead, it provides direct contact details.")

            except exceptions.ElementNotInteractableException:
                try:
                    self.driver.execute_script("arguments[0].value = arguments[1];", full_name_field, f_name + " " + l_name)
                    # print(f"Full Name Elment interectable by JS")
                    return
                except Exception:
                    raise Exception("Full name is found! But not interactable. Bacuase interactions with this field will hit another element due to paint order.")
    
            except exceptions.StaleElementReferenceException:
                countet += 1
                if counter >= retries:
                    # print(f"Name field not found after staled")
                    raise Exception("Stale Element! No name fields (full name, first name, or last name) are attached to the DOM.")
            
            except Exception:
                raise Exception(f"Unexpected error occurred while filling the name field.")

