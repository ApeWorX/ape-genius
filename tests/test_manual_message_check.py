import os
import logging
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    if update.effective_chat.id != GROUP_ID:
        return

    message_text = update.message.text.lower()
    logger.info(f"Received message: {message_text}")

    if "what is apeworx" in message_text:
        logger.info("Processing 'what is apeworx' query...")
        
        try:
            # Get knowledge base content
            kb_path = Path("knowledge-base/all.txt")
            knowledge_base = kb_path.read_text(encoding='utf-8')
            
            # Initialize Claude
            client = anthropic.Anthropic(api_key=CLAUDE_KEY)
            
            # Get response from Claude
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": f"""Based on this documentation:
                    {knowledge_base}
                    
                    Question: What is ApeWorX?
                    
                    Please provide a concise explanation."""
                }]
            )
            
            # Send response back to group
            await update.message.reply_text(response.content[0].text)
            logger.info("Response sent successfully")
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg)
            await update.message.reply_text(error_msg)

def main():
    """Run the manual test bot"""
    logger.info("Starting manual test bot...")
    
    # Build application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot is running. Send 'what is apeworx' to the ApeClaudeCouncil group...")
    logger.info("Press Ctrl+C to stop")
    
    # Start polling
    app.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")