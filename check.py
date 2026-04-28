import os

print("templates folder exists:", os.path.exists("templates"))
print("index.html exists:", os.path.exists("templates/index.html"))
print("main.py exists:", os.path.exists("main.py"))
print("pipeline.py exists:", os.path.exists("pipeline.py"))
print("validator.py exists:", os.path.exists("validator.py"))

# Check index.html size
if os.path.exists("templates/index.html"):
    size = os.path.getsize("templates/index.html")
    print(f"index.html size: {size} bytes")
    if size == 0:
        print("WARNING: index.html is EMPTY!")
else:
    print("WARNING: index.html does NOT exist!")