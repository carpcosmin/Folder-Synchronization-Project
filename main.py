import hashlib
import logging


# The function below configures the logging system
def logger_config(log_file_path):
    # configuration of a logger handler which outputs log messages on a file which is given as parameter
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,  # messages with a level of INFO or higher will be recorded
        format='%(asctime)s - &(message)s',  # format of the log: timestamp - message
        datefmt='%Y-%m-%d %H:%M:%S'  # timestamp format
    )

    # configuration of a separate handler for console-based logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - &(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)  # console_handler is added to the root logger of the logging system


# The function below computes MD5 hash of a file which is given as parameter
def get_file_hash_value(file_path):
    hasher = hashlib.md5()  # creation of MD5 hash object

    with open(file_path, "rb") as file:  # opening the file in binary read mode
        while True:
            data = file.read(4096)  # reading the data as chunks of 4096 bytes
            if not data:
                break
            hasher.update(data)  # updating the MD5 hasher object with the chunk of data read

    return hasher.hexdigest()  # the function returns the MD5 hash value
