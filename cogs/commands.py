import discord
from discord.ext import commands
from discord.ext.commands import bot
from cogs.query import *
from cogs.database import *
from main import has_perms

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        author = self.client.get_user(ctx.message.author.id)

        embed = discord.Embed(colour=discord.Color.blue())
        embed.set_author(name='Commands:')
        embed.add_field(name='$help', value='Displays this message.', inline=False)
        embed.add_field(name='$setup IP:Port', value='Used to setup a source server.', inline=False)
        embed.add_field(name='$server', value='Displays current server information.', inline=False)

        embed2 = discord.Embed(colour=discord.Color.blue())
        embed2.add_field(name='To setup your server please use this format: $setup IP:Port', value='$setup 127.0.0.1:27015', inline=False)
        embed2.set_footer(text='Source Server Manager | Created by Hamzah#0017')

        await author.send(embed=embed)
        await author.send(embed=embed2)

        await ctx.send('Please check your DMs for a list of commands.')

    @commands.command()
    async def setup(self, ctx, address):
        if not has_perms(ctx):
            await ctx.send('> You must be an admin to use this command.')
            return

        if "." not in address or ":" not in address:
            await ctx.send('> The IP/Port was formatted incorrectly, e.g. 127.0.0.1:27015')
            return

        guild_id = ctx.message.author.guild.id

        await Database(self).replace_db(guild_id)
        await Database(self).write_db(guild_id, address)

        await ctx.send('Your server has been added to the database, use the $server command to view server information.')

    @commands.command()
    async def server(self, ctx):
        check = str(ctx.message.channel.type)
        if check == 'private':
            return False

        address = (await Database(self).read_db())[0][1]
        server_info = await Query(self).get_server_info(address)

        server_embed = discord.Embed(colour=discord.Color.blue())
        server_embed.set_thumbnail(url='https://cdn.icon-icons.com/icons2/1852/PNG/512/iconfinder-server-4417119_116634.png')
        server_embed.set_author(name=server_info[2])
        server_embed.add_field(name='IP Address:', value=address)
        server_embed.add_field(name='Players:', value=str(server_info[0]) + '/' + str(server_info[1]), inline=False)
        server_embed.add_field(name='Map:', value=server_info[3], inline=False)
        server_embed.set_footer(text='Source Server Manager | Created by Hamzah#0017')

        await ctx.send(embed=server_embed)

        if server_info[0] == 0:
            return

        try:
            player_info = await Query(self).get_players(address)

            player_embed = discord.Embed(colour=discord.Color.blue())
            player_embed.set_author(name='Online Players:')

            for i in range(0, server_info[0]):
                player_embed.add_field(name=player_info[0][i], value=str(player_info[1][i]) + ' minutes')
            
            await ctx.send(embed=player_embed)

        except:
            await ctx.send('> I was unable to print the player list, this could be due to weird characters in names.')


def setup(client):
    client.add_cog(Commands(client))