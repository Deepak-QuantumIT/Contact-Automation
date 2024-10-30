import sys
import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from src.custum_exception import CustomException


class CompanyFiller:
    def __init__(self, search_space: selenium.webdriver.remote.webelement.WebElement) -> None:
        self.search_space = search_space

        self.company_n_XPATH = """//input[
                contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'company name') or
                contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'company') or
                contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'company') or
                contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'company')
                ]"""
                
                
    def fill(self, company_n):
        try:
            company_field = self.search_space.find_element(By.XPATH, self.company_n_XPATH)
            
            if company_field.is_displayed():
                company_field.send_keys(company_n)
            else:
                raise exceptions.ElementNotInteractableException("Company Name field found but not interectable")
        except exceptions.ElementNotInteractableException as e:
            raise CustomException(e, sys)
        except Exception as e:
            raise CustomException(e, sys)