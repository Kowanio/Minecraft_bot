import json
import discord
from discord.ext import commands


def search_item(item_name, item_data):
    for i in item_data:
        if item_name in [str(i['type']), str(i['type']) + ":" + str(i['meta']), i['name'], i['text_type']]:
            return i
    else:
        return {}


class Item(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='item')
    async def item(self, ctx, item_name):
        """Get data of Minecraft item"""
        path = "data/item.json"
        print(item_name)
        try:
            with open(path) as item_file:
                item_data = json.load(item_file)
                item = search_item(item_name, item_data)
                if item:
                    emb = discord.Embed(title=item['name'])
                    emb.add_field(name="id", value=str(item['type']) + ":" + str(item['meta']))
                    emb.add_field(name="text_type", value=item['text_type'])
                    await ctx.send(embed=emb)
                    with open("data/assets/items/{}.png".format(str(item['type']) + "-" + str(item['meta'])), "rb") as item_image:
                        file = discord.File(item_image, filename="item.png")
                        print(file.filename)
                        await ctx.send(file=file)
                else:
                    await ctx.send("Item not found")
        except FileNotFoundError:
            await ctx.send('Warning failed to load file {} : file does not exist'.format(path))
