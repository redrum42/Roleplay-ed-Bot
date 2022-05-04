import disnake
import aiosqlite
import os
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

OWNER = 288199261185900547
INTENTS = disnake.Intents.default()
INTENTS.members = True


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.GUILD = 923413542303055932

    async def db_main(self):
        self.db = await aiosqlite.connect("main.sqlite")
        print("Main DataBase Connected")

    async def commit(self):
        await self.db.commit()

    async def execute(self, query, *values):
        async with self.db.cursor() as cur:
            await cur.execute(query, tuple(values))
        await self.commit()

    async def fetchval(self, query, *values):
        async with self.db.cursor() as cur:
            exe = await cur.execute(query, tuple(values))
            val = await exe.fetchone()
        return val[0] if val else None

    async def fetchrow(self, query, *values):
        async with self.db.cursor() as cur:
            exe = await cur.execute(query, tuple(values))
            row = await exe.fetchmany(size=1)
        if len(row) > 0:
            row = [r for r in row[0]]
        else:
            row = None
        return row

    async def fetchmany(self, query, size, *values):
        async with self.db.cursor() as cur:
            exe = await cur.execute(query, tuple(values))
            many = await exe.fetchmany(size)
        return many

    async def fetch(self, query, *values):
        async with self.db.cursor() as cur:
            exe = await cur.execute(query, tuple(values))
            all = await exe.fetchall()
        return all


bot = MyBot(command_prefix="-",
            owner_id=OWNER,
            intents=INTENTS,
            help_command=None,
            test_guilds=[923413542303055932],
            sync_commands_debug=False
            )


@bot.event
async def on_ready():
    print("Ready!")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Reload the extension"""
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(embed=disnake.Embed(
        description=f"`{extension.upper()}` reloaded!",
        color=disnake.Color.dark_gold()))


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """load the extension"""
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(embed=disnake.Embed(
        description=f"`{extension.upper()}` loaded!",
        color=disnake.Color.dark_gold()))


for file in os.listdir("./cogs"):
    if file.startswith("!"):
        pass
    elif file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


bot.loop.run_until_complete(bot.db_main())
bot.run(TOKEN)
