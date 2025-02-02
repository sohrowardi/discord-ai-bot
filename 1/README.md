# Discord-AI-bot
A self-hostable chatbot for Discord that utilizes Ollama.

## Installation
1. [Install Ollama](https://ollama.com/download/)
2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
3. Open `config.toml` and enter your model and bot token.
4. Run the bot:
   ```sh
   python run.py
   ```
   - If you want the bot to work without being pinged/mentioned, use `runNoMention.py`:
     ```sh
     python runNoMention.py
     ```
   - If you want a simpler version without memories, use `runStable.py`:
     ```sh
     python runStable.py
     ```

## Usage
To use the bot, ping it via its username (e.g., `@bot`) or reply to it.

## Support
Discord support coming soon.

Any contributions to this project would be greatly appreciated.

## TODO
- Clean up the code
- Squash some bugs
- Add history "cleaning" (cleans past lines to save on storage, RAM, and VRAM)
