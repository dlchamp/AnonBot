import os
import discord
import logging
from dotenv import load_dotenv

# Basic logging config
logging.basicConfig(format="%(message)s", level="INFO")
log = logging.getLogger("root")

"""
Set discord intents - DO NOT CHANGE DISCORD INTENTS
Initialize bot and configure presence activity
"""
intents = discord.Intents.default()
intents.dm_messages = True
intents.dm_reactions = True
intents.members = True
intents.reactions = True

bot = discord.Client(intents=intents)
activity = discord.Activity(
    type=discord.ActivityType.listening, name="for your DMs")

"""
Start bot listening events
"""


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=activity)
    log.info("Bot is online and ready!")

"""
When a message is sent in a guild channel or DM, the bot will check that it's
a DM message and move through the script.
First it splits the message content into sections to easily pull out the
"send" command, the "channel-name", and the "users-message"

Using the "channel-name" it will check if the user is in a mutal guild with the bot,
then it will iterate through all mutual guilds' channels to find a channel that matches
the user inputted "channel-name" once it does, it will find the ID for that channel.

If it fails, it will alert the user that no channels match the name provided.
If successful, it will generate a preview for the user and send a DM of this preview
showing intended channel, and the user's message contents to be sent.

Finally, it lets the user confirm or cancel the message
"""


@bot.event
async def on_message(msg):
    if isinstance(msg.channel, discord.channel.DMChannel) and msg.author != bot.user:
        log.info(f"Received message in DM")
        message = msg.content.split(" ")
        log.info("Checking for mutual guilds")
        if not msg.author.mutual_guilds:
            log.info('No mutual guilds found - sending DM to user')
            await msg.author.send("Sorry, we don't share a mutual discord server")
            pass
        else:
            # Get message content and split into sections for gathering variable data
            if msg.content.lower().startswith("send"):
                log.info('Getting user message contents')
                message = msg.content.split(" ")
                command = message[0]
                user_msg = " ".join(message[2:])
                # Get user mutual guilds, then find channel by name within those guilds
                for g in msg.author.mutual_guilds:
                    try:
                        log.info(f'Getting channels in {g.name} ')
                        for c in g.channels:
                            if c.name.lower() == message[1]:
                                msg_channel = bot.get_channel(c.id)
                                log.info(f'Found channel: {c.name}')
                    except:
                        log.info(f'Cannot find a channel called {message[1]}')
                        await msg.author.send(f"Sorry, I cannot find a channel called {message[1]}. Please check spelling and try again.  😊")
                        return
                # Checking reaction to ensure it's in a DM and not originating from the bot

                def r_check(reaction, user):
                    if isinstance(reaction.message.channel, discord.DMChannel):
                        return user == msg.author

                log.info(
                    'Sending message preview to user DM - awaiting confirmation')
                resp = await msg.author.send(
                    f"Received your message. Here is a preview!\n\n**Channel**:\n{message[1].lower()}\n\n**Message**:\n{user_msg}\n\nPlease react with ✅ to send or ❌ to cancel"
                )
                await resp.add_reaction("✅")
                await resp.add_reaction("❌")
                reaction, user = await bot.wait_for("reaction_add", check=r_check)

                if reaction.emoji == "✅":
                    log.info(
                        f'User confirmed message - sending to {msg_channel}')
                    await msg.author.send(f"Your message has been anonymously sent to {msg_channel}")
                    await msg_channel.send(user_msg)

                    return
                elif reaction.emoji == "❌":
                    log.info('User cancelled message - sleeping.')
                    await msg.author.send(
                        f"Your message has been cancelled.  You may try again if you wish")
                    return
            else:
                await msg.author.send("Sorry, I don't understand.  Please format your message correctly\n(ex. `send channel-name your-message`")
                log.info(
                    'Incorrectly formatted incoming message - directing user to try again')
    else:
        pass


load_dotenv()
bot.run(os.environ["TOKEN"])
