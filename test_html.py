import os

# Check current directory
print("Current directory:", os.getcwd())

# Check templates folder
print("Templates exists:", os.path.exists("templates"))

# List files in templates
if os.path.exists("templates"):
    files = os.listdir("templates")
    print("Files in templates:", files)

# Check index.html
if os.path.exists("templates/index.html"):
    size = os.path.getsize("templates/index.html")
    print("index.html size:", size, "bytes")
    with open("templates/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    print("First 100 chars:", content[:100])
else:
    print("ERROR: index.html NOT FOUND!")
    