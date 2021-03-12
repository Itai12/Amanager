import discord, sqlite3, json, datetime, pytz
from discord.ext import commands
from datetime import datetime, date
from pytz import timezone

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:

            connection = sqlite3.connect("iso_card.db")
            cursor = connection.cursor()
            member_id = (f"{message.author.id}",)
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            member_values = cursor.fetchone()
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()

###########################
# NEVER GONNA GIVE YOU UP #
###########################

            if message.content.lower() == "never gonna give you up":
                achievement = ":notes:"
                member_values_list = member_values[2]
                if member_values != None and achievement not in member_values_list:
                    archi_list = str(member_values[2]) + f" {achievement}"
                    updated_user = (f"{archi_list}", f"{message.author.id}",)
                    cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                    connection.commit()
                await message.channel.send(":notes: Never gonna let you down !")

###############
# KONAMI CODE #
###############

            konami_codes = ['up up down down left right left right b a', 'uuddlrlrba']
            if message.content.lower() in konami_codes:
                achievement = ":video_game:"
                member_values_list = member_values[2]
                if member_values != None and achievement not in member_values_list:
                    archi_list = str(member_values[2]) + f" {achievement}"
                    updated_user = (f"{archi_list}", f"{message.author.id}",)
                    cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                    connection.commit()
                embed = discord.Embed(title=f"Le pouvoir de Konami a été RELACHÉ !!!", color=0xf8e604)
                embed.add_field(name='Le cheat code a bien été activé.', value="** **", inline=False)
                await message.author.send(embed=embed)
                await message.delete()

############
# BOT PING #
############

            bot_mentions = ['@Amanager#8727', '<@760171813866700850>', '<@!760171813866700850>']
            if message.content in bot_mentions:
                mention_time = int(datetime.now(pytz.timezone('Europe/Paris')).strftime("%H"))
                mention_date = date.today().strftime("%B %d, %Y")
                if 7 <= mention_time <= 12:
                    mention_time = "Bonjour"
                elif 13 <= mention_time <= 19:
                    mention_time = "Bon après-midi"
                elif 20 <= mention_time <= 23:
                    mention_time = "Bonsoir"
                elif 0 <= mention_time <= 6:
                    mention_time = "Bonne nuit"

                if "december" in mention_date.lower():
                    mention_time = "Oh! oh! oh! " + str(mention_time)
                elif "august" in mention_date.lower():
                    mention_time = "Bonnes vacances d'été ! " + str(mention_time)

                embed = discord.Embed(title=f"{mention_time} ! :grin:", description=f"Mon préfixe est **{self.client.command_prefix}** | **{self.client.command_prefix}help** pour plus d'infos !", color=0xf5900b)
                embed.add_field(name="** **", value="Tu recontres des bugs, tu as besoin d'aide, tu veux contribuer ou juste discuter ? Tu peux rejoindre le [serveur support](https://discord.gg/WamZS7CExw) du bot !", inline=False)
                await message.channel.send(embed=embed)

#################################
# VÉRIFIE SI LA COMMANDE EXISTE #
#################################

            if message.content.startswith(self.client.command_prefix):
                command = message.content.split(" ")[0].replace(self.client.command_prefix, "")
                commands_list = json_object_nm['help_commands']
                owner_commands_list = ['load', 'unload', 'restart']
                if command not in commands_list:
                    if command not in owner_commands_list:
                        await message.channel.send(f"{message.author.mention} Désolé mais la commande que tu as entré n'existe pas... :wink: Si tu veux voir la liste, tu peux faire **{self.client.command_prefix}help** !")

##################################
# STARBOARD - AJOUT DE RÉACTIONS #
##################################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        connection = sqlite3.connect("starboard.db")
        cursor = connection.cursor()
        server_id = (f"{payload.guild_id}",)
        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
        server_values = cursor.fetchone()
        if server_values != None and server_values[1] == "yes":
            if payload.emoji.name == str(server_values[3]):
                message_id_cursor = 'SELECT * FROM {} WHERE message_id = {}'.format(f"_{payload.guild_id}", payload.message_id)
                cursor.execute(message_id_cursor)
                message_values = cursor.fetchone()

                if message_values == None:
                    new_message = (int(payload.message_id), int(payload.channel_id), 1, 0, "no")
                    cursor.execute('INSERT INTO {} VALUES(?, ?, ?, ?, ?)'.format(f"_{payload.guild_id}"), new_message)
                    connection.commit()
                else:
                    nb_stars = int(message_values[2])
                    if nb_stars >= 0:
                        new_nb_of_stars = nb_stars + 1
                        updated_user = (f"{new_nb_of_stars}", f"{payload.message_id}",)
                        cursor.execute('UPDATE {} SET number_of_stars = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_user)
                        connection.commit()

                        message_id = (f"{payload.message_id}",)
                        cursor.execute('SELECT * FROM {} WHERE message_id = ?'.format(f"_{payload.guild_id}"), message_id)
                        messages_values_f = cursor.fetchone()
                        server_id = (f"{payload.guild_id}",)
                        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                        message_values = cursor.fetchone()

                        chosen_emoji = message_values[3]
                        number_of_stars = int(messages_values_f[2])
                        was_message_sent = messages_values_f[4]
                        limit_trigger = message_values[2]

                        if number_of_stars == limit_trigger:
                            if was_message_sent == "no":
                                was_message_sent = "yes"
                                channel_to_send = self.client.get_channel(int(message_values[4]))
                                channel_to_find = self.client.get_channel(payload.channel_id)
                                msg = await channel_to_find.fetch_message(payload.message_id)
                                embed = discord.Embed(title="Nouveau message sur le starboard !", description=f"de {msg.author.mention} | [ID du message](https://discord.com/channels/736689848626446396/{msg.channel.id}/{msg.id})")
                                try:
                                    embed.set_image(url=msg.attachments[0].url)
                                except IndexError:
                                    pass
                                embed.add_field(name=f"{number_of_stars} {chosen_emoji}", value="** **", inline=False)
                                if msg.content:
                                    embed.add_field(name="** **", value=msg.content, inline=False)
                                bot_message = await channel_to_send.send(embed=embed)
                                updated_user = (f"{bot_message.id}", f"{payload.message_id}",)
                                cursor.execute('UPDATE {} SET bot_message_id = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_user)
                                updated_message_s = (f"{was_message_sent}", f"{payload.message_id}",)
                                cursor.execute('UPDATE {} SET was_message_sent = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_message_s)
                                connection.commit()
                        elif number_of_stars > limit_trigger:
                            cursor.execute('SELECT * FROM {} WHERE message_id = ?'.format(f"_{payload.guild_id}"), message_id)
                            messages_values_b = cursor.fetchone()
                            b_msg = messages_values_b[3]
                            channel_to_find = self.client.get_channel(int(message_values[4]))
                            msg_bot = await channel_to_find.fetch_message(b_msg)

                            channel_to_send = self.client.get_channel(int(message_values[4]))
                            channel_to_find = self.client.get_channel(payload.channel_id)
                            msg = await channel_to_find.fetch_message(payload.message_id)

                            embed = discord.Embed(title="Nouveau message sur le starboard !", description=f"de {msg.author.mention}")
                            try:
                                embed.set_image(url=msg.attachments[0].url)
                            except IndexError:
                                pass
                            embed.add_field(name=f"{number_of_stars} :star:", value=msg.content, inline=False)
                            embed.add_field(name="** **", value=f"[ID du message](https://discord.com/channels/736689848626446396/{msg.channel.id}/{msg.id})", inline=False)
                            await msg_bot.edit(content=None, embed=embed)

        connection.close()

#########################################
# STARBOARD - SUPPRESSIONS DE RÉACTIONS #
#########################################

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        connection = sqlite3.connect("starboard.db")
        cursor = connection.cursor()
        server_id = (f"{payload.guild_id}",)
        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
        server_values = cursor.fetchone()
        if server_values != None and server_values[1] == "yes":
            if payload.emoji.name == str(server_values[3]):
                message_id = (f"{payload.message_id}",)
                cursor.execute('SELECT * FROM {} WHERE message_id = ?'.format(f"_{payload.guild_id}"), message_id)
                message_values = cursor.fetchone()

                nb_stars = int(message_values[2])
                new_nb_of_stars = nb_stars - 1
                updated_user = (f"{new_nb_of_stars}", f"{payload.message_id}",)
                cursor.execute('UPDATE {} SET number_of_stars = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_user)
                connection.commit()

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("triggers")