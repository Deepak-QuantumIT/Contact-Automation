import os
import logging
from pathlib import Path
from datetime import datetime


# create a bucket where all logs will be stored
logfiles_bkt = os.path.join(os.getcwd(), 'LOGS')
os.makedirs(logfiles_bkt, exist_ok=True)

logfile = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
logfile_path = Path(os.path.join(logfiles_bkt, logfile))


# create the logfile
with open(logfile_path, 'w') as file:
    pass


logging.basicConfig(
    filename=logfile_path,
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
)