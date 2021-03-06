import discord, random, TenGiphPy, sqlite3, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="karen", description="KAREN ?")
    async def _karen(self, ctx):
        random_karen = random.randint(1, 4)
        if random_karen == 1: # joke
            jokes_karen = ['I want to speak to the manager !', 'I want to speak with the manager !', 'Take the kids out.', 'I have a complaint, i want to speak to the manager', f'{ctx.author.mention} entre en mode Karen !']
            await ctx.send(random.choice(jokes_karen))
        elif random_karen == 2: # meme (image)
            memes_karen = ['https://is.gd/NShcnL', 'https://is.gd/hY2B4H', 'https://is.gd/KG4vtc', 'https://is.gd/tBvPsH', 'https://is.gd/SG4WmK', 'https://is.gd/xzGV2u', 'https://is.gd/8yJPKU', 'https://is.gd/H2gMSh']
            await ctx.send(random.choice(memes_karen))
        elif random_karen == 3: # gif
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()
            tengiphpy_api_key = json_object_nm['token']['tengiphpy']
            rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
            karen_gif = rgif.random("karen")
            await ctx.send(karen_gif)
        elif random_karen == 4: # nouveau nickname
            try:
                await ctx.author.edit(nick="Karen")
            except discord.errors.Forbidden:
                if str(ctx.author.name) != str(ctx.guild.owner.name):
                    await ctx.send("Je n'ai pas la permission de changer de pseudo... Donne moi cette permission pour que cette commande puisse fonctionner pleinement.\nSi j'ai déjà cette permission, vérifie que mon rôle soit le plus haut hiérarchiquement.")
                elif str(ctx.author.name) == str(ctx.guild.owner.name):
                    await ctx.send("Are you Queen Karen ?\nhttps://media.tenor.co/images/3f1fe20f669bff4e43fa862ee110b42d/tenor.gif")

        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{ctx.author.id}",)
        achievement = "<:karen:791351537347723284>"
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        member_values = cursor.fetchone()
        cursor.execute('SELECT * FROM achievements WHERE user_id = ?', member_id)
        a_user = cursor.fetchone()
        a_misc = a_user[1]
        if member_values != None and achievement not in a_misc:
            archi_list = str(a_misc) + f" {achievement}"
            updated_user = (f"{archi_list}", f"{ctx.author.id}",)
            cursor.execute('UPDATE achievements SET a_misc = ? WHERE user_id = ?', updated_user)
            connection.commit()
        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("karen")