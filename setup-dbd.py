#!/usr/bin/env python3

import pathlib
import urllib.request
import shutil

import subprocess
import sys

base_path = pathlib.Path(__file__).parent.absolute()
downloads = {
        "dbd_requirements.txt": "https://raw.githubusercontent.com/wowdev/WoWDBDefs/master/code/Python/requirements.txt",
        "dbd.py": "https://raw.githubusercontent.com/wowdev/WoWDBDefs/master/code/Python/dbd.py",
        "definitions/SpellEffect.dbd": "https://raw.githubusercontent.com/wowdev/WoWDBDefs/master/definitions/SpellEffect.dbd",
        }

for file_name, url in downloads.items():
    print("Downloading {}...".format(file_name))
    file_name = base_path / file_name
    file_name.parent.mkdir(parents=True, exist_ok=True)
    print("> urlopen {}".format(url))
    with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
        print("> copyfileobj {}".format(out_file.name))
        shutil.copyfileobj(response, out_file)
print()

print("Installing requiremnts for dbd...")
pip_install = [sys.executable, "-m", "pip", "install", "-r", "dbd_requirements.txt"]
print("> {}".format(" ".join(pip_install)))
subprocess.check_call(pip_install, cwd=base_path)
