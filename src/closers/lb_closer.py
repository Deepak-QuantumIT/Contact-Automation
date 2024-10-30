import selenium
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from src.utils import human_sleep


class LightBoxCloser:
    def __init__(self, driver:selenium.webdriver.remote.webdriver.WebDriver) -> None:
        self.driver = driver        
        self.lb_XPATH = """//div[@class='lightbox-close']
        |
        //button[contains(@class, 'close')]
        |
        //div[contains(@class, 'ad-close')]
        |
        //span[contains(text(), 'Close')]
        |
        //div[@role='dialog']//button[contains(text(), '×')]
        |
        //button[contains(@aria-label, 'Close')]
        |
        //button[contains(@aria-label, 'close')]
        """
        
    def close(self) -> None:
        """LightBoxCloser method for closing the banners/lightboxes/dialougs etc.
        
        Args:

        Raises:
            Exception: Raise error when any error occured while closing the box
            
        Returns:
            None: None
        """
        
        lb_boxes = self.driver.find_elements(By.XPATH, self.lb_XPATH)
            
        if not lb_boxes:
            return
        
        for lb_box in lb_boxes:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", lb_box)
                human_sleep(a=1, b=1)
                
                if lb_box.is_enabled() and lb_box.is_displayed():
                    lb_box.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click()", lb_box)
            except Exception as e:
                raise e