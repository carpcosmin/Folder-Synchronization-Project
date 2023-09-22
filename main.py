import hashlib
import logging
import os
import shutil
import argparse
import time

# The function below handles the synchronization of the folders
def synchronize_folders(source_path, replica_path):
    # Creating two arrays which store the hash-value of each file
    source_files = {}
    replica_files = {}

    # Populating the array corresponding to the source folder
    for root, _, files in os.walk(source_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_file_path, source_path)
            source_files[relative_path] = get_file_hash_value(source_file_path)

    # Populating the array corresponding to the replica folder
    for root, _, files in os.walk(replica_path):
        for file in files:
            replica_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(replica_file_path, replica_path)
            replica_files[relative_path] = get_file_hash_value(replica_file_path)

    # Copying new and modified files from the source folder to the replica folder
    for rel_path, source_hash in source_files.items():
        replica_file_path = os.path.join(replica_path, rel_path)
        if rel_path not in replica_files or source_hash != replica_files[rel_path]:
            logging.info(f"Copying {rel_path}")
            shutil.copy2(os.path.join(source_path, rel_path), replica_file_path)

    # Remove files from replica that no longer exist in source
    for rel_path, _ in replica_files.items():
        replica_file_path = os.path.join(replica_path, rel_path)
        if rel_path not in source_files:
            logging.info(f"Deleting {rel_path}")
            os.remove(replica_file_path)


# The function below configures the logging system
def logger_config(log_file_path):
    # configuration of a logger handler which outputs log messages on a file which is given as parameter
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,  # messages with a level of INFO or higher will be recorded
        format='%(asctime)s - %(message)s',  # format of the log: timestamp - message
        datefmt='%Y-%m-%d %H:%M:%S'  # timestamp format
    )

    # configuration of a separate handler for console-based logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
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

def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Tool")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Log file path")
    args = parser.parse_args()

    logger_config(args.log_file)

    logging.info("Folder synchronization started.")
    while True:
        synchronize_folders(args.source, args.replica)
        logging.info("Folder synchronization completed.")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
