import pytest

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers",
        "telegram: mark test as a telegram test"
    )

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables"""
    from dotenv import load_dotenv
    load_dotenv()