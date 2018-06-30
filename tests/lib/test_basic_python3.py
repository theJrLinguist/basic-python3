#! /usr/bin/env python3

import sys, os
sys.path.append(os.getcwd())

import re, time, vcr
import config, lib.basic_python3

def sanitise_telegram_url(request):
    request.uri = re.sub('(?<=telegram\.org/bot)[^/]*', '', request.uri)
    request.uri = re.sub('(?<=\?chat_id=)\d+', '', request.uri)
    return request

vcr = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    before_record_request=sanitise_telegram_url
)

@vcr.use_cassette(match_on=['host'])
def test_telegram_get_me():
    result_list = lib.basic_python3.telegram_whoami(config.TELEGRAM_KEY)
    are_strings = all([ isinstance(x, str) for x in result_list ])
    are_non_empty = all([ len(x) > 0 for x in result_list ])
    assert isinstance(result_list, list)
    assert are_strings
    assert are_non_empty

@vcr.use_cassette('tests/cassettes/test_telegram_send', match_on=['host'])
def test_telegram_send():
    result = lib.basic_python3.telegram_send(
        config.TELEGRAM_KEY, config.TELEGRAM_CHAT_ID, '`test_telegram_send`'
    )
    assert result

@vcr.use_cassette(match_on=['host'])
def test_weather_get_now():
    temperatures = lib.basic_python3.weather_get_now()
    are_nums = all([
        isinstance(x, float) or isinstance(x, int) for x in temperatures
    ])
    assert temperatures != []
    assert are_nums

def test_strftime():
    time_string = '2016-01-10T13:30:33'
    time_tuple = time.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    assert lib.basic_python3.strftime(time_tuple) == time_string

def test_strftime_now():
    time_string = lib.basic_python3.strftime_now()
    assert re.match("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", time_string)
