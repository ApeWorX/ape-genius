import pytest
from telegram import Update
from telegram.ext import ContextTypes
import logging
import pytest_asyncio
from unittest.mock import AsyncMock, patch
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# Now we can import from bot
from bot import start, handle_message, add_admin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
class TestTelegramBot:
    @pytest.fixture(autouse=True)
    async def setup(self):
        """Setup test fixtures"""
        self.chat_id = 1978731049
        self.update = AsyncMock(spec=Update)
        self.update.effective_chat.id = self.chat_id
        self.update.message = AsyncMock()
        self.update.message.chat.id = self.chat_id
        self.context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    async def test_start_command(self):
        """Test /start command"""
        self.update.message.text = "/start"
        await start(self.update, self.context)
        
        self.update.message.reply_text.assert_awaited_once_with(
            'Hello! Ask me anything about ApeWorX!'
        )

    async def test_prompt_command(self):
        """Test /p command"""
        self.update.message.text = "/p What is Ape?"
        # Mock group check
        with patch('bot.groups', {str(self.chat_id): {'messages_today': 0, 'last_reset': '2024-12-04'}}):
            await handle_message(self.update, self.context)
            
        assert self.update.message.reply_text.awaited

    async def test_group_chat(self):
        """Test group chat functionality"""
        # Setup group context
        self.update.message.chat.type = 'group'
        self.update.message.text = "/p Test message"
        
        # Mock group data
        with patch('bot.groups', {str(self.chat_id): {'messages_today': 0, 'last_reset': '2024-12-04'}}):
            await handle_message(self.update, self.context)
            assert self.update.message.reply_text.awaited

    @pytest.mark.parametrize("command,expected_text", [
        ("/start", "Hello! Ask me anything about ApeWorX!"),
        ("/p What is Ape?", None),
        ("/prompt Tell me about ApeWorX", None),
    ])
    async def test_commands(self, command, expected_text):
        """Test various commands"""
        self.update.message.text = command
        
        with patch('bot.groups', {str(self.chat_id): {'messages_today': 0, 'last_reset': '2024-12-04'}}):
            if command.startswith("/start"):
                await start(self.update, self.context)
                self.update.message.reply_text.assert_awaited_once_with(expected_text)
            else:
                await handle_message(self.update, self.context)
                assert self.update.message.reply_text.awaited

    async def test_message_limit(self):
        """Test message limit in groups"""
        # Mock group with max messages
        group_data = {str(self.chat_id): {'messages_today': 10, 'last_reset': '2024-12-04'}}
        
        with patch('bot.groups', group_data):
            await handle_message(self.update, self.context)
            self.update.message.reply_text.assert_awaited_with(
                'GPT limit for this group has been reached (10 msgs a day).'
            )

    async def test_admin_command(self):
        """Test admin command"""
        # Setup admin test
        self.update.message.from_user.id = 67950696  # Default admin ID
        self.context.args = ["12345"]
        
        await add_admin(self.update, self.context)
        self.update.message.reply_text.assert_awaited_with('Admin added successfully.')