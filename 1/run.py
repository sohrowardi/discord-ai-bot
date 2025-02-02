# import everything
import requests
import json
import discord
import tomllib
import ollama
import os # Don't panic!!! This is used to save the history file to the computer!


# LOAD VARIABLES FROM config.toml
with open("config.toml", 'rb') as f:  # load config as f (f is short for file im just using slang, chat)
    config_data = tomllib.load(f)

# api info for ollama
TOKEN = config_data['discord']['token']  # Load token from config file
API_URL = 'http://localhost:11434/api/chat'

# Define the path for the conversation history file
HISTORY_FILE_PATH = "history.json"

# Load conversation history from a file if it exists
def load_conversation_history():
    if os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'r') as file:
            return json.load(file)
    return []

# Save conversation history to a file
def save_conversation_history():
    with open(HISTORY_FILE_PATH, 'w') as file:
        json.dump(conversation_history, file)

# Store conversation history in a list
conversation_history = load_conversation_history()

# set what the bot is allowed to listen to
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
client = discord.Client(intents=intents)


# Function to send a request to the Ollama API and get a response
def generate_response(prompt):
    conversation_history.append({
        "role": "user",
        "content": prompt
    })
    save_conversation_history()

    data = {
        "model": config_data['ollama']['model'],
        "messages": conversation_history,
        "stream": False
    }

    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        response_data = response.json()
        assistant_message = response_data['message']['content']

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        save_conversation_history()

        return assistant_message
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "There was an error with the API."
    except json.JSONDecodeError:
        return "Error: Invalid API response"


# When the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


# When the bot detects a new message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@!{client.user.id}>", "").strip()
        if prompt:
            try:
                async with message.channel.typing():
                    response = generate_response(prompt)
                    await message.channel.send(response)
            except discord.errors.Forbidden:
                print(f"Error: Bot does not have permission to type in {message.channel.name}")


# Run the bot
client.run(TOKEN)
