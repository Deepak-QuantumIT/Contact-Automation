import os
import pathlib
from pathlib import Path
import time
from dotenv import load_dotenv

import pandas
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options

from src.clicks.contact_click import ContactClick
from src.closers.lb_closer import LightBoxCloser
from src.fillers.name_filler import NameFiller
from src.fillers.email_filler import EmailFiller
from src.fillers.phone_filler import PhoneFiller
from src.fillers.enquiry_filler import EnquiryFiller
from src.fillers.message_filler import MessageFiller
from src.captcha.reCaptcha import ReCaptcha
from src.checks.required_check import CheckRequired
from src.buttons.button import SubmitButton
from src.utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()


class ContactUsAutomation:    
    def __init__(self, csv_filepath, save_dir=None):  
        # FireFox Driver Configurations here 
        self.options = Options()
        self.options.binary_location = str(Path(os.path.abspath(os.path.join(os.path.dirname(__file__), os.environ.get("GECKO_DRIVER_PATH")))))
        self.options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.90 Safari/537.36")
        self.options.set_preference("dom.webnotifications.enabled", False)
        self.options.set_preference("permissions.default.image", 2)
        self.options.set_preference("dom.disable_beforeunload", True)
        self.options.add_argument('--headless')
                
        # XPATHS => Contact form [
            # choose form which have following fields mandatory
            # 1. Name
            # 2. Email or Phone Number
            # 3. Submit or Send button(Not subscribe, etc.)
            # ]  
        self.form_XPATH = """//form[
            (
                .//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')]
                and 
                (
                    .//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')]
                    or
                    .//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]
                )
            )
            or
            (
                .//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')]
                and 
                (
                    .//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mail')]
                    or
                    .//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]
                )
            )
            and
            (
                .//button[
                    contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')
                    or 
                    contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')
                ]
                or
                .//a[
                    contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')
                    or 
                    contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')
                ]
                or
                .//input[
                    (@type='submit' or @type='button')
                    and 
                    (
                        contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
                        or 
                        contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')
                    )
                ]
                or
                .//div[
                    @role='buttom'
                    and
                    (
                        contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') 
                        or 
                        contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')
                    )
                ]
            )
        ]"""

        self.csv_filepath = csv_filepath
        self.save_dir = save_dir if save_dir else "results"
        os.makedirs(os.path.join(os.getcwd(), self.save_dir), exist_ok=True)
        
        self.result_csv = get_random_name(ext='.csv')
        self.result_filepath = os.path.join(os.getcwd(), self.save_dir, self.result_csv)
    
    
    def fill_contact_form(self, 
                        driver: selenium.webdriver.remote.webdriver.WebDriver, 
                        search_space: selenium.webdriver.remote.webdriver.WebDriver | selenium.webdriver.remote.webelement.WebElement, 
                        details: pd.core.series.Series, 
                        by=None) -> None:
        
        """Helper method for filling the form
        
        Args:
            driver: Browser instance[Firefox, Chrome etc.]
            search_space: Page area where we need to search the elements
            details: Pandas dataframe row/automation data
            by: form | page, defualts to None
            
        Raises: Raises exceptions according to filling exceptions
        
        Returns:
            None: None
        """
        
        # fill name field
        try:
            name_filler = NameFiller(driver=driver, search_space=search_space)
            name_filler.fill(f_name=details["First Name"], l_name=details["Last Name"])
        except Exception as e:
            raise e
            
        # fill email field
        try:
            email_filler = EmailFiller(driver=driver, search_space=search_space)
            email_filler.fill(email=details["Email"])
        except Exception as e:
            raise e
        
        # fill phone number field
        try:
            phone_filler = PhoneFiller(driver=driver, search_space=search_space)
            phone_filler.fill(phone=details["Phone Number"])
        except Exception as e:
            pass
            
        # fill enquiry/subject field
        try:
            enquiry_filler = EnquiryFiller(driver=driver, search_space=search_space)
            enquiry_filler.fill(enquiry=details["Subject"])
        except Exception as e:
            pass

        # fill message/comment Field
        try:
            message_filler = MessageFiller(driver=driver, search_space=search_space)
            message_filler.fill(message=details["Comments"])
        except Exception as e:
            pass
                
        # perform reCaptcha verification
        try:
            recaptcha = ReCaptcha(driver=driver, search_space=search_space)
            recaptcha.verify()
        except Exception as e:
            pass
        
        # click the submit button(submit form)
        try:
            submit_button = SubmitButton(driver=driver, search_space=search_space)
            submit_button.click()
        except Exception as e:
            raise e
        
        # check all required fields are filled or not
        if by == "form":
            # Check that all required fields are filled or not
            try:
                required_checker = CheckRequired(search_space=search_space)
                is_all_filled = required_checker.validate()
                if not is_all_filled:
                    raise Exception("Form submission failed! Becuase not all required fields are filled!")
            except Exception as e:
                raise e

        
    def automate_contact_form(self, record:pandas.core.series.Series) -> dict:
        """Main function for contact us form automation
        
        Args:
            record: Pandas dataframe's row with columns ["website", "First Name", "Last Name", "Phone Number", "Email", "Subject", "Comments"]
            
        Raises:
            None
            
        Returns:
            dict: Dictionary containing information about automation for provided record
        """
        
        # keep automation result as dict for appending with final .csv report
        result_rec = {}
            
        URL = record["website"]
        result_rec["Website"] = URL

        try:
            driver = webdriver.Firefox(options=self.options)                   # driver 1
            # driver = webdriver.Chrome(options=self.options)                  # driver 2
        except Exception:
            result_rec["Result"] = "Fail"
            result_rec["Reason"] = "Browser instance initialization failed!"
            result_rec["Automation Status"] = "Fail"
            return result_rec
        else:
            driver.maximize_window()
                    
        # Initial Steps:
        # 1. Open the website
        # 2. Close the advertisements/banners/dialougs' etc.
        try:
            get_page(driver=driver, URL=URL)
        except Exception as e:
            result_rec["Result"] = "Fail"
            result_rec["Reason"] = str(e)
            result_rec["Automation Status"] = "Fail"
            driver.quit()
            return result_rec
        
        try:
            lb_closer = LightBoxCloser(driver=driver, search_space=driver)
            lb_closer.close()
        except Exception as e:
            # This can be replaced according to cases. Means, If we want to not proceed if any lightbox is found & not closed, we can return back.
            # currently ignoring it
            pass
        human_sleep(a=1, b=1)

        # Next steps:
        # 1. Find the contact us page, if found move to page
        # 2. else, stay on main page
        # Contact Us link can found in: [Nav bar, Nav Dropdown, Nav Hamburger, Mid Page, Page Footer]
        # print(f"URL: {URL}")
        try:
            contact_clicker = ContactClick(driver=driver)
            contact_clicker.click()
        except Exception as e:
            result_rec["Result"] = "Fail"
            result_rec["Reason"] = str(e)
            result_rec["Automation Status"] = "Fail"
            # human_sleep(a=5, b=5)
            driver.quit()
            return result_rec
        # else:
        #     result_rec["Result"] = "Pass"
        #     result_rec["Reason"] = None
        #     result_rec["Automation Status"] = "Pass"
        #     human_sleep(a=5, b=5)
        #     driver.quit()
        #     return result_rec
            
        # Next steps:
        # 1. Find the contact us form on page, if found:
        #     - Fill the details on form by using form as search space for finding input fields
        # 2. else if not found:
        #     - Fill the details by searching the input fields on all over the page.
        #
        # try to fill the form by form
        human_sleep(a=5, b=5)
        
        try:
            contact_forms = driver.find_elements(By.XPATH, self.form_XPATH)
                
            if not contact_forms:
                raise exceptions.NoSuchElementException("No Contact-Us form found! Trying searching input fields directly.")

            for form in contact_forms:
                if form.is_displayed():
                    # print(f"Form found...")
                    self.fill_contact_form(driver=driver, search_space=form, details=record, by="form")    
                    result_rec["Result"] = "Success"
                    result_rec["Reason"] = "None"
                    result_rec["Automation Status"] = "Pass"
                    break
            else:
                raise exceptions.ElementNotVisibleException("Contact form found but not visible! Trying searching input fields directly.")
            
        # try to fill the form by direct, if no form found
        except (exceptions.NoSuchElementException, exceptions.ElementNotVisibleException, exceptions.ElementNotInteractableException, exceptions.StaleElementReferenceException):
            try:
                # print("form not found")
                human_sleep(a=1, b=1)
                self.fill_contact_form(driver=driver, search_space=driver, details=record)
                result_rec["Result"] = "Success"
                result_rec["Reason"] = "None"
                result_rec["Automation Status"] = "Pass"
                
        # catch the errors which occured in between form filling, mark form as fail
            except Exception as e:
                error_msg = str(e)
                result_rec["Result"] = "Fail"
                result_rec["Reason"] = error_msg
                result_rec["Automation Status"] = "Fail"
        
        except Exception as e:
            error_msg = str(e)
            result_rec["Result"] = "Fail"
            result_rec["Reason"] = error_msg
            result_rec["Automation Status"] = "Fail"
        finally:
            driver.quit()
        
        return result_rec


    def automate(self, max_workers:int=1) -> pathlib.Path:
        """Automate the contact us page for given data

        Args:
            max_workers: Number of threads workers, defualt to 1.
            
        Raises:
            None

        Returns:
            pathlib.Path: Generate automation result file
        """
        data = pd.read_csv(Path(self.csv_filepath), chunksize=50)
        result = pd.DataFrame(columns=["Website", "Result", "Reason", "Automation Status"])
        
        for chunk_no, chunk in enumerate(data):            
            s_time = time.time()
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self.automate_contact_form, chunk.iloc[i, :]) for i in range(len(chunk))]
                for future in as_completed(futures):
                    result = result._append(future.result(), ignore_index=True)
            
            e_time = time.time()
            print(f"Time Consumed by Chunk {chunk_no + 1}: {round((e_time-s_time), 2)} sec.\n")
    
            human_sleep(a=1, b=5)
            
        result.to_csv(self.result_filepath, index=False)        
        return Path(self.result_filepath)