import disnake
import os
import json
import random
import asyncio

from disnake.ext import commands, tasks
from datetime import timedelta, datetime, date


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    Type = commands.option_enum(
        {
            "AllTime": "charcount",
            "Daily": "dailycount",
            "Weekly": "weeklycount",
            "Monthly": "monthlycount"
        }
    )

    @commands.slash_command(
        name="leaderboard",
        description="Shows the Character Count Leaderboard"
    )
    async def leaderboard(self, ctx, type: Type):
        if type == "charcount":
            users_data = await self.bot.fetchmany(
                "SELECT user_id, charcount, dailycount, weeklycount, monthlycount FROM users ORDER BY charcount DESC", 10
            )
            m = ('\n'.join(f"**#{n+1}** <@{data[0]}> | **Characters** : **`{data[1]}`**"
                           for n, data in enumerate(users_data)))
            t = "All Time count"

        elif type == "dailycount":
            users_data = await self.bot.fetchmany(
                "SELECT user_id, dailycount FROM users ORDER BY dailycount DESC", 10
            )
            m = ('\n'.join(f"**#{n+1}** <@{data[0]}> | **Characters** : **`{data[1]}`**"
                           for n, data in enumerate(users_data)))
            t = "Daily count"

        elif type == "weeklycount":
            users_data = await self.bot.fetchmany(
                "SELECT user_id, weeklycount FROM users ORDER BY weeklycount DESC", 10
            )
            m = ('\n'.join(f"**#{n+1}** <@{data[0]}> | **Characters** : **`{data[1]}`**"
                           for n, data in enumerate(users_data)))
            t = "Weekly count"

        elif type == "monthlycount":
            users_data = await self.bot.fetchmany(
                "SELECT user_id, monthlycount FROM users ORDER BY monthlycount DESC", 10
            )
            m = ('\n'.join(f"**#{n+1}** <@{data[0]}> | **Characters** : **`{data[1]}`**"
                           for n, data in enumerate(users_data)))
            t = "Monthly count"

        embed = disnake.Embed(
            description=f"Top **{len(users_data)} {t}**",
            color=disnake.Color(0x25c0e2),
            timestamp=datetime.now()
        )
        #embed.set_thumbnail(url=ctx.guild.icon.url)

        fields = []
        fields.append(("Count", m))

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        await ctx.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Leaderboard(bot))
    print("[Leaderboard] Loaded")
