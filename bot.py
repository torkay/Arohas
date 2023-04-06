import discord
from discord.ext import commands
import command
from keep_alive import keep_alive
import asyncio
import os

statusNotify_list = []

async def check_server_status():
    previousCycle = None  # Initialize previousCycle
    while True:
        wizStatus = command.check.serverStatus()

        # Detect change in status
        if previousCycle is not None and wizStatus != previousCycle:
            if wizStatus == False:
                for user_id in statusNotify_list:
                    user = bot.get_user(user_id)
                    if user is not None:
                        await user.send("🔴 Wizard101 servers are down!")

            if wizStatus == True:
                for user_id in statusNotify_list:
                    user = bot.get_user(user_id)
                    if user is not None:
                        await user.send("🟢 Wizard101 servers are back up!")

        previousCycle = wizStatus
        await asyncio.sleep(300) # Wait for 5 minutes before checking again



bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = 965232170933288970  # Change to your discord id!!!


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Try out !commands"))
    # Start the coroutine to periodically check server status
    await check_server_status()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!test'):
        await message.channel.send('This is a test message.')

    if message.content == "!status":
        status = command.check.serverStatus()
        response = ""
        if status == True:
            response = "🟢 Wizard101 seems to have its servers **up and running** 🙂"
        elif status == False:
            response = '''🔴 Wizard101 seems to have its servers **offline** at the moment 🙁
**Tip:** If you'd like for me to ping you when they're back up, type '!notifystatus' '''
        else:
            response = "Hmm... something went wrong during my checks, I'll let my developer know immediately"
        await message.channel.send(response)
      
    if message.content == '!notifystatus':
        user_id = message.author.id
        if message.content == '!notifystatus':
            user_id = message.author.id
            if user_id in statusNotify_list:
                statusNotify_list.remove(user_id)
                await message.channel.send(f"🔕 You have been **removed** from the notify list, {message.author.mention}")
            else:
                statusNotify_list.append(user_id)
                await message.channel.send(f"🔔 You have been **added** to the notify list, {message.author.mention}")

    if message.content == "!commands":
        await message.channel.send(f'''Here's a **complete list of commands,** {message.author.mention} 🙂

1️⃣ **!status**
Check on the status of Wizard101's servers

2️⃣ **!notifyStatus**
I'll ping with every Wizard101 server status change

3️⃣ **!wiki**
Quickly pull up a Wizard101 wiki link to anything you ask for. Try '!wiki Zafaria quest line'

4️⃣ **!find**
Find where you are with your quests, simply just type in the name of your quest. Try '!find Elephant March' ''')

    if message.content.startswith('!wiki'):
        input_string = message.content.split('!wiki ')[1]
        input_string = input_string.replace(' ', '-')
        url = 'https://www.wizard101central.com/wiki/Wizard101_Wiki:GoogleSearch?q=' + input_string
        await message.channel.send(f'''I found this on the Wizard101 Wiki, hope it helps 🙏
➡️ {url}''')

    if message.content.startswith('!find'):
        input_string = message.content.split('!find ')[1]
        await command.check.quest(message, input_string)


extensions = [
    'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.

    keep_alive()  # Starts a webserver to be pinged.
    token = os.environ.get("DISCORD_BOT_SECRET")
    bot.run(token)  # Starts the bot
