import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from src.utils import human_sleep


class MessageFiller:
    def __init__(self, 
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement,
                ) -> None:
        self.search_space = search_space
        self.driver = driver
        
        self.message_XPATH = """//
        label[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message') 
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comments')
            or
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'question')
        ]/following-sibling::textarea 
        | 
        //textarea[
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message') 
            or
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message') 
            or
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message') 
            or 
            contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comments') 
            or 
            contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comments') 
            or 
            contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comments') 
            or 
            contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comments')
        ] 
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comment')
        ]//ancestor::label//following-sibling::textarea
        |
        //*[
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message')
            or 
            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comment') 
        ]//preceding-sibling::textarea
        """
                
        
    def fill(self, message:str) -> None:
        """Find and fills the message to related field

        Args:
            message: User query message

        Raises:
            Exception: Raises the exception with catched exceptions message
            
        Returns:
            None: None
        """
        
        try:
            msg_field = self.search_space.find_element(By.XPATH, self.message_XPATH)
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", msg_field)
            human_sleep(a=1, b=1)
                
            if msg_field.is_displayed():
                msg_field.send_keys(message)
            else:
                raise exceptions.ElementNotVisibleException("Message/Comments field not inntereactable or incorrect element type.")
        
        except (exceptions.ElementNotVisibleException, exceptions.NoSuchElementException):
            raise Exception("No fields found for Message.")
        
        except exceptions.ElementNotInteractableException:
            try:
                self.driver.execute_script("arguments[0].value = arguments[1];", msg_field, message)
            except Exception:
                raise Exception("Message/Comment filling failed! Becuase interactions with this element will hit another element due to paint order.")
        
        except exceptions.StaleElementReferenceException:
            raise Exception("Message field is no longer attached to the DOM.")
                
        # except exceptions.ElementClickInterceptedException:
        #     raise Exception("Message filling failed! Becuase the field/element is obscured or blocked by another element due to overlapping or something else.")
        
        except Exception as e:
            raise Exception("Unexpected error occurred while working with message field.")
        