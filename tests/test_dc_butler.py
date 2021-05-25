import pytest

from dc_butler import split_message_argument, convert_time_to_seconds
from dc_butler import on_message, parse_command, message_allowed, is_local_channel
from dc_butler import client

client.LOCAL_BOT_CHANNEL_ID = '1234'
CHANNEL_ID = 1234
ENV = 'local'


class MockMessage:
    def __init__(self, content):
        self.content = content
        self.author = 1
        self.channel = MockChannel()


class MockChannel:
    def __init__(self):
        self.send_buffer = []
        self.id = 9999

    async def send(self, content):
        self.send_buffer.append(content)


def test_split_message_argument():
    assert split_message_argument('/타이머 1시간 뒤에 알려줘') == (
        '타이머', '1시간 뒤에 알려줘'
    )


def test_parse_command():
    assert parse_command('/타이머 1시간 뒤에 알려줘') == '타이머'
    assert parse_command('1시간 뒤에') is None


def test_convert_time_to_seconds():
    assert convert_time_to_seconds('1분 30초') == 90
    assert convert_time_to_seconds('10분 ') == 600


def test_is_local_channel():
    assert is_local_channel(CHANNEL_ID + 1) is False
    assert is_local_channel(CHANNEL_ID) is True


def test_message_allowed():
    client.ENV = 'local'
    assert message_allowed(CHANNEL_ID + 1) is False
    assert message_allowed(CHANNEL_ID) is True

    client.ENV = 'production'
    assert message_allowed(CHANNEL_ID) is False
    assert message_allowed(CHANNEL_ID + 1) is True


@pytest.mark.asyncio
async def test_on_message():
    # when messages arrive at non-local channels,
    message = MockMessage('/타이머 5초')

    # local bot should ignore messages
    client.ENV = 'local'
    await on_message(message)
    assert len(message.channel.send_buffer) == 0

    # production bot should response to messages
    client.ENV = 'production'
    await on_message(message)
    assert message.channel.send_buffer[0] == '5초 뒤에 알려드릴게요 :ok_hand:'
    assert message.channel.send_buffer[1] == '5초 됐습니다 :coffee:'


@pytest.mark.asyncio
async def test_on_message_local_channel():
    # when messages arrive at the 'local' channel,
    message = MockMessage('/타이머 5초')
    message.channel.id = CHANNEL_ID

    client.ENV = 'local'   # local bot should response to messages
    await on_message(message)
    assert message.channel.send_buffer[0] == '5초 뒤에 알려드릴게요 :ok_hand:'
    assert message.channel.send_buffer[1] == '5초 됐습니다 :coffee:'

    message.channel.send_buffer = []

    client.ENV = 'production'  # production bot should ignore messages
    await on_message(message)
    assert len(message.channel.send_buffer) == 0

