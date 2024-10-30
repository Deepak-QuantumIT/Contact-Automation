import selenium
from selenium.webdriver.common.by import By



class CheckRequired:
    def __init__(self, search_space:selenium.webdriver.remote.webelement.WebElement) -> None:
        self.search_space = search_space
        
        
    def check1(self) -> bool:
        """Checks if any element in the search space contains 'is required' in its HTML.
        If found, it prevents form submission by returning False.
        
        Args:
            None
        
        Raises:
            None
            
        Returns:
            form_submission: True | False
        """
        
        key = "is required"
        form_submission = True
        try:
            all_elements = self.search_space.find_elements(By.CSS_SELECTOR, "*")
            for element in all_elements:
                if key in element.get_attribute('outerHTML'):
                    form_submission = False
                    break
        except Exception:
            pass
        finally:
            return form_submission

        
    def check2(self) -> bool:
        """Checks all 'input' elements for the 'required' attribute.
        If any required input is missing a value, it prevents form submission by returning False.
        
        Args:
            None
        
        Raises:
            None
            
        Returns:
            form_submission: True | False
        """
        
        form_submission = True
        try:
            all_elements = self.search_space.find_elements(By.TAG_NAME, 'input')
            for element in all_elements:
                if element.get_attribute('required') and not element.get_attribute('value'):
                    form_submission = False
                    break
        except Exception:
            pass
        finally:
            return form_submission


    def validate(self) -> bool:
        """Validates the form by running both check1 and check2.
        If any check fails, a custom exception is raised to stop the form submission.
        
        Args:
            None
            
        Raises:
            None
            
        Returns:
            bool
        """
        
        if self.check1() and self.check2():
            return True
        else:
            return False