import disnake
from disnake import Intents
from disnake.ext import commands, tasks
import json
import a2s

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix="!!!", help_command=None, intents=Intents.all())


@tasks.loop(seconds=15)
async def update_status():
    try:
        address = [config['server_ip'], config['query_server_port']]
        a2s_info = a2s.info(tuple(address), timeout=5, encoding="utf-8")

        if a2s_info.player_count == 0:
            activity_type = disnake.ActivityType.watching
            status = disnake.Status.idle
            await bot.change_presence(
                activity=disnake.Activity(name=config['empty_server_status'], type=activity_type), status=status
            )
        else:
            activity_type = disnake.ActivityType.watching
            status = disnake.Status.online
            players_count = a2s_info.player_count
            players_max_count = a2s_info.max_players
            server_status = config["server_status"].format(players_count=players_count,
                                                           players_max_count=players_max_count)
            await bot.change_presence(
                activity=disnake.Activity(name=server_status, type=activity_type), status=status
            )
    except Exception as e:
        print(f"An error occurred: {e}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_status.start()


bot.run(config['token'])
