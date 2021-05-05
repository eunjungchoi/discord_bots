from dc_butler.init__ import split_message_argument, convert_time_to_seconds


def test_split_message_argument():
    assert split_message_argument('/타이머 1시간 뒤에 알려줘') == '1시간 뒤에 알려줘'


def test_convert_time_to_seconds():
    assert convert_time_to_seconds('1분 30초') == 90
    assert convert_time_to_seconds('10분 ') == 600
