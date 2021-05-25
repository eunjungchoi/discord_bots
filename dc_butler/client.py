import asyncio
import os
import sys

import discord

ENV = 'local'

client = discord.Client()
help_message = """원하는 시간을 입력해주세요. 그때가 되면 타이머봇이 시간을 알려드릴게요.
예시) 10분, 1시간 25분, 2분 30초
"""
LOCAL_BOT_CHANNEL_ID = os.getenv("LOCAL_BOT_CHANNEL_ID", '')


@client.event
async def on_ready():
    print(f'We have logged in as {ENV} server: {client.user}')


async def timer_handler(message, arg):
    if arg == 'help':
        await message.channel.send(help_message)
        return

    await message.channel.send(arg + ' 뒤에 알려드릴게요 :ok_hand:')

    duration = convert_time_to_seconds(arg)
    await asyncio.sleep(duration)
    await message.channel.send(arg + ' 됐습니다 :coffee:')


def is_local_channel(channel_id):
    if not LOCAL_BOT_CHANNEL_ID:
        return False
    return channel_id == int(LOCAL_BOT_CHANNEL_ID)


def message_allowed(channel_id):
    if is_local_channel(channel_id) and ENV == 'local':
        return True
    if not is_local_channel(channel_id) and ENV == 'production':
        return True
    return False


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message_allowed(message.channel.id):
        return

    dispatch_handlers = {
        '타이머': timer_handler,
    }

    command, arg = split_message_argument(message.content)
    if not command:
        return

    dispatch_handler = dispatch_handlers.get(command)
    if not dispatch_handler:
        # error message
        pass
    await dispatch_handler(message, arg)


def parse_command(content):
    if content[0] != '/':
        return None
    command_with_slash = content.split(' ')[0]
    return command_with_slash[1:]


def split_message_argument(content):
    if command := parse_command(content):
        message = content[len(command)+1:].strip()
        return command, message
    return None, None


def convert_time_to_seconds(arg):
    min_ = sec_ = 0
    for txt in arg.split(' '):
        if txt.endswith('분'):
            min_ += int(txt[:-1].strip())
        elif txt.endswith('초'):
            sec_ += int(txt[:-1].strip())
    return min_ * 60 + sec_


def run(token):
    client.run(token)
