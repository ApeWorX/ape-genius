import os
import logging
import hashlib
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CLAUDE_KEY = os.getenv('CLAUDE_KEY')
GROUP_ID = -4718382612  # ApeClaudeCouncil group

class KnowledgeBaseCache:
    _content = None
    _file_hash = None
    
    @classmethod
    def get_content(cls):
        """Get cached content or load from file if needed"""
        kb_path = Path("knowledge-base/all.txt")
        current_hash = hashlib.md5(kb_path.read_bytes()).hexdigest()
        
        if cls._content is None or current_hash != cls._file_hash:
            print("Loading knowledge base from file...")
            cls._content = kb_path.read_text(encoding='utf-8')
            cls._file_hash = current_hash
            print("Knowledge base loaded and cached")
        else:
            print("Using cached knowledge base")
            
        return cls._content

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    if update.effective_chat.id != GROUP_ID:
        return

    user_message = update.message.text
    print("\n" + "="*80)
    print(f"Received message: {user_message}")
    print("="*80)
    
    try:
        # Get cached knowledge base content
        knowledge_base = KnowledgeBaseCache.get_content()
        
        # Define system and user prompts
        system_prompt = """You are a technical assistant for ApeWorX, specializing in smart contract development and blockchain tooling.
Use ONLY the provided documentation to answer questions.
If the answer cannot be found in the documentation, say so clearly."""

        user_prompt = f"""Documentation:
{knowledge_base}

Question: {user_message}

Please provide a clear and specific answer based solely on the documentation provided."""

        print("\nPrompt being sent to Claude:")
        print("-"*40)
        print(user_prompt)
        print("-"*40)
        
        # Initialize Claude and get response
        client = anthropic.Anthropic(api_key=CLAUDE_KEY)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        claude_response = response.content[0].text
        print("\nClaude's response:")
        print("-"*40)
        print(claude_response)
        print("-"*40)
        
        # Send response back to group
        await update.message.reply_text(claude_response)
        print("\nResponse sent to Telegram group")
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"\nERROR: {error_msg}")
        await update.message.reply_text(f"❌ Error: {error_msg}")

def main():
    """Run the manual test bot"""
    print("\n" + "="*80)
    print("Starting manual test bot...")
    
    # Pre-load knowledge base into cache
    KnowledgeBaseCache.get_content()
    
    # Build application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("\nBot is running! 🚀")
    print("- Send any question to the ApeClaudeCouncil group")
    print("- Press Ctrl+C to stop")
    print("="*80 + "\n")
    
    # Start polling
    app.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"\nFatal error: {e}")