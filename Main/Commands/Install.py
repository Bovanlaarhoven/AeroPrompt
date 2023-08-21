#!/usr/bin/env python3

import sys
import os

library_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(library_parent_dir)

from Library.Modules import find_additional_args
from Library.Modules import subprocess
from Library.Modules import requests
from Library.Modules import BeautifulSoup
from Library.Modules import json

def install_package_with_pip(package_name):
    try:
        subprocess.run(["pip3", "install", package_name], check=True)
        print(f"Successfully installed {package_name} using pip3")
    except subprocess.CalledProcessError:
        print(f"pip3 installation of {package_name} failed, attempting to clone from Git...")
        install_package_with_git(package_name)

def install_package_with_git(package_name):
    github = requests.get(f"https://github.com/search?q={package_name}&type=repositories")
    soup = BeautifulSoup(github.text, "html.parser")
    json_data = soup.text[soup.text.find('{'):]
    data = json.loads(json_data)
    results = data.get("payload", {}).get("results", [])
    if results:
        name = results[0].get("hl_name", "")
        repo_link = f"https://github.com/{name}.git"
        print(f"Cloning {repo_link}...")
        subprocess.run(["git", "clone", repo_link])
    else:
        print(f"No Git repository found for {package_name}")

def main():
    additional_args = find_additional_args()
    if len(additional_args) >= 1:
        package_name = additional_args[0]
        install_package_with_pip(package_name)
    else:
        print("Usage: Install <package_name>")


if __name__ == "__main__":
    main()
