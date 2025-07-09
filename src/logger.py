import logging
import os
from datetime import datetime

# Create a unique log file name with timestamp
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a path to the logs directory
logs_path=os.path.join(os.getcwd(),"logs")
os.makedirs(logs_path,exist_ok=True)

# Create full path to the log file
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


'''
Think of a log as a diary entry for your program.

    Whenever something important happens — like:

        a function starts

        a value is calculated

        an error occurs

'''
