from sigint_lib.app_env import VERSION
import os
import subprocess


DBS_NAME = "sigint.sqlite3"
APP_AUTHOR = "Prime Security"


if os.name == "nt":
    pyinstaller_path = ";."
else:
    pyinstaller_path = ":."
    
    

subprocess.call(
    [ "pyinstaller", "main.py" ,"--onefile",  f"--add-data=sigint.sqlite3{pyinstaller_path}" ]
)