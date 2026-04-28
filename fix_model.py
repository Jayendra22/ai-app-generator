content = open("pipeline.py", "r").read()

# Replace old model with new one
content = content.replace("llama3-70b-8192", "llama-3.3-70b-versatile")
content = content.replace("llama3-8b-8192", "llama-3.3-70b-versatile")

open("pipeline.py", "w").write(content)
print("Model name fixed!")

# Verify
content2 = open("pipeline.py", "r").read()
if "llama-3.3-70b-versatile" in content2:
    print("Verified: correct model name found in pipeline.py")
else:
    print("ERROR: model name not found!")
    