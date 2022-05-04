import disnake
import json

from disnake.ext import commands, tasks
from datetime import timedelta, datetime, date

CATEGORY = [923748324530585640,  # Magic and Books
            923439155768352818,  # Starters
            923413738869116971,  # One on One
            924303481580445696,   # One on One Contro
            938913777489940580,   # 1:1 HZ Controversial
            938177831991668776]    # Mutanverse

ACHIEVEMENTS = [10000, 100000, 500000, 1000000, 10000000]


class CharCount(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reset_time = datetime.strptime("00:05:00", "%H:%M:%S").time()

        if not self.count_check.is_running():
            self.count_check.start()

    def cog_unload(self):
        self.count_check.cancel()

# //////////////////////////////////////// #

    @tasks.loop(seconds=60)
    async def count_check(self):
        timenow = datetime.utcnow()
        refresh_time = datetime.combine(timenow.date(), self.reset_time)

        if 60 > (timenow-refresh_time).total_seconds() >= 0:

            users_data = await self.bot.fetchmany(
                "SELECT user_id, dailycount FROM users ORDER BY dailycount DESC", 3
            )
            m = ('\n'.join(f"<@{data[0]}> ended up **`#{n+1}`** with **`{data[1]}`** characters"
                           for n, data in enumerate(users_data)))
            channel = self.bot.get_channel(924757636417748992)
            await channel.send(f"**Daily Winners!**\n {m}")

            await self.bot.execute(
                "UPDATE users SET dailycount = 0"
            )

            if timenow.weekday() == 6:

                users_data = await self.bot.fetchmany(
                    "SELECT user_id, weeklycount FROM users ORDER BY weeklycount DESC", 3
                )
                m = ('\n'.join(f"<@{data[0]}> ended up **`#{n+1}`** with **`{data[1]}`** characters"
                               for n, data in enumerate(users_data)))
                channel = self.bot.get_channel(924757636417748992)
                await channel.send(f"**Weekly Winners!**\n {m}")

                await self.bot.execute(
                    "UPDATE users SET weeklycount = 0"
                )

            if timenow.date().day == 28:

                users_data = await self.bot.fetchmany(
                    "SELECT user_id, monthlycount FROM users ORDER BY monthlycount DESC", 3
                )
                m = ('\n'.join(f"<@{data[0]}> ended up **`#{n+1}`** with **`{data[1]}`** characters"
                               for n, data in enumerate(users_data)))
                channel = self.bot.get_channel(924757636417748992)
                await channel.send(f"**Montly Winners!**\n {m}")

                await self.bot.execute(
                    "UPDATE users SET monthlycount = 0"
                )

    @count_check.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

# //////////////////////////////////////// #

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.guild is None:
                return
            if message.guild.id == self.bot.GUILD:
                if message.channel.category_id in CATEGORY:
                    user_check = await self.bot.fetchrow(
                        "SELECT user_id, charcount, achievements FROM users WHERE user_id = ?",
                        message.author.id
                    )
                    msg_count = len(message.content)
                    if user_check:
                        await self.bot.execute(
                            "UPDATE users SET charcount = charcount + ?, dailycount = dailycount + ?, weeklycount = weeklycount + ?, monthlycount = monthlycount + ? WHERE user_id = ?",
                            msg_count, msg_count, msg_count, msg_count, message.author.id
                        )
                        a_list = json.loads(user_check[2])
                        await self.charcountachivements(message, user_check[1] + msg_count, a_list)
                        await self.onetimeachivements(message, a_list)
                    else:
                        j = json.dumps([])
                        await self.bot.execute(
                            "INSERT INTO users(user_id, charcount, dailycount, weeklycount, monthlycount, achievements) VALUES(?,?,?,?,?,?)",
                            message.author.id, msg_count, msg_count, msg_count, msg_count, j
                        )
                        a_list = []
                        await self.charcountachivements(message.author, msg_count, a_list)
                        await self.onetimeachivements(message, a_list)

    async def charcountachivements(self, message, count, a_list):
        if count:
            for a in ACHIEVEMENTS:
                if count >= a:
                    text = f"Reached {a} Characters"
                    if text not in a_list:
                        a_list.append(text)
                        j = json.dumps(a_list)
                        await self.bot.execute(
                            "UPDATE users SET achievements = ? WHERE user_id = ?",
                            j, message.author.id
                        )
                        ch = message.guild.get_channel(924757636417748992)
                        await ch.send(f"||{message.author.mention}|| \n**Achievement Unlocked**- *Reached {a} Characters*")

    async def onetimeachivements(self, message, a_list):
        if message.channel.category_id == 923439155768352818:
            text = "Getting Started"
            if text not in a_list:
                a_list.append(text)
                j = json.dumps(a_list)
                await self.bot.execute(
                    "UPDATE users SET achievements = ? WHERE user_id = ?",
                    j, message.author.id
                )
                ch = message.guild.get_channel(924757636417748992)
                await ch.send(f"||{message.author.mention}|| \n**Achievement Unlocked**- *{text}*")

        elif message.channel.category_id == 923413738869116971:
            text = "Howdy partner"
            if text not in a_list:
                a_list.append(text)
                j = json.dumps(a_list)
                await self.bot.execute(
                    "UPDATE users SET achievements = ? WHERE user_id = ?",
                    j, message.author.id
                )
                ch = message.guild.get_channel(924757636417748992)
                await ch.send(f"||{message.author.mention}|| \n**Achievement Unlocked**- *{text}*")

        elif message.channel.category_id == 923748324530585640:
            text = "Warrior Student"
            if text not in a_list:
                a_list.append(text)
                j = json.dumps(a_list)
                await self.bot.execute(
                    "UPDATE users SET achievements = ? WHERE user_id = ?",
                    j, message.author.id
                )
                ch = message.guild.get_channel(924757636417748992)
                await ch.send(f"||{message.author.mention}|| \n**Achievement Unlocked**- *{text}*")

        elif message.channel.category_id == 938177831991668776:
            text = "Mutant"
            if text not in a_list:
                a_list.append(text)
                j = json.dumps(a_list)
                await self.bot.execute(
                    "UPDATE users SET achievements = ? WHERE user_id = ?",
                    j, message.author.id
                )
                ch = message.guild.get_channel(924757636417748992)
                await ch.send(f"||{message.author.mention}|| \n**Achievement Unlocked**- *{text}*")

        if message.channel.category_id == 938177831991668776 or message.channel.category_id == 923748324530585640:
            text = "Groupie"
            if text not in a_list:
                a_list.append(text)
                j = json.dumps(a_list)
                await self.bot.execute(
                    "UPDATE users SET achievements = ? WHERE user_id = ?",
                    j, message.author.id
                )
                ch = message.guild.get_channel(924757636417748992)
                await ch.send(f"||{message.author.mention}|| \n**Achievement Unlocked**- *{text}*")


def setup(bot):
    bot.add_cog(CharCount(bot))
    print("[CharCount] Loaded")
