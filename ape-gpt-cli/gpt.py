import subprocess
import os
import sys
import datetime
import argparse
import base64
import yaml
from anthropic import Anthropic, APIError, APIConnectionError, APITimeoutError

CONFIG_FILE = 'claude_config.yml'
SOURCES_DIR = 'sources'
RESPONSES_DIR = 'responses'

os.makedirs(SOURCES_DIR, exist_ok=True)
os.makedirs(RESPONSES_DIR, exist_ok=True)

def save_api_key():
    key = input("Enter your Claude API key: ")
    encoded_key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump({'api_key': encoded_key}, file)
    print("API key saved successfully.")

def load_api_key():
    if not os.path.exists(CONFIG_FILE):
        print(f"Configuration file {CONFIG_FILE} not found. Please run 'claude config' to set up your API key.")
        sys.exit(1)
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)
            encoded_key = config.get('api_key', '')
            return base64.b64decode(encoded_key.encode('utf-8')).decode('utf-8')
    except Exception as e:
        print(f"Error loading API key: {str(e)}")
        sys.exit(1)

def clone_repository(repo_url):
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(SOURCES_DIR, repo_name)
    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        print(f"Successfully cloned repository to {repo_path}")
        return repo_name
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {str(e)}")
        sys.exit(1)

def concatenate_sources(source_dirs):
    concatenated_content = ""
    for src_dir in source_dirs:
        full_src_dir = os.path.join(SOURCES_DIR, src_dir)
        if not os.path.exists(full_src_dir):
            print(f"Error: Source directory '{src_dir}' not found in {SOURCES_DIR}")
            sys.exit(1)
            
        for root, dirs, files in os.walk(full_src_dir):
            for file in files:
                if file.endswith('.lock'):  # Skip lock files
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        concatenated_content += f'######## {file_path}\n\n'
                        concatenated_content += f.read() + '\n\n'
                except Exception as e:
                    print(f"Skipping non-text file or error reading file: {file_path} - {e}")
    return concatenated_content

def send_claude_prompt(concatenated_content, prompt):
    try:
        client = Anthropic(api_key=load_api_key())
        
        system_prompt = """
/- Analyze the provided source code and documentation.
/- Base your answers solely on the provided content.
/- If the answer cannot be found in the sources, state that clearly.
/- When referencing specific parts of the code, cite the relevant file paths.
/- Provide concrete examples when possible.
"""
        
        messages = [{
            "role": "user",
            "content": f"{system_prompt}\n\nSource Content:\n{concatenated_content}\n\nQuestion/Task: {prompt}"
        }]

        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=0,
            messages=messages
        )
        
        return response.content[0].text
    
    except (APIError, APIConnectionError, APITimeoutError) as e:
        print(f"Claude API error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='CLI tool to interact with Claude and GitHub repositories.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Config command
    subparsers.add_parser('config', help='Configure the Claude API key')
    
    # Clone command
    clone_parser = subparsers.add_parser('clone', help='Clone a GitHub repository into the sources directory')
    clone_parser.add_argument('repo_url', type=str, help='GitHub repository URL to clone')
    
    # Prompt command
    prompt_parser = subparsers.add_parser('prompt', help='Send a prompt to Claude with concatenated source directories')
    prompt_parser.add_argument('--src', action='append', required=True, help='Source directory to include in the prompt')
    prompt_parser.add_argument('prompt', type=str, help='Prompt text to send to Claude')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'config':
            save_api_key()
        
        elif args.command == 'clone':
            clone_repository(args.repo_url)
        
        elif args.command == 'prompt':
            concatenated_content = concatenate_sources(args.src)
            response = send_claude_prompt(concatenated_content, args.prompt)
            
            # Save response with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            response_filename = os.path.join(RESPONSES_DIR, f"claude_response_{timestamp}.txt")
            
            with open(response_filename, 'w', encoding='utf-8') as f:
                f.write('######## Sources:\n\n')
                f.write(', '.join(args.src) + '\n\n')
                f.write('######## Prompt:\n\n')
                f.write(args.prompt + '\n\n')
                f.write('######## Response:\n\n')
                f.write(response)
            
            print(response)
            print(f"\nResponse saved to: {response_filename}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()