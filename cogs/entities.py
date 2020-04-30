import json
import discord
from discord.ext import commands


def search_entities(entities_name, entities_data):
    for i in entities_data:
        if entities_name in [str(i['type']), i['name'], i['text_type']]:
            return i
    else:
        return {}


class Entities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='entity')
    async def entities(self, ctx, entities_name):
        """Get data of Minecraft entity"""
        path = "data/entities.json"
        try:
            with open(path) as entities_file:
                entities_data = json.load(entities_file)
                entity = search_entities(entities_name, entities_data)
                if entity:
                    emb = discord.Embed(title=entity['name'])
                    emb.add_field(name="id", value=entity['type'])
                    emb.add_field(name="text_type", value=entity['text_type'])
                    await ctx.send(embed=emb)
                    with open("data/assets/entities/{}.png".format(str(entity['type'])), "rb") as item_image:
                        file = discord.File(item_image, filename="item.png")
                        print(file.filename)
                        await ctx.send(file=file)
                else:
                    await ctx.send("Entity not found")
        except FileNotFoundError:
            await ctx.send('Warning failed to load file {} : file does not exist'.format(path))