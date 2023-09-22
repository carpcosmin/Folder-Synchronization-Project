import hashlib
import logging
import os
import shutil


# The function below handles the synchronization of the folders
def synchronize_folders(source_folder_path, replica_folder_path):
    # Creating two arrays which store the hash-value of each file
    source_folder_files = {}
    replica_folder_files = {}

    # Populating the array corresponding to the source folder
    for root, _, files in os.walk(source_folder_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_file_path, source_folder_path)
            source_folder_files[relative_path] = get_file_hash_value(source_file_path)

    # Populating the array corresponding to the replica folder
    for root, _, files in os.walk(replica_folder_path):
        for file in files:
            replica_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(replica_file_path, replica_folder_path)
            replica_folder_files[relative_path] = get_file_hash_value(replica_file_path)

    # Copying new and modified files from the source folder to the replica folder
    for rel_path, source_hash in source_folder_files.items():
        replica_file_path = os.path.join(replica_folder_path, rel_path)
        if rel_path not in replica_folder_files or source_hash != replica_folder_files[rel_path]:
            logging.info(f"Copying {rel_path}")
            shutil.copy2(os.path.join(source_folder_path, rel_path), replica_file_path)

    # Remove files from replica that no longer exist in source
    for rel_path, _ in replica_folder_files.items():
        replica_file_path = os.path.join(replica_folder_path, rel_path)
        if rel_path not in source_folder_files:
            logging.info(f"Deleting {rel_path}")
            os.remove(replica_file_path)


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
