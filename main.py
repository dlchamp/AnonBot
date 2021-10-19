import os
import nextcord
import logging
from buttons import Confirm
from nextcord.ext import commands
from dotenv import load_dotenv

# Basic logging config
logging.basicConfig(format="%(message)s", level="INFO")
log = logging.getLogger("root")

"""
Set discord intents - DO NOT CHANGE INTENTS
Initialize bot and configure presence activity
"""
intents = nextcord.Intents.default()
intents.dm_messages = True
intents.dm_reactions = True
intents.members = True
intents.reactions = True

## Configure Command Prefix ##
# Must be a string surrounded by ""
prefix = "!anon "

bot = commands.Bot(command_prefix=prefix, help_command=None,
                   case_insensitive=True, intents=intents)
activity = nextcord.Activity(
    type=nextcord.ActivityType.listening, name=f"{prefix}help")

"""
Start bot listening events
"""


@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.online, activity=activity)
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
    if isinstance(msg.channel, nextcord.channel.DMChannel) and msg.author != bot.user:
        log.info(f"Received message in DM")
        '''
        Split message into sections, get command at index 0, channel name or id at index 1 and user's message at index 2:
        '''
        resp_message = msg.content.split(" ")
        msg_command = resp_message[0].lower()
        msg_channel = resp_message[1].lower()
        user_msg = ' '.join(resp_message[2:])

        log.info("Checking for mutual guilds")
        if not msg.author.mutual_guilds:
            log.info('No mutual guilds found - sending DM to user')
            await msg.author.send("Sorry, we don't share a mutual discord server")
            pass
        else:
            if msg_command == "send":
                log.info('Getting channel from message')
                if msg_channel.startswith(('0','1','2','3','4','5','6','7','8','9')):
                    for guild in msg.author.mutual_guilds:
                        channel = bot.get_channel(int(msg_channel))
                        log.info(f'Found channel by ID')
                        view = Confirm()
                        embed = nextcord.Embed(title="Message Preview:", description=f'\n{user_msg}\n\nWould you like to send this message to {channel.name}?')
                        await msg.author.send(embed=embed, view=view)
                        await view.wait()

                        if view.value is None:
                            return
                        elif view.value:
                            log.info(f'User message sent to channel: {channel.name}')
                            await msg.author.send(f'Your message has been anonymously send to {channel.name}')
                            await channel.send(user_msg)
                        else:
                            log.info('User cancelled anonymous message')
                            await msg.author.send('Your message has been cancelled.')

                        if channel is None:
                            log.info(f'No channel found with ID: {msg_channel}')
                            await msg.author.send(f'Sorry. I could not find any channels with ID: {msg_channel}')
                else:
                    channel_dict = {}
                    for guild in msg.author.mutual_guilds:
                        for c in guild.channels:
                            channel_dict[c.name] = c.id

                    if not msg_channel in channel_dict:
                        log.info(f"No channel found with name: {msg_channel}")
                        await msg.author.send(f'Sorry. I could not find any channels named: {msg_channel}')
                    else:
                        channel = bot.get_channel(channel_dict[msg_channel])
                        log.info('Found channel by name')
                        view = Confirm()
                        embed = nextcord.Embed(title="Message Preview:", description=f'\n{user_msg}\n\nWould you like to send this message to {channel.name}?')
                        await msg.author.send(embed=embed, view=view)
                        await view.wait()

                        if view.value is None:
                            return
                        elif view.value:
                            log.info(f'User message sent to channel: {channel.name}')
                            await msg.author.send(f'Your message has been anonymously send to {channel.name}')
                            await channel.send(user_msg)
                        else:
                            log.info('User cancelled anonymous message')
                            await msg.author.send('Your message has been cancelled.')

                        if channel is None:
                            log.info(f'No channel found with ID: {msg_channel}')
                            await msg.author.send(f'Sorry. I could not find any channels with ID: {msg_channel}')

    # Required to allow bot to process commands while also monitoring on_message events
    await bot.process_commands(msg)


## Help Command ##
@bot.command(name="help")
async def help_command(ctx):
    # build embed
    embed = nextcord.Embed(
        title="Intro", description=f"{bot.user.name} allows you to send anonymous messages to a public channel. Even the logs are kept 100% anonymous.\n\nAll commands should be direct messaged to me. I will present a preview and wait for your confirmation before sending any messages to any channels.")
    embed.add_field(name="Direct Message Commands:",
                    value=f"**send (channel) (message)**\nSends an anonymous message to the specified channel.\n(*ex: send channel-name The juice is worth the squeeze.\n\n**{prefix}help**\n*(Can be used in any server channel)*\nDisplay this help message.")

    await ctx.send(embed=embed)


load_dotenv()
bot.run(os.environ["TOKEN"])
