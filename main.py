import pathlib
from src.automation.contact_us_automation import ContactUsAutomation


def main(filepath: str | pathlib.Path, save_dir:str | pathlib.Path=None) -> None | pathlib.Path:
    """Main function for initiating the automation

    Args:
        filepath (str | pathlib.Path): File path for which automation initiate
        save_dir (str, optional): Directory where the automation result file will stored
        
    Raises:
        None

    Returns:
        None: Returns when any error occured in automation
        result_filepath: Saved file path of automation
    """
    try:
        contact_us = ContactUsAutomation(csv_filepath=filepath, save_dir=save_dir)
        result_filepath = contact_us.automate()
    except Exception as e:
        print(str(e))
        return
    else:
        return result_filepath


if __name__ == "__main__":
    main(r'data\sample_data_2\6.csv')