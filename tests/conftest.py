import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Chat, Message, User
from telegram.ext import CallbackContext
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "telegram: mark test as a telegram test")
    config.addinivalue_line("markers", "claude: mark test as a claude test")
    config.addinivalue_line("markers", "integration: mark as integration test")

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables"""
    load_dotenv()
    # Verify critical environment variables
    required_vars = ['TELEGRAM_TOKEN', 'CLAUDE_KEY']
    for var in required_vars:
        if not os.getenv(var):
            logger.warning(f"{var} is not set in environment")

@pytest.fixture
def telegram_token():
    """Get Telegram token"""
    return os.getenv('TELEGRAM_TOKEN')

@pytest.fixture
def claude_key():
    """Get Claude API key"""
    return os.getenv('CLAUDE_KEY')

@pytest.fixture
def test_chat_id():
    """Get test chat ID"""
    return 1978731049

@pytest.fixture
async def mock_message():
    """Create mock telegram message"""
    message = AsyncMock(spec=Message)
    message.chat = AsyncMock(spec=Chat)
    message.chat.id = 1978731049
    message.from_user = AsyncMock(spec=User)
    message.from_user.id = 67950696  # Default admin ID
    return message

@pytest.fixture
async def mock_update(mock_message):
    """Create mock telegram update"""
    update = AsyncMock(spec=Update)
    update.effective_chat = mock_message.chat
    update.message = mock_message
    return update

@pytest.fixture
async def mock_context():
    """Create mock context with bot"""
    context = AsyncMock(spec=CallbackContext)
    context.bot = AsyncMock()
    return context

@pytest.fixture
def mock_claude_response():
    """Create mock Claude API response"""
    response = MagicMock()
    response.content = [MagicMock(text="Test response")]
    return response

@pytest.fixture
def sample_knowledge_base():
    """Provide sample knowledge base content"""
    return """
    # Sample Ape Documentation
    Ape is a tool for smart contract development...
    """

@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for tests"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

# Helper fixtures for common test scenarios
@pytest.fixture
async def send_command(mock_update, mock_context):
    """Helper to simulate sending a command"""
    async def _send_command(command: str, *args):
        mock_update.message.text = f"/{command} {' '.join(args)}"
        return mock_update, mock_context
    return _send_command

@pytest.fixture
async def admin_context(mock_context):
    """Context with admin privileges"""
    mock_context.user_data = {'is_admin': True}
    return mock_context

@pytest.fixture
async def group_context(mock_context):
    """Context for group chat"""
    mock_context.chat_data = {'is_group': True, 'messages_today': 0}
    return mock_context

@pytest_asyncio.fixture(scope='function')
async def event_loop():
    """Create event loop"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

def pytest_configure(config):
    """Configure pytest"""
    # Add asyncio marker
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async"
    )