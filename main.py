from pyrogram import Client, filters
from pymongo import MongoClient
from bson.json_util import dumps

# Bot configuration
API_ID = "29872536"  # Replace with your Telegram API ID
API_HASH = "65e1f714a47c0879734553dc460e98d6"  # Replace with your Telegram API Hash
BOT_TOKEN = "7835615149:AAGXYrwLqYYiXDBXSvGw_y0Mlk3-Gja_yg0"  # Replace with your Telegram bot token

# MongoDB configuration
MONGO_URL = "mongodb+srv://denji3494:denji3494@cluster0.bskf1po.mongodb.net/"
mongo_client = MongoClient(MONGO_URL)

# Initialize bot
bot = Client("mongoBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "Welcome! Use the following commands:\n"
        "- `/databases`: Show available database names.\n"
        "- `/getdata <collection_name>`: Fetch data from a MongoDB collection."
    )

@bot.on_message(filters.command("databases"))
async def show_databases(_, message):
    try:
        # Fetch the list of databases
        databases = mongo_client.list_database_names()
        if not databases:
            await message.reply_text("No databases found.")
        else:
            db_list = "\n".join(databases)
            await message.reply_text(f"Available Databases:\n`{db_list}`", parse_mode="markdown")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@bot.on_message(filters.command("getdata"))
async def get_data(_, message):
    try:
        # Extract collection name from the command
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Please provide the collection name. Usage: /getdata <collection_name>")
            return
        
        collection_name = command_parts[1]
        # Assume a default database name for this example
        db = mongo_client["your_database_name"]  # Replace with your database name
        collection = db[collection_name]
        
        # Fetch data from the collection
        documents = collection.find()
        data = [doc for doc in documents]
        
        if not data:
            await message.reply_text(f"No data found in the collection '{collection_name}'.")
            return
        
        # Convert data to JSON for readability
        json_data = dumps(data, indent=2)
        if len(json_data) > 4000:  # Telegram message size limit
            await message.reply_document(("data.json", json_data))
        else:
            await message.reply_text(f"Data from '{collection_name}':\n```{json_data}```", parse_mode="markdown")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    bot.run()
    
