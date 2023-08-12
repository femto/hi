import os
import hashlib
import json
import subprocess
import sys
import requests
import yaml

# Setup filesystem
CONFIG_FILE = os.path.join(os.getenv("HOME"), ".hi")
CACHE_DIR = os.path.join(os.getenv("HOME"), ".hicache")
os.makedirs(CACHE_DIR, exist_ok=True)
if not os.path.exists(CONFIG_FILE):
    open(CONFIG_FILE, 'a').close()

# Load settings
config = {}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)

HI_API_KEY = config.get("HI_API_KEY", "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
HI_MODEL = config.get("HI_MODEL", "gpt-4")
HI_API = config.get("HI_API", "https://api.openai.com/v1")
HI_EXECUTE = config.get("HI_EXECUTE", "true")
HI_REGENERATE = config.get("HI_REGENERATE", "false")

# Read the script passed to the interpreter
if len(sys.argv) < 2:
    print("Must pass a humanscript")
    sys.exit(1)
humanscript_path = sys.argv[1]
with open(humanscript_path, 'r') as f:
    humanscript = f.read()

# Execute from cache if we have a hit
script_name = os.path.basename(humanscript_path)
script_hash = hashlib.sha256(humanscript.encode()).hexdigest()
script_cache_path = os.path.join(CACHE_DIR, f"{script_name}-{script_hash}")
if HI_REGENERATE == "true" and os.path.exists(script_cache_path):
    os.remove(script_cache_path)
if os.path.exists(script_cache_path):
    if HI_EXECUTE == "true":
        subprocess.run(['bash', script_cache_path] + sys.argv[2:])
    else:
        with open(script_cache_path, 'r') as f:
            print(f.read())
    sys.exit()

# System prompt
system_prompt = """...
(omitted for brevity)
"""

# User prompt
user_prompt = f"""
### Input script:
{humanscript}

### Output script:"""

# Format JSON payload
data_payload = {
    "model": HI_MODEL,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": True
}

# Send request and handle the response
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {HI_API_KEY}"
}
response = requests.post(f"{HI_API}/chat/completions", headers=headers, data=json.dumps(data_payload))
if response.status_code == 200:
    response_data = response.json()
    output_script = response_data.get('choices', [{}])[0].get('delta', {}).get('content', "")
    with open(script_cache_path, 'w') as f:
        f.write(output_script)
    if HI_EXECUTE == "true":
        subprocess.run(['bash', '-s'] + sys.argv[2:], input=output_script.encode())
    else:
        print(output_script)
else:
    print(f"Error: {response.text}")

