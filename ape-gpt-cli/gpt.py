import subprocess
import os
import sys
import datetime
import argparse
import base64
import yaml
import openai

CONFIG_FILE = 'gpt_config.yml'
SOURCES_DIR = 'sources'
RESPONSES_DIR = 'responses'

os.makedirs(SOURCES_DIR, exist_ok=True)
os.makedirs(RESPONSES_DIR, exist_ok=True)

def save_api_key():
    key = input("Enter your OpenAI API key: ")
    encoded_key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump({'api_key': encoded_key}, file)

def load_api_key():
    if not os.path.exists(CONFIG_FILE):
        print(f"Configuration file {CONFIG_FILE} not found. Please run 'gpt config' to set up your API key.")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as file:
        config = yaml.safe_load(file)
        encoded_key = config.get('api_key', '')
        return base64.b64decode(encoded_key.encode('utf-8')).decode('utf-8')

def clone_repository(repo_url):
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(SOURCES_DIR, repo_name)
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)
    return repo_name

def concatenate_sources(source_dirs):
    concatenated_content = ""
    for src_dir in source_dirs:
        full_src_dir = os.path.join(SOURCES_DIR, src_dir)
        for root, dirs, files in os.walk(full_src_dir):
            for file in files:
                if file.endswith('.lock'):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        concatenated_content += '######## ' + file_path + '\n\n'
                        concatenated_content += f.read() + '\n\n'
                except Exception as e:
                    print(f"Skipping non-text file or error reading file: {file_path} - {e}")
    return concatenated_content

def send_gpt_prompt(concatenated_content, prompt):
    openai.api_key = load_api_key()
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": concatenated_content
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description='CLI tool to interact with GPT and GitHub repositories.')
    subparsers = parser.add_subparsers(dest='command')

    config_parser = subparsers.add_parser('config', help='Configure the OpenAI API key.')
    clone_parser = subparsers.add_parser('clone', help='Clone a GitHub repository into the sources directory.')
    clone_parser.add_argument('repo_url', type=str, help='GitHub repository URL to clone.')
    prompt_parser = subparsers.add_parser('prompt', help='Send a prompt to GPT with concatenated source directories.')
    prompt_parser.add_argument('--src', action='append', help='Source directory to include in the prompt to GPT.')
    prompt_parser.add_argument('prompt', type=str, help='Prompt text to send to GPT.')

    args = parser.parse_args()

    if args.command == 'config':
        save_api_key()
    elif args.command == 'clone':
        clone_repository(args.repo_url)
    elif args.command == 'prompt':
        if not args.src:
            print("Error: No source directories provided for the prompt.")
            sys.exit(1)
        concatenated_content = concatenate_sources(args.src)
        response = send_gpt_prompt(concatenated_content, args.prompt)
        print(response)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        response_filename = os.path.join(RESPONSES_DIR, f"gpt_response_{timestamp}.txt")
        with open(response_filename, 'w', encoding='utf-8') as f:
            f.write('######## Sources: \n\n' + ', '.join(args.src) + '\n\n' + '######## Prompt: ' + args.prompt + '\n\n' + '######## Response: \n\n' + response)

if __name__ == "__main__":
    main()