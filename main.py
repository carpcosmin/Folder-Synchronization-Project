import hashlib

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

