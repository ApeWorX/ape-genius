from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment
tg_token = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )
    
if __name__ == '__main__':
    # Create application
    application = ApplicationBuilder().token(tg_token).build()
    
    # Add handlers
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # Start bot
    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)