import telebot
import requests
from requests.auth import HTTPDigestAuth

# Bot token from BotFather
BOT_TOKEN = "7835615149:AAGXYrwLqYYiXDBXSvGw_y0Mlk3-Gja_yg0"

# MongoDB Atlas API credentials
ATLAS_PUBLIC_KEY = "fafcircg"
ATLAS_PRIVATE_KEY = "0749ff04-e266-443a-9375-8daeb3458b22"
ATLAS_PROJECT_ID = "6759ec4cb6ed924ed0c2ada5"
ATLAS_BASE_URL = f"https://cloud.mongodb.com/api/atlas/v1.0"

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Command: /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Welcome to the MongoDB Cluster Bot!\n"
        "Use /create_cluster <cluster_name> to create a new MongoDB cluster."
    )

# Command: /create_cluster
@bot.message_handler(commands=["create_cluster"])
def create_cluster(message):
    try:
        # Extract cluster name from the user's message
        parts = message.text.split(maxsplit=1)
        if len(parts) != 2:
            bot.reply_to(message, "Usage: /create_cluster <cluster_name>")
            return

        cluster_name = parts[1]

        # API request payload to create a cluster
        cluster_payload = {
            "name": cluster_name,
            "providerSettings": {
                "providerName": "AWS",  # Cloud provider (AWS, AZURE, GCP)
                "regionName": "US_EAST_1",  # AWS region
                "instanceSizeName": "M0",  # Free-tier cluster
            },
            "clusterType": "REPLICASET",
        }

        # Make the API request to create the cluster
        response = requests.post(
            f"{ATLAS_BASE_URL}/groups/{ATLAS_PROJECT_ID}/clusters",
            json=cluster_payload,
            auth=HTTPDigestAuth(ATLAS_PUBLIC_KEY, ATLAS_PRIVATE_KEY)
        )

        if response.status_code == 201:
            # Extract connection URL
            cluster_data = response.json()
            connection_string = cluster_data.get("connectionStrings", {}).get("standardSrv", "URL not available")
            bot.reply_to(message, f"✅ Cluster '{cluster_name}' created successfully!\nConnection URL:\n{connection_string}")
        else:
            error_msg = response.json().get("detail", "Unknown error")
            bot.reply_to(message, f"❌ Failed to create cluster. Error: {error_msg}")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
          
