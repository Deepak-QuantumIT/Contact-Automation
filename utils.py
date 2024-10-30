import os
import pathlib
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def automation_report(filepath: str | pathlib.Path) -> None | dict:
    """Generate the highlevel report for given automation result file

    Args:
        filepath (str | pathlib.Path): Automation result file path

    Raises:
        None

    Returns:
        None: Reture None, when any occured during generation of report
        report: Returns highlevel report
    """
    try:
        df = pd.read_csv(filepath)
        df['Reason'] = df['Reason'].fillna('').astype(str)
        
        report = {}
    
        report['Total Websites'] = len(df["Website"].tolist())
        report['Total Successfull Automation'] = len(df[df["Result"]== "Success"])
        report['Total Failed Automation'] = len(df[df["Result"]== "Fail"])    
        report['Total Faild Automation by Reason'] = {}

        # Filter out 'None' or empty values from the list of unique reasons
        reasons = [reason for reason in df['Reason'].unique().tolist() if reason and reason != 'None']
        for reason in reasons:
            if reason:
                report['Total Faild Automation by Reason'][reason] = len(df[df["Reason"]== reason])
        
        return report
    except Exception as e:
        print(str(e))
        return None
    
    
def remove_files(filepaths:list) -> None:
    """Removes the files from directories"""
    for filepath in filepaths:
        os.remove(filepath)
    
    
def create_dirs(dirs:list) -> None:
    """Creates the directories"""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        
        
class MailSender:
    def __init__(self, sender, passkey):
        self.sender = sender
        self.passkey = passkey
        self.message = MIMEMultipart()
        self.message['From'] = self.sender  
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
    def send_mail(self, receiver, subject, body, attachments_paths=None):
        self.message['Subject'] = subject
        self.message['To'] = receiver
        body_part = MIMEText(body)
        self.message.attach(body_part)
        
        if attachments_paths:
            for path in attachments_paths:
                with open(path,'rb') as file:
                    filename = os.path.basename(path)
                    self.message.attach(MIMEApplication(file.read(), Name=filename))
                
        self.server.login(self.sender, self.passkey)
        self.server.sendmail(self.sender, receiver, self.message.as_string())
            
    def tear_down(self):
        self.server.quit()
        
        
