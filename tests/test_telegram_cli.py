import os
import sys
import argparse
import time
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram import Bot
from telegram.error import TelegramError

class TelegramBotTester:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.updater = Updater(token=self.token, use_context=True)
        self.bot = self.updater.bot
        self.direct_chat_id = None
        self.test_results = []
        
        # Define command types
        self.simple_commands = {'start', 'help'}
        self.message_commands = {'p', 'prompt'}
        self.url_commands = {'preaudit'}

    def log_result(self, test_name, success, message=None):
        """Log test results"""
        result = "✅" if success else "❌"
        self.test_results.append((test_name, result, message))
        if message:
            print(f"{result} {test_name}: {message}")
        else:
            print(f"{result} {test_name}")

    def send_message(self, chat_id, message):
        """Send a message and return success status"""
        print(f"\n📤 Sending: {message}")
        try:
            self.bot.send_message(chat_id=chat_id, text=message)
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def run_test_suite(self, chat_id):
        """Run a complete test suite"""
        print(f"\n🧪 Starting test suite on chat ID: {chat_id}")
        
        # Test basic commands
        tests = [
            ("Start Command", "/start", None),
            ("Help Command", "/help", None),
            ("Basic Prompt", "/p", "Tell me about ApeWorX"),
            ("Long Prompt", "/prompt", "Explain the core features of Ape Framework"),
            ("Preaudit Command", "/preaudit", "https://github.com/ApeWorX/ape"),
        ]

        for test_name, command, arg in tests:
            message = f"{command} {arg}" if arg else command
            success = self.send_message(chat_id, message)
            self.log_result(test_name, success)
            time.sleep(2)  # Wait between messages

        # Print summary
        print("\n📊 Test Summary:")
        successful = sum(1 for _, result, _ in self.test_results if result == "✅")
        total = len(self.test_results)
        print(f"Passed: {successful}/{total} tests")
        
        return successful == total

    def send_command(self, chat_id, command, message=None):
        """Send a command with optional message"""
        if command in self.simple_commands:
            return self.send_message(chat_id, f"/{command}")
        elif command in self.message_commands or command in self.url_commands:
            if not message:
                print(f"❌ Error: {command} requires a message/URL")
                return False
            return self.send_message(chat_id, f"/{command} {message}")
        else:
            print(f"❌ Unknown command: {command}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Telegram Bot Test Suite')
    parser.add_argument('--chat-id', type=str, help='Chat ID to use')
    parser.add_argument('--command', choices=['start', 'help', 'p', 'prompt', 'preaudit'], 
                       help='Command to test')
    parser.add_argument('--message', type=str, help='Message for command (required for p, prompt, preaudit)')
    parser.add_argument('--suite', action='store_true', help='Run complete test suite')
    
    args = parser.parse_args()
    tester = TelegramBotTester()

    if not args.chat_id:
        print("❌ Please provide --chat-id")
        print("\nExample commands:")
        print("\n1. Run test suite:")
        print("   python tests/test_telegram_cli.py --suite --chat-id 1978731049")
        print("\n2. Test command with message:")
        print("   python tests/test_telegram_cli.py --chat-id 1978731049 --command p --message 'What is Ape?'")
        print("\n3. Test simple command:")
        print("   python tests/test_telegram_cli.py --chat-id 1978731049 --command start")
        return

    if args.suite:
        tester.run_test_suite(args.chat_id)
    elif args.command:
        success = tester.send_command(args.chat_id, args.command, args.message)
        tester.log_result(f"Command /{args.command}", success)
    else:
        print("\nPlease specify --suite or --command")
        print("\nExample: python tests/test_telegram_cli.py --chat-id 1978731049 --command start")

if __name__ == "__main__":
    main()