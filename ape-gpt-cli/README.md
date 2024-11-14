# ApeGenius

A CLI tool that facilitates interactions between AI language models (GPT and Claude) and GitHub repositories, designed specifically for analyzing and understanding Ape Framework codebases. It streamlines the process of cloning repositories, managing API keys, and sending prompts using the contents of cloned repositories.

## Features

- Support for both GPT-4 and Claude
- Secure API key management
- GitHub repository cloning
- Source code analysis optimized for Ape Framework
- Response logging and tracking
- Command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ApeWorX/apegenius.git
cd apegenius
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GPT Commands

Configure OpenAI API key:
```bash
python gpt.py config
```

Clone a repository:
```bash
python gpt.py clone 
```

Send a prompt:
```bash
python gpt.py prompt --src "source_directory" "Your prompt text"
```

### Claude Commands

Configure Claude API key:
```bash
python claude.py config
```

Clone a repository:
```bash
python claude.py clone 
```

Send a prompt:
```bash
python claude.py prompt --src "source_directory" "Your prompt text"
```

### Multiple Source Directories

Both tools support analyzing multiple source directories in a single prompt:
```bash
python gpt.py prompt --src "dir1" --src "dir2" "Your prompt"
python claude.py prompt --src "dir1" --src "dir2" "Your prompt"
```

## Project Structure

```
apegenius/
├── gpt.py           # GPT interface
├── claude.py        # Claude interface
├── requirements.txt # Project dependencies
├── sources/         # Cloned repositories
└── responses/       # AI responses
```

## Response Storage

All responses are automatically saved in the `responses` directory with the following information:
- Source directories used
- Original prompt
- AI response
- Timestamp

## Configuration

- API keys are stored securely using base64 encoding
- GPT config: `gpt_config.yml`
- Claude config: `claude_config.yml`

## Example Usage

1. Set up API keys:
```bash
python gpt.py config    # For GPT
python claude.py config # For Claude
```

2. Clone the Ape repository:
```bash
python gpt.py clone https://github.com/ApeWorX/ape.git
```

3. Analyze the code:
```bash
python claude.py prompt --src "ape" "Explain the main functionality of this Ape codebase"
```

## Requirements

- Python 3.8+
- Git
- OpenAI API key (for GPT)
- Anthropic API key (for Claude)
- Required Python packages (see requirements.txt)

## Error Handling

Both tools include robust error handling for:
- Invalid API keys
- Repository cloning issues
- File reading errors
- API rate limits
- Network connectivity issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to the [ApeGenius repository](https://github.com/ApeWorX/apegenius).

## License

[Apache License 2.0](LICENSE)

## Support

For issues and feature requests, please open an issue on the [ApeGenius GitHub repository](https://github.com/ApeWorX/apegenius/issues).