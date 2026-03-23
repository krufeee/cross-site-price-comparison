from pathlib import Path
from time import sleep

if Path("..database/data.csv").exists():
    print("File exists")
else:
    print("File does NOT exist")

sleep(5)


if Path("../database/categories.csv").exists():
    print("File exists")
else:
    print("File does NOT exist")