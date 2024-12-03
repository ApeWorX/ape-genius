import pytest
from telegram import Bot
from telegram.error import TelegramError, Conflict
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def telegram_bot():
    """Create telegram bot instance"""
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        pytest.skip("TELEGRAM_TOKEN not set")
    return Bot(token=token)

def test_bot_connection(telegram_bot):
    """Test if bot can connect to Telegram"""
    try:
        bot_info = telegram_bot.get_me()
        logger.info(f"✅ Connected to bot: @{bot_info.username}")
        assert bot_info.username is not None
    except TelegramError as e:
        pytest.fail(f"Failed to connect to Telegram: {e}")

def test_webhook_status(telegram_bot):
    """Test webhook configuration"""
    try:
        webhook_info = telegram_bot.get_webhook_info()
        if webhook_info.url:
            logger.warning(f"⚠️ Webhook found: {webhook_info.url}")
            # Clean up webhook
            telegram_bot.delete_webhook(drop_pending_updates=True)
            logger.info("✅ Webhook deleted")
        else:
            logger.info("✅ No webhook set")
        assert True  # Test passes if we can check webhook status
    except TelegramError as e:
        pytest.fail(f"Failed to check webhook: {e}")

def test_polling_status(telegram_bot):
    """Test for polling conflicts"""
    try:
        # Try to get updates with minimal timeout
        updates = telegram_bot.get_updates(timeout=1)
        logger.info("✅ No polling conflicts detected")
        assert updates is not None
    except Conflict as e:
        logger.error(f"❌ Polling conflict detected: {e}")
        pytest.fail(f"Polling conflict detected: {e}")
    except TelegramError as e:
        pytest.fail(f"Failed to check polling: {e}")

def test_environment():
    """Test environment setup"""
    token = os.getenv('TELEGRAM_TOKEN')
    assert token is not None, "TELEGRAM_TOKEN not set"
    assert token.strip() != "", "TELEGRAM_TOKEN is empty"
    logger.info("✅ Environment variables verified")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--log-cli-level=INFO"])