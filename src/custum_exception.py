import sys
from selenium.common.exceptions import WebDriverException


def error_msg_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    message = 'Error occured in python script name [{0}], line number [{1}], error  message [{2}]'.format(filename, exc_tb.tb_lineno, str(error))
    return message


class CustomException(Exception):
    def __init__(self, error_msg, error_detail:sys):
        super().__init__(error_msg)
        self.error_message = error_msg_detail(error = error_msg, error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
    
class CustomSeleniumException(WebDriverException):
    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        self.message = message or "A unexpected selenium error occured."