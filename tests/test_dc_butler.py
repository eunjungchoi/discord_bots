import pytest
from dc_butler import split_message_argument, convert_time_to_seconds
from dc_butler import on_message, parse_command


class MockMessage:
    def __init__(self, content):
        self.content = content
        self.author = 1
        self.channel = MockChannel()


class MockChannel:
    def __init__(self):
        self.send_buffer = []

    async def send(self, content):
        self.send_buffer.append(content)


def test_split_message_argument():
    assert split_message_argument('/타이머 1시간 뒤에 알려줘') == (
        '타이머', '1시간 뒤에 알려줘'
    )


def test_parse_command():
    assert parse_command('/타이머 1시간 뒤에 알려줘') == '타이머'


def test_convert_time_to_seconds():
    assert convert_time_to_seconds('1분 30초') == 90
    assert convert_time_to_seconds('10분 ') == 600


@pytest.mark.asyncio
async def test_on_message():
    message = MockMessage('/타이머 5초')
    await on_message(message)
    assert message.channel.send_buffer[0] == '5초 뒤에 알려드릴게요 :ok_hand:'
    assert message.channel.send_buffer[1] == '5초 됐습니다 :coffee:'
