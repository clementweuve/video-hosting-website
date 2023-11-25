"""-------Import OS module for directories checking system-------"""
import os

def check_directories():
    """Function that checks if all directories are there and create missing directories.
    Return: Nothing
    """
    if not os.path.isdir("static/profile_pictures"):
        os.mkdir("static/profile_pictures")
    if not os.path.isdir("static/videos"):
        os.mkdir("static/videos")
    if not os.path.isdir("static/miniatures"):
        os.mkdir("static/miniatures")
