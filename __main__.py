import json
import discord
from discord.ext import commands, tasks
import cogs


async def on_ready():
    print("We have logged")


def check_config(config):
    if config["discord_bot"]["token"] == "":
        print("Failed to load configuration parameter token is empty")
        return 1
    if config['discord_bot']['prefix'] == "":
        config['discord_bot']['prefix'] = "$"
    if config['discord_bot']['description'] == "":
        config['discord_bot']['prefix'] = "no description"
    if config['feed']['activated'] and config['feed']['feed_url'] == "":
        print("Failed to load configuration parameter feed_url is empty")
        return 1
    return 0


def load_config():
    path = "config/config.json"
    config = {}
    try:
        with open(path) as config_file:
            config_data = json.load(config_file)
            config['discord_bot'] = {
                "token": config_data['discord_bot']['token'],
                "prefix": config_data['discord_bot']['prefix'],
                "description": config_data['discord_bot']['description']
            }
            config['feed'] = {
                "feed_channel": config_data['feed']['feed_channel'],
                "feed_url": config_data['feed']['feed_url'],
                "activated": config_data['feed']['activated']
            }
            if check_config(config):
                return {}
            else:
                return config
    except FileNotFoundError as e:
        print('Warning failed to load file {} : file does not exist'.format(path))
    except KeyError as e:
        print('Warning failed to load config from {}: please consult readme'.format(path))
        return {}


def main():
    config = load_config()
    if not config:
        exit(1)
    else:
        bot = commands.Bot(command_prefix=config['discord_bot']['prefix'],
                           description=config['discord_bot']['description'])
        if config['feed']['activated']:
            bot.add_cog(cogs.Feed(bot, config['feed']))
        bot.add_cog(cogs.Entities(bot))
        bot.add_cog(cogs.Item(bot))
        bot.add_cog(cogs.Mojang(bot))
        bot.add_listener(on_ready)
        try:
            bot.run(config['discord_bot']['token'])
        except discord.LoginFailure as e:
            print("Login failure {}".format(e))
            exit(1)


if __name__ == '__main__':
    main()
