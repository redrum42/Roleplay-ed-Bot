import disnake
import json

from disnake.ext import commands, tasks
from datetime import timedelta, datetime, date


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=disnake.Streaming(name="Best Boss in the World", url='https://www.youtube.com/watch?v=vaNpcgmj5qI'))

    @commands.slash_command(
        name="profile",
        description="Shows a users profile"
    )
    async def profile(self, ctx, member: disnake.Member = None):
        if not member:
            member = ctx.author
        data = await self.bot.fetchrow(
            "SELECT charcount, achievements FROM users WHERE user_id = ?",
            member.id
        )
        if data is None:
            await ctx.response.send_message("Member not registered yet", ephemeral=True)
            return
        count = data[0]
        a_list = json.loads(data[1])
        embed = disnake.Embed(
            description=f"**All time character count** : `{count}`",
            color=member.color
        )
        if member.avatar.url:
            embed.set_author(name=member.name, icon_url=member.avatar.url)
        else:
            embed.set_author(name=member.name)
        a = " "
        for achive in a_list:
            a += f"**`{achive}`**\n"
        if len(a) > 1:
            embed.add_field(name="Achievements -", value=a)
        await ctx.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
    print("[General] Loaded")
