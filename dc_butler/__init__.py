import asyncio
import os
import sys

import discord

client = discord.Client()
TOKENS = {
    'local': 'DC_TOKEN_LOCAL',
    'test': 'DC_TOKEN_TEST',
    'production': 'DISCORD_TOKEN'
}
ENV = 'local'
help_message = """원하는 시간을 입력해주세요. 그때가 되면 타이머봇이 시간을 알려드릴게요.
예시) 10분, 1시간 25분, 2분 30초
"""
LOCAL_BOT_CHANNEL_ID = os.getenv("LOCAL_BOT_CHANNEL_ID")


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


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == int(LOCAL_BOT_CHANNEL_ID) and ENV != 'local':
        return
    if message.channel.id != int(LOCAL_BOT_CHANNEL_ID) and ENV == 'local':
        return

    dispatch_handlers = {
        '타이머': timer_handler,
    }

    command, arg = split_message_argument(message.content)
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
    ENV = sys.argv[1]
    TOKEN = os.getenv(TOKENS[ENV])
    client.run(TOKEN)
