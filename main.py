import discord, os
from discord.ext import commands
from discord.ext.commands import bot

owner_id = 181386549525479424

client = commands.Bot(command_prefix='$')
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is online')

@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == owner_id:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'> Loaded {extension}.')

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == owner_id:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'> Unloaded {extension}.')

@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == owner_id:
        client.reload_extension(f'cogs.{extension}')
        await ctx.send(f'> Reloaded {extension}.')

def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

def has_perms(ctx):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == owner_id:
        return True

    check = str(ctx.message.channel.type)
    if check == 'private':
        return False

    return False
    
load_cogs()

client.run('TOKEN HERE')