import os
import argparse
from typing import List, Dict
from anthropic import Anthropic, APIError, APIConnectionError, APITimeoutError

def load_knowledge_base(filepath: str) -> str:
    """Load knowledge base from file."""
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Knowledge base file '{filepath}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading knowledge base: {str(e)}")
        exit(1)

def create_messages(knowledge_base: str, question: str) -> List[Dict[str, str]]:
    """Create message structure for Claude API."""
    system_prompt = """
/- You are a bot helping people understand Ape.
/- The answer must exist within the source files, otherwise don't answer.
/- Do not invent anything about ape that is not in source files unless you said you were going creative.
/- False certainty about what ape can do is the worse thing you can do, avoid it at all costs.
/- ALWAYS Answer the user question using the source files and tell the source of your answer.
/- ALWAYS provide a % score of how much of your answer matches the KNOWLEDGE BASE.
/- If the task is of creative nature it's ok to go wild and beyond just the sources, but you MUST state that confidence score is -1 in that case.
"""
    return [{
        "role": "user",
        "content": f"{system_prompt}\n\nKnowledge Base:\n{knowledge_base}\n\nQuestion: {question}"
    }]

def query_claude(client: Anthropic, messages: List[Dict[str, str]], temperature: float = 0) -> str:
    """Send query to Claude API and handle errors."""
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=temperature,
            messages=messages
        )
        return response.content[0].text
    except (APIError, APIConnectionError, APITimeoutError) as e:
        print(f"Claude API error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Query Claude about ApeWorX')
    parser.add_argument('question', nargs='?', default=None, help='Question to ask Claude')
    parser.add_argument('-f', '--file', default='knowledge-base.txt', help='Path to knowledge base file')
    parser.add_argument('-t', '--temperature', type=float, default=0, help='Temperature for Claude response (0-1)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()

    # Initialize Claude client
    api_key = os.getenv('CLAUDE_KEY')
    if not api_key:
        print("Error: CLAUDE_KEY environment variable not set")
        exit(1)
    
    client = Anthropic(api_key=api_key)
    knowledge_base = load_knowledge_base(args.file)

    def process_question(question: str):
        """Process a single question and print response."""
        messages = create_messages(knowledge_base, question)
        response = query_claude(client, messages, args.temperature)
        print("\nClaude's Response:")
        print("-" * 80)
        print(response)
        print("-" * 80)

    if args.interactive:
        print("Interactive mode. Type 'exit' or 'quit' to end.")
        while True:
            question = input("\nEnter your question: ").strip()
            if question.lower() in ['exit', 'quit']:
                break
            if question:
                process_question(question)
    elif args.question:
        process_question(args.question)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()