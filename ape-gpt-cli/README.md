# ape-gpt

The `ape-gpt` CLI tool facilitates interactions between GPT (Generative Pre-trained Transformer) models and GitHub repositories. It streamlines the process of cloning repositories, managing your OpenAI API key, and sending prompts to GPT using the contents of the cloned repositories.

## Installation

To get started with `ape-gpt`, follow these steps:

1. Clone the `ape-gpt` repository to your local machine.
2. Install the required Python dependencies by executing `pip install -r requirements.txt` in your terminal.

## Usage

### Configuring the OpenAI API Key

Set up your OpenAI API key with `ape-gpt` by running:

```
python gpt.py config
```

You will be prompted to enter your OpenAI API key, which will be stored securely for future use.

### Cloning a GitHub Repository

Clone a GitHub repository into the local `sources` directory with the following command:

```
python gpt.py clone <repository-url>
```

### Sending a Prompt to GPT

Send a custom prompt to GPT using the content from one or more specified source directories:

```
python gpt.py prompt --src "source_directory1" --src "source_directory2" "Your prompt text"
```

The GPT response will be displayed in the terminal and also saved within the `responses` directory for your reference.

## Organization

- Cloned repositories are stored in the `sources` directory.
- GPT responses are saved in the `responses` directory.