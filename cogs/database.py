  
import discord, csv
from discord.ext import commands
from discord.ext.commands import bot

class Database(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def read_db(self):
        lines = list()

        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                lines.append(row)

        return lines

    async def write_db(self, guild_id, address):
        with open('database.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([guild_id, address])

    async def replace_db(self, guild_id):
        lines = list()

        with open('database.csv', 'r') as inp:
            for row in csv.reader(inp):
                if row[0] != str(guild_id):
                    lines.append(row)

        with open('database.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for x in range(0, len(lines)):
                writer.writerow([lines[x][0]])

def setup(client):
    client.add_cog(Database(client))