# ape-genius

The smartest ape in the jungle

## Runnig your own bot

### 1. Replace [`knowledge-base.txt`](./knowledge-base.txt) with your own knowledge-base

- Delete the existing .ext
- Add your stuff in [`knowledge-base`](./knowledge-base)
- Run `python concat.py` to compile the aboe folder into [`knowledge-base.txt`](./knowledge-base.txt) 

### 2. Set `OPENAI_API_KEY` and `TELEGRAM_TOKEN` environment variables.

- `OPENAI_API_KEY`: https://platform.openai.com/api-keys
- `TELEGRAM_TOKEN`: https://t.me/BotFather

### 3. Override [instructions](https://github.com/ApeWorX/ape-genius/blob/main/bot.py#L108) and [owner id](https://github.com/ApeWorX/ape-genius/blob/main/bot.py#L63) to fit your usage.

- You can find your owner id with https://t.me/username_to_id_bot

### 4. Run or deploy to cloud

- run locally with docker, or: `pip install -r "requirements.txt"` then `python bot.py`
- or deploy to cloud with https://fly.io: `flyctl deploy --ha=false` (atm the script only supports 1 machine, it's already configured like this)
- add bot in a group and use `/add_group groupid` to whitelist it and it's ready to use with `/prompt whatever you want`
