import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", -4718382612))  # Default to -4718382612 if not set

# Setup logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming messages and responds with '- claude' if in the target group.
    """
    chat_id = update.effective_chat.id
    message = update.message.text

    # Log the received message and its chat ID for debugging
    logging.debug(f"Received message: {message} | Chat ID: {chat_id}")

    # Check if the message is from the target group
    if chat_id != GROUP_ID:
        logging.info("Message is not from the target group. Ignoring.")
        return

    # Generate response and send it back
    response = f"{message} - claude"
    logging.debug(f"Sending response: {response}")
    try:
        await update.message.reply_text(response)
        logging.info("Response sent successfully!")
    except Exception as e:
        logging.error(f"Error sending response: {e}")

def main():
    """
    Initializes and runs the Telegram bot application.
    """
    # Ensure the bot token is provided
    if not TELEGRAM_TOKEN:
        logging.critical("TELEGRAM_TOKEN is missing. Please check your .env file.")
        return

    logging.info("Starting the echo bot...")
    logging.info(f"Target Group ID: {GROUP_ID}")

    # Create the bot application instance
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add a message handler to process text messages
    app.add_handler(MessageHandler(filters.TEXT, echo_message))

    # Start polling for updates
    logging.info("Bot is running and ready to receive messages.")
    try:
        app.run_polling(allowed_updates=["message"])
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.critical(f"Bot encountered an error: {e}")

if __name__ == "__main__":
    main()
