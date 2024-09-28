import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Define your bot token
BOT_TOKEN = '7546779723:AAGckCuFIhMfa9h7sUZylW_hQfa_0UsSL7I'

# Set up an external API (Weather API in this case)
WEATHER_API_KEY = 'your_openweathermap_api_key_here'  # Replace with your OpenWeatherMap API key

# Command to start the bot with credits to @f2wnet
async def start(update: Update, context) -> None:
    message = (
        "Hello! I am your advanced bot.\n"
        "You can send /weather <city> to get the current weather information.\n"
        "Bot created with ❤️ by @f2wnet."
    )
    await update.message.reply_text(message)

# Command to fetch weather from an external API
async def weather(update: Update, context) -> None:
    try:
        if len(context.args) == 0:
            await update.message.reply_text('Please provide a city name. Usage: /weather <city>')
            return
        
        city_name = ' '.join(context.args)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            await update.message.reply_text(f"City {city_name} not found!")
        else:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = (f"Weather in {city_name.title()}:\n"
                            f"Description: {weather_description}\n"
                            f"Temperature: {temperature}°C\n"
                            f"Feels like: {feels_like}°C\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind speed: {wind_speed} m/s\n"
                            f"\nBot created by @f2wnet.")
            await update.message.reply_text(weather_info)

    except Exception as e:
        await update.message.reply_text("An error occurred while fetching the weather data.")

# Command to handle any text message and echo it back with credits
async def echo(update: Update, context) -> None:
    user_message = update.message.text
    await update.message.reply_text(f'You said: {user_message}\n\nBot created by @f2wnet.')

# Command to handle unknown commands with credits
async def unknown(update: Update, context) -> None:
    await update.message.reply_text("Sorry, I didn't understand that command.\n\nBot created by @f2wnet.")

# Main function to run the bot
async def main():
    # Create the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers for commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('weather', weather))  # Advanced API command for weather

    # Add handler for text messages (echo)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Add handler for unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Run the bot
    await app.start()
    print("Bot is running...")
    await app.idle()

# Run the bot
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
