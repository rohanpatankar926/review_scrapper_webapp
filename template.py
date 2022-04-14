from genericpath import exists
import os 
dirs=[
    "templates","static"
]
files=["main.py","__init__.py"]

for dir in dirs:
    os.makedirs(dir,exist_ok=True)
    
for file in files:
    with open(file,"w") as f:
        pass