import pkg_resources
import subprocess
import sys

global FILE_PATH 


def get():
    try:
        FILE_PATH = "requirements.txt"
        with open("requirements.txt", "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print("Can't find requirements.txt")
        exit(1)


def check():
    pkg_resources.require(get())

def install():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        sys.exit()



