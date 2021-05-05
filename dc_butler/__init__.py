import asyncio
import os
import time

import discord
from discord.ext import commands

client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")
help_message = """원하는 시간을 입력해주세요. 그때가 되면 타이머봇이 시간을 알려드릴게요.
예시) 10분, 1시간 25분, 2분 30초 
"""


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # print(message)
    print(message.content)

    if message.content.startswith('/타이머'):
        command, arg = split_message_argument(message.content)

        if arg == 'help':
            await message.channel.send(help_message)
            return

        await message.channel.send(arg + ' 뒤에 알려드릴게요 :ok_hand:')

        duration = convert_time_to_seconds(arg)
        await asyncio.sleep(duration)
        await message.channel.send(arg + ' 됐습니다 :coffee:')
def parse_command(content):
    if content[0] != '/':
        return None
    command_with_slash = content.split(' ')[0]
    return command_with_slash[1:]


def split_message_argument(content):
    command = parse_command(content)
    message = content[len(command)+1:].strip()
    return command, message


def convert_time_to_seconds(arg):
    min_ = sec_ = 0
    for txt in arg.split(' '):
        if txt.endswith('분'):
            min_ += int(txt[:-1].strip())
        elif txt.endswith('초'):
            sec_ += int(txt[:-1].strip())
    return min_ * 60 + sec_


if __name__ == '__main__':
    client.run(TOKEN)
