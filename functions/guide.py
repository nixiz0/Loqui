import json
import os
import requests
import webbrowser
import subprocess


def open_html_file(file_path):
    webbrowser.open(f"file://{os.path.realpath(file_path)}")

def installation_guide():
    html_file_path = "functions/html_guide/guide.html"
    try:
        # Checks if WSL is installed
        wsl_install = subprocess.run(["wsl", "-l"], capture_output=True, text=True)
        if wsl_install.returncode != 0:
            # Download and install WSL if not already done
            subprocess.run(["wsl", "--install"], check=True)
            subprocess.run(["wsl", "sudo", "apt", "update", "&&", "sudo", "apt", "upgrade"], check=True)
            open_html_file(html_file_path)
        else:
            print("WSL is already installed.")
            open_html_file(html_file_path)

    except subprocess.CalledProcessError as e:
        print(f"An error has occurred: {e}")
        
    