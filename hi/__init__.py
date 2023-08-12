import os
import hashlib
import json
import subprocess
import sys
import requests
import yaml
import re

def sanitize_for_filename(input_str):
    # Remove invalid characters for file names using regular expression
    return re.sub(r'[\/:*?"<>|]', '_', input_str)


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

HI_API_KEY = os.getenv("HI_API_KEY", config.get("HI_API_KEY", "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"))
HI_MODEL = os.getenv("HI_MODEL", config.get("HI_MODEL", "gpt-4"))
HI_API = os.getenv("HI_API", config.get("HI_API", "https://api.openai.com/v1"))
HI_EXECUTE = os.getenv("HI_EXECUTE", config.get("HI_EXECUTE", "true"))
HI_REGENERATE = os.getenv("HI_REGENERATE", config.get("HI_REGENERATE", "false"))
def main():

    # Read the script passed to the interpreter
    if len(sys.argv) < 2:
        print("Must pass an argument")
        sys.exit(1)

    if len(sys.argv) >=3 and sys.argv[1] == "cache" and sys.argv[2] == "clear":


        for file in os.listdir(CACHE_DIR):
            os.remove(os.path.join(CACHE_DIR, file))

        sys.exit(0)


    hiscript_path = sys.argv[1]
    if sys.argv[1].endswith('.hi'):
        run_file(hiscript_path)
    else:
        run_command()

def run_file(hiscript_path):

    with open(hiscript_path, 'r') as f:
        hiscript = f.read()
    # Execute from cache if we have a hit
    script_name = os.path.basename(hiscript_path)

    execute(hiscript, script_name)
def run_command():


        hiscript = ' '.join(sys.argv[1:])
        # Execute from cache if we have a hit
        script_name = '-'.join(sys.argv[1:])
        sanitized_script_name = sanitize_for_filename(script_name)

        execute(hiscript, sanitized_script_name)


def execute(hiscript, script_name):
    script_hash = hashlib.sha256(hiscript.encode()).hexdigest()
    script_cache_path = os.path.join(CACHE_DIR, f"{script_name}-{script_hash}")
    if HI_REGENERATE == "true" and os.path.exists(script_cache_path):
        os.remove(script_cache_path)
    if os.path.exists(script_cache_path):

        if HI_EXECUTE == "true":
            subprocess.run(['bash', script_cache_path] + sys.argv[2:])
        else:
            with open(script_cache_path, 'r') as f:
                #breakpoint()
                print(f.read())
        sys.exit()
    # System prompt
    system_prompt = """You are humanscript, a human readable script interpreter, here are your rules:
    You read an input script consisting of human readable commands and convert it to a bash output script.
    You always start the output script with the exact shebang \"#!/usr/bin/env bash\".
    You take care to provide portable code that runs well on both macos and linux systems.
    Lines in the input script starting with a '#' are comments.
    You NEVER respond with markdown, only respond in pure bash.
    You NEVER explain anything about the script.
    """
    # User prompt
    user_prompt = f"""
    ### Input script:
    {hiscript}

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
        lines = response.text.split('\n')
        processed_lines = []

        for line in lines:
            # 去掉以 "data: " 开头的部分
            if line.startswith("data: "):
                line = line.replace("data: ", "", 1)
            if not line.startswith("[DONE]") and not line.strip() == '':
                processed_lines.append(line)

        # 将处理后的行合并回文本

        output_script = [json.loads(line).get('choices', [{}])[0].get('delta', {}).get('content', "") for line in
                         processed_lines]
        script = ''.join(output_script)

        with open(script_cache_path, 'w') as f:

            # print("writing to file: " + script_cache_path)
            f.write(script)
        if HI_EXECUTE == "true":

            subprocess.run(['bash', '-s'] + sys.argv[2:], input=script.encode())

        else:
            print(output_script)
    else:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    main()




