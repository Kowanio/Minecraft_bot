import feedparser
from discord.ext import commands, tasks


class Feed(commands.Cog):
    config = {}

    def __init__(self, bot, config):
        self.bot = bot
        Feed.config = config
        self.feed.start()

    def cog_unload(self):
        self.feed.cancel()

    @tasks.loop(minutes=1.0)
    async def feed(self):
        feed = feedparser.parse(self.config['feed_url'])
        if hasattr(feed, 'old_entry'):
            if not feed['old_entry'] == feed.entries[0].link:
                feed['old_entry'] = feed.entries[0].link
                channel = self.bot.get_channel(self.config['feed_channel'])
                await channel.send(feed["old_entry"])
        else:
            feed["old_entry"] = feed.entries[0].link

    @feed.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()