import requests
import json
import base64
import discord
from discord.ext import commands
from datetime import datetime


class Mojang(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='status')
    async def status(self, ctx):
        """Get the current status of Mojang and Minecraft services"""
        r = requests.get(url="https://status.mojang.com/check")
        server_state_data = r.json()
        emb = discord.Embed(title="Mojang server status")
        for i in server_state_data:
            emb.add_field(name=list(i.keys())[0], value=":{}_circle:".format(list(i.values())[0]), inline=False)
        await ctx.send(embed=emb)

    @commands.command(name='player')
    async def player(self, ctx, player_name: str):
        """Get player skin and current information"""
        r = requests.post(url="https://api.mojang.com/profiles/minecraft", json=player_name)
        player_data = r.json()
        if not player_data:
            await ctx.send("Player not found")
        else:
            r = requests.get(
                url="https://sessionserver.mojang.com/session/minecraft/profile/{}".format(player_data[0]['id']))
            request_data = r.json()
            skin_data = json.loads(base64.b64decode(request_data["properties"][0]['value']))
            emb = discord.Embed(title=skin_data['profileName'])
            emb.add_field(name="Profile id", value="{}".format(skin_data['profileId']))
            try:
                emb.set_image(url=skin_data['textures']['SKIN']['url'])
            except KeyError:
                pass
            await ctx.send(embed=emb)

    @commands.command(name='pseudo')
    async def pseudo(self, ctx, player_name: str):
        """Get name history for a player"""
        r = requests.post(url="https://api.mojang.com/profiles/minecraft", json=player_name)
        player_data = r.json()
        if not player_data:
            await ctx.send("Player not found")
        else:
            r = requests.get("https://api.mojang.com/user/profiles/{}/names".format(player_data[0]['id']))
            pseudo_data = r.json()
            emb = discord.Embed(title="History of {}".format(player_name))
            for i in pseudo_data[-15:]:
                try:
                    emb.add_field(name=i['name'], value="{}".format(
                        datetime.fromtimestamp(i['changedToAt'] // 1000).strftime("%d/%m/%Y %H:%M:%S")), inline=False)
                except KeyError:
                    emb.add_field(name=i['name'], value="Initial pseudonym", inline=False)
            await ctx.send(embed=emb)