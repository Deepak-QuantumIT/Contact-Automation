import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import human_sleep


class ContactClick:
    def __init__(self,
                driver: selenium.webdriver.remote.webdriver.WebDriver, 
                ) -> None:
        self.driver = driver
        
        self.hamburger_XPATH = [
            "//i[@aria-hidden='true' and following-sibling::span[contains(text(), 'Menu')]]",
    
            "//i[contains(@class, 'bars') or contains(@class, 'menu') or contains(@class, 'nav') or contains(@class, 'toggle')]",

            "//button[contains(@class, 'hamburger') or contains(@class, 'menu') or contains(@class, 'nav') or @aria-label='Menu' or @aria-label='Navigation']",

            "//nav//div[contains(@class, 'menu') or contains(@class, 'nav') or contains(@class, 'toggle')]",
    
            "//*[contains(@data-toggle, 'menu') or contains(@data-toggle, 'nav')]",
    
            "//a[contains(@class, 'menu') or contains(@class, 'nav') or @aria-label='Menu']",

            "//span[contains(text(), 'Menu') or contains(text(), 'Navigation') or contains(text(), 'Toggle')]",

            "//*[@id='menu' or @role='navigation' or @role='menu']",
        ]

        self.dropdown_XPATH = """//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'more') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')]//parent::a"""
        
        # Select links which,
        # 1. href attribute contain [contact, connect, touch] like text
        # 2. Same as in text
        self.XPATH = """//a[
            (
                contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') 
                or 
                contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'connect') 
                or 
                contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'touch')
            ) 
            and 
            (
                contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') 
                or 
                contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'connect') 
                or 
                contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'touch')
            )
        ]"""
        
    
    def click(self, timeout:int=20, retries:int=2) -> None:
        """Finds the Contact Us page link and clicks on that link

        Args:
            timeout (int, optional): Time limit to wait for the page to load completely.
            retries (int, optional): Retry number for retrying to load the page.

        Raises:
            Exception: Raises, When Contact Us page not loaded in time range. 
            Exception: Raises, When Contact Us link not attached with DOM after retries.
            
        Returns:
            None: None
        """
        
        counter = 0
        while counter < retries:
            # find element all over the page, locate links whether it is in dropdown, hamburger, footer etc.
            contact_us_links = self.driver.find_elements(By.XPATH, self.XPATH)
            
            # print(f"Links found: {len(contact_us_links)}")
            if not contact_us_links:
                return
            
            try:
                for contact_us in contact_us_links:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", contact_us)
                    human_sleep(a=1, b=2)
                    
                    if contact_us.is_displayed():
                        # print(f"Link Visible")
                        self.driver.execute_script("arguments[0].removeAttribute('target');", contact_us)
                        try:
                            contact_us.click()
                            # print(f"link clicked by selenium")
                            WebDriverWait(self.driver, timeout).until(
                                lambda driver: driver.execute_script('return document.readyState') == 'complete'
                            )
                            return
                        except exceptions.TimeoutException:
                            raise exceptions.TimeoutException("Timeout! Contact Us page not loaded in time range.")     
                        except (exceptions.ElementClickInterceptedException, exceptions.ElementNotInteractableException):
                            try:
                                self.driver.execute_script("arguments[0].click()", contact_us)
                                # print(f"link clicked by JS")
                                WebDriverWait(self.driver, timeout).until(
                                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                                )
                                return
                            except exceptions.TimeoutException:
                                raise exceptions.TimeoutException("Timeout! Contact Us page not loaded in time range.")  
                        except exceptions.StaleElementReferenceException:
                            counter += 1
                            if counter >= retries:
                                # print("link staled after retries")
                                raise exceptions.StaleElementReferenceException("Contact Us link not attached with DOM after retries.")
                            break
                else:
                    # if none of the links clicked, click anyone using JS
                    self.driver.execute_script("arguments[0].click()", contact_us_links[0])
                    WebDriverWait(self.driver, timeout).until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete'
                    )
                    return
            except exceptions.TimeoutException as e:
                raise Exception(str(e))
            except exceptions.StaleElementReferenceException as e:
                raise Exception(str(e))
            except Exception:
                return
