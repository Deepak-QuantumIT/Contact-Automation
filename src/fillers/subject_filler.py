import sys
import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from src.custum_exception import CustomException


class SubjectFiller:
    def __init__(self, search_space: selenium.webdriver.remote.webelement.WebElement) -> None:
        self.search_space = search_space
        
        self.subj_XPATH = """//ancestor::label[contains(text(), 'Subject')]/following-sibling::div/input | //ancestor::label[contains(text(), 'Subject')]/following-sibling::input | //input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject') or contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'subject')]"""
        
        
    def fill(self, subject):
        try:
            subject_field = self.search_space.find_element(By.XPATH, self.subj_XPATH)
            
            if subject_field.is_displayed():
                subject_field.send_keys(subject)
            else:
                raise exceptions.ElementNotInteractableException("EMail field found but not interectable")
        except exceptions.ElementNotInteractableException as e:
            raise CustomException(e, sys)
        except Exception as e:
            raise CustomException(e, sys)
            
                