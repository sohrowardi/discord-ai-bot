# TODO: make it remember conversations for a more "human" feel.
# maybe i could use SQLite or Redis for this..

# import everything
import discord
import ollama
import requests
import json
import sqlite3

# api info for ollama
TOKEN = '' # dont share this with anyone
API_URL = 'http://localhost:11434/api/generate'

# set what the bot is allowed to listen to
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
client = discord.Client(intents=intents)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (user_id TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# Function to get conversation history
def get_conversation_history(user_id):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('SELECT message FROM conversations WHERE user_id = ?', (user_id,))
    messages = c.fetchall()
    conn.close()
    return [msg[0] for msg in messages]

# Function to store a message in the conversation history
def store_message(user_id, message):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('INSERT INTO conversations (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()
    conn.close()

# Function to send a request to the Ollama API and get a response
def generate_response(prompt, user_id):
    history = get_conversation_history(user_id)
    full_prompt = "\n".join(history + [prompt])
    data = {
        "model": "llama2-uncensored",  # Adjust this if you want to use a different model
        "prompt": full_prompt,
	"stream": False
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("response", "Sorry, I couldn't generate a response.")
    else:
        return "There was an error with the API."

# When the bot is ready
@client.event
async def on_ready():
    init_db()
    print(f'Logged in as {client.user}')

# When the bot detects a new message
@client.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == client.user:
        return

    # Check if the bot was mentioned
    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@!{client.user.id}>", "").strip()  # Remove the mention part
        if prompt:
            response = generate_response(prompt, str(message.author.id))
            store_message(str(message.author.id), prompt)
            store_message(str(message.author.id), response)
            await message.channel.send(response)
        else:
            await message.channel.send("bing bop boom boom boom bop bam")

# Run the bot
client.run(TOKEN)