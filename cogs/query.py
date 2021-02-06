import discord, valve.source.a2s
from discord.ext import commands
from discord.ext.commands import bot

class Query(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_server_info(self, address):
        address = address.split(':')[0], int(address.split(':')[1])
        info = list()

        with valve.source.a2s.ServerQuerier(address) as server:
            info.append(server.info()['player_count'])
            info.append(server.info()['max_players'])
            info.append(server.info()['server_name'])
            info.append(server.info()['map'])
            info.append(server.info()['game'])

        return info

    async def get_players(self, address):
        address = address.split(':')[0], int(address.split(':')[1])
        player_list, time_online = [], []

        with valve.source.a2s.ServerQuerier(address) as query:
            for player in query.players()['players']:
                player_list.append("{name}".format(**player))
                time_online.append(round(float("{duration}".format(**player)) / 60))

        return player_list, time_online

def setup(client):
    client.add_cog(Query(client))