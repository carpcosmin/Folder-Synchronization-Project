The task is the following:
  Please implement a program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder. Solve the test task by writing a program in Python.
  Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source folder;
  Synchronization should be performed periodically;
  File creation/copying/removal operations should be logged to a file and to the console output;
  Folder paths, synchronization interval and log file path should be provided using the command line arguments;
  It is undesirable to use third-party libraries that implement folder synchronization;
  It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there is no point in implementing yet
  another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library.

The way I solved this task involves using hash-functions and hash-values. By comparing the hash-values of all files from the source folder with the hash-values from the replica folder,
the script knows whether to copy, modify or delete files from the replica folder.
