import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROUP_ID = -4718382612  # Replace with your actual group ID

# Setup logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the message back with '- claude' suffix if it's in the target group"""
    chat_id = update.effective_chat.id
    message = update.message.text
    
    # Debugging: Log chat ID and received message
    logging.debug(f"Chat ID: {chat_id}, Message: {message}")
    
    if chat_id != GROUP_ID:
        logging.info("Message not from the target group. Ignoring.")
        return

    response = f"{message} - claude"
    logging.debug(f"Sending response: {response}")
    
    try:
        await update.message.reply_text(response)
        logging.info("Response sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send response: {e}")

def main():
    """Run the echo bot"""
    if not TELEGRAM_TOKEN:
        logging.critical("TELEGRAM_TOKEN is missing. Please check your .env file.")
        return

    logging.info("Starting the echo bot...")
    logging.info(f"Target group ID: {GROUP_ID}")
    
    # Create application instance
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    logging.info("Bot is running! Send messages to the group for testing.")
    try:
        app.run_polling(allowed_updates=["message"])
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.critical(f"Bot encountered an error: {e}")

if __name__ == '__main__':
    main()
