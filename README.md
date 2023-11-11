# ape-genius

The smartest ape in the jungle

## Runnig your own bot

### 1. Replace [`knowledge_base.txt`](./knowledge_base.txt) with your own knowledgebase

Here is a handy python function that can help you take an entire repo and concatenate all files in a single .txt with all files contents and paths:

```python
# Function to concatenate files into a single .txt file
def concatenate_files(dir_name, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                if file.endswith('.lock'): # Ignore large files that adds nothing to overall knowledge
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        output_file.write('######## ' + file_path + '\n\n')
                        output_file.write(f.read() + '\n\n')
                except Exception as e:
                    print(f"Skipping non-text file or error reading file: {file_path} - {e}")

# Example Call
concatenate_files(dir_name, 'knowledge_base.txt')
```

### 2. Set `OPENAI_API_KEY` and `TELEGRAM_TOKEN` environment variables.

- `OPENAI_API_KEY`: https://platform.openai.com/api-keys
- `TELEGRAM_TOKEN`: https://t.me/BotFather

### 3. Override [instructions](https://github.com/ApeWorX/ape-genius/blob/main/bot.py#L108) and [owner id](https://github.com/ApeWorX/ape-genius/blob/main/bot.py#L63) to fit your usage.

- You can find your owner id with https://t.me/username_to_id_bot

### 4. Run or deploy to cloud

- run locally: `python bot.py`
- or deploy to cloud with https://fly.io: `flyctl deploy --ha=false` (atm the script only supports 1 machine, it's already configured like this)
