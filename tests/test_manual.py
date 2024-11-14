import os
from anthropic import Anthropic
import argparse
from dotenv import load_dotenv

def test_claude_api():
    """Test Claude API connection and response"""
    print("\n📡 Testing Claude API connection...")
    
    client = Anthropic(api_key=os.getenv('CLAUDE_KEY'))
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": "Please respond with 'Hello, test successful!'"
            }]
        )
        print("✅ Claude API test successful!")
        print(f"Response: {response.content[0].text}")
    except Exception as e:
        print(f"❌ Claude API test failed: {str(e)}")

def test_telegram_token():
    """Test Telegram token validity"""
    print("\n🤖 Testing Telegram token...")
    
    import telegram
    try:
        bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
        bot_info = bot.get_me()
        print("✅ Telegram token valid!")
        print(f"Bot username: @{bot_info.username}")
    except Exception as e:
        print(f"❌ Telegram token test failed: {str(e)}")

def test_file_system():
    """Test file system setup"""
    print("\n📂 Testing file system setup...")
    
    required_dirs = ['sources', 'responses']
    required_files = ['requirements.txt', '.env']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' missing")
            os.makedirs(dir_name)
            print(f"  Created '{dir_name}' directory")

    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ File '{file_name}' exists")
        else:
            print(f"❌ File '{file_name}' missing")

def test_environment():
    """Test environment variables"""
    print("\n🔐 Testing environment variables...")
    
    required_vars = ['TELEGRAM_TOKEN', 'CLAUDE_KEY']
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
            if var == 'TELEGRAM_TOKEN':
                print(f"  Token: ...{os.getenv(var)[-10:]}")
            else:
                print(f"  Key: ...{os.getenv(var)[-10:]}")
        else:
            print(f"❌ {var} is not set")

def main():
    parser = argparse.ArgumentParser(description='Manual CLI testing tool')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--claude', action='store_true', help='Test Claude API')
    parser.add_argument('--telegram', action='store_true', help='Test Telegram token')
    parser.add_argument('--files', action='store_true', help='Test file system')
    parser.add_argument('--env', action='store_true', help='Test environment variables')
    
    args = parser.parse_args()

    # Load environment variables
    print("🔄 Loading environment variables...")
    load_dotenv()

    # If no specific tests are selected, run all tests
    if not (args.claude or args.telegram or args.files or args.env):
        args.all = True

    if args.all or args.env:
        test_environment()
    
    if args.all or args.files:
        test_file_system()
    
    if args.all or args.claude:
        test_claude_api()
    
    if args.all or args.telegram:
        test_telegram_token()

if __name__ == "__main__":
    main()