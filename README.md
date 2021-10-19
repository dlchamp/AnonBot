# AnonBot

A Discord bot written using Nextcord's Python wrapper for Discord.   
This bot simply anonymously relays a user submitted message to a public server channel.
It is 100% anonymous, as even the log only provides as much as the channel name.  No user information is saved or displayed anywhere.



## Using the bot
* `!anon help` will display the help command explaining what the bot does and how to use it
* Simply DM the bot with `send channel-name message` to have your message anonymously sent.
*Please note that `channel-name` can also be a `channel-id` (ex. 78957513587965488)*
* Once the message has been sent to the bot, it will build a preview and ask you to confirm or cancel that message using Discord's new Buttons


### Dependencies

* Built on the latest [Python3](https://www.python.org/downloads/)
* see requirements.txt for Python dependencies (`pip install -r requirements.txt` to install dependencies automatically)
* Have Python installed on your host machine

## Getting Started

**Setting up Discord Bot**
1. Login to Discord web - https://discord.com
2. Navigate to Discord Developer Portal - https://discord.com/developers/applications
3. Click *New Application*
4. Give the Appplication a name and *Create*
5. Add image for Discord icon, you may also add a description
6. Go to Bot tab and click *Add Bot*
7. Be sure to enable SERVER MEMBERS INTENT under **Privileged Gateway Intents** (it is required for DMs to work)
8. Add bot image
9. Copy Token and paste it in .env-sample, save, then rename `.env-sample` to `.env`
10. Go to OAuth2 tab
11. Under *Scopes* - Check Bot
12. Under *Bot Permissions* - check Send messages and View Channels
13. Copy the generated link and Go to the URL in your browser - Invite Bot to your Discord server
14. At this point the bot is configured and ready to use.  




