import os
import logging
from pathlib import Path
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

def load_knowledge_base():
    """Load the knowledge base content"""
    try:
        kb_path = Path("knowledge-base/all.txt")
        return kb_path.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error loading knowledge base: {e}")
        raise

def test_claude_queries():
    """Test Claude's responses to various queries"""
    
    # Initialize Claude
    client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_KEY'))
    
    # Load knowledge base
    logger.info("Loading knowledge base...")
    knowledge_base = load_knowledge_base()
    logger.info("Knowledge base loaded successfully")

    # Test queries
    test_queries = [
        "What is ApeWorX?",
        "Write a simple Silverback bot",
        "How do I deploy a smart contract with Ape?",
    ]

    system_prompt = """You are a technical assistant for ApeWorX, specializing in smart contract development and blockchain tooling.
Use ONLY the provided documentation to answer questions.
If the answer cannot be found in the documentation, say so clearly."""

    for query in test_queries:
        print("\n" + "="*80)
        print(f"\nTesting query: {query}")
        print("="*80)

        try:
            # Construct full prompt
            full_prompt = f"""Documentation:
{knowledge_base}

Question: {query}

Please provide a clear and specific answer based solely on the documentation provided."""

            print("\nPrompt sent to Claude:")
            print("-"*40)
            print(full_prompt)
            print("-"*40)

            # Get Claude's response using correct message structure
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                temperature=0,
                system=system_prompt,  # System prompt goes here
                messages=[
                    {"role": "user", "content": full_prompt}  # Only user message in the messages array
                ]
            )

            print("\nClaude's response:")
            print("-"*40)
            print(response.content[0].text)
            print("-"*40)

        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    print("\nStarting Claude test...")
    try:
        test_claude_queries()
        print("\nTest completed")
    except Exception as e:
        print(f"\nTest failed: {e}")