import pytest
from telegram import Bot
from telegram.error import TelegramError, Conflict, TimedOut
import os
from dotenv import load_dotenv
import logging
import time

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
            time.sleep(1)  # Wait for webhook deletion to take effect
        else:
            logger.info("✅ No webhook set")
        assert True  # Test passes if we can check webhook status
    except TelegramError as e:
        pytest.fail(f"Failed to check webhook: {e}")

def test_polling_status(telegram_bot):
    """Test for polling conflicts"""
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Try to get updates with longer timeout
            updates = telegram_bot.get_updates(
                timeout=3,
                offset=-1,  # Get only the latest update
                limit=1     # Limit to 1 update
            )
            logger.info("✅ No polling conflicts detected")
            # Test passes if we can get updates
            assert True
            return
        except TimedOut:
            if attempt < max_retries - 1:
                logger.warning(f"Timeout on attempt {attempt + 1}, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            else:
                logger.error("❌ All polling attempts timed out")
                pytest.fail("All polling attempts timed out")
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