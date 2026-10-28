
import os

path = os.path.expanduser("~/Documents/F1_UDP_Dashboard/page")

# List only HTML files
html_files = [
    file for file in os.listdir(path)
    if file.endswith(".html")
]

print("HTML files in", path, ":")
print(html_files)
