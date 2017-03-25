import game
import player
import discord
import asyncio
import json
import os

if os.path.exists('config.json'):
    with open('config.json','r') as configs:
        configs = json.load(configs)

bot_token = configs['discord']['token']
bot_trigger = configs['discord']['trigger']
bot_description = "Spyfall"

game = game.Game()
bot = discord.Client()

@bot.event
async def on_ready():
    print("Bot User-Name: %s" % bot.user)
    print("Bot User-ID: %s" % bot.user.id)
    print("--------------------")

def embeded_message(role, location):
    if role == "Spy":
        title = "Spyfall - Game"
        content = "Your Role is ---> **SPY** \n The Location is ---> *NOTGIVEN*"
        return discord.Embed(title=title, description=content)
    elif role != "Spy":
        title = "You are not the **Spy**"
        content = "Your role is ---> **%s** \nThe location is ---> *%s*" % (role, location)
        return discord.Embed(title=title, description=content)
@bot.event
async def on_message(message):
    message_delete = message
    message_author = message.author
    message_author_id = message.author.id
    message_channel = message.channel
    message_content = message.content.lower()


    if message_content.startswith(bot_trigger + 'join'):
        game.join_player(message_author_id)
        await bot.send_message(message.channel, "<@%s> has joined the game." % message_author_id)

        print(message_author)

        print(game.players)
    if message_content.startswith(bot_trigger + 'leave'):
        game.leave_player(message_author_id)
        await bot.send_message(message.channel, "<@%s> has left the game." % message_author_id)

        print(game.players)
    if message_content.startswith(bot_trigger + 'startgame'):
        game.start_game()
        for player in game.players:
            await bot.send_message(discord.User(id=player.name), embed=embeded_message(player.role, game._game_data['locations'][game.location]['Location']))
bot.run(bot_token)
