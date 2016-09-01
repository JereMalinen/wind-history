# This Python file uses the following encoding: utf-8
import urllib
from datetime import datetime
import re
import logging
import sys


logger = logging.getLogger('weather.py')

PATH = './'
DATA_FILE = PATH + '%s.csv'
DIRECTION_FILE = PATH + 'direction_%s.csv'
URL = 'http://weather.willab.fi/weather.html.fi'
DATE_RE = '(?P<date>\d+\.\d+\.\d+ \d+:\d+)'
#<tr><th>Tuulen nopeus:</th><td>1,2 m/s (puuskissa: 4,6 m/s)</td></tr>
WIND_RE = 'Tuulen nopeus.*?(?P<base>[\d,]+) .*? (?P<blast>[\d,]+)'
#<tr><th>Tuulen suunta:</th><td>194&deg; <img src="http://www.ipv6.wi
DIRECTION_RE = 'Tuulen suunta(.*?)(?P<number>[\d]+)&deg;'


def get_date(page):
    m = re.search(DATE_RE, page)
    if m:
        date = m.group('date')
        return datetime.strptime(date, '%d.%m.%Y %H:%M')
    logger.warn('Could not parse date: %s' % page)
    return datetime.now()


def get_wind_speed(page):
    """
    >>> wind_speed('<th>Tuulen nopeus:</th><td>1,2 m/s (puuskissa: 4,6 m/s)</td>')
    ('1.2', '4.6')
    >>> wind_speed('<th>Tuulen nopeus:</th><td>1 m/s (puuskissa: 4 m/s)</td>')
    ('1', '4')
    >>> wind_speed('<th>Tuulen nopeus:</th><td>tyynta (puuskissa: 4 m/s)</td>')
    """
    m = re.search(WIND_RE, page)
    if m:
        base = m.group('base')
        blast = m.group('blast')
        return (base.replace(',', '.'), blast.replace(',', '.'))
    logger.warn('Could not parse wind speed: %s' % page)
    return None


def get_direction(page):
    """
    >>> direction('<th>Tuulen suunta:</th><td>193&deg; <img src="http://www.ipv6.willab.fi/weather/arr/s.png" alt="" />')
    '193'
    """
    m = re.search(DIRECTION_RE, page)
    if m:
        return m.group('number')
    logger.warn('Could not parse wind direction: %s' % page)
    return None


def write_data(date, speed, direction):
    file_date = date.strftime('%Y.%m.%d')
    graph_date = date.strftime('%Y/%m/%d %H:%M:%S')
    if speed:
        f = open(DATA_FILE % file_date, 'a')
        f.write('%s,%s,%s\n' % (graph_date, speed[0],
                                speed[1]))
    if direction:
        f = open(DIRECTION_FILE % file_date, 'a')
        f.write('%s,%s\n' % (graph_date, direction))


def get_weather_data():
    sock = urllib.urlopen(URL)
    page = sock.read()
    sock.close()
    date = get_date(page)
    speed = get_wind_speed(page)
    direction = get_direction(page)
    write_data(date, speed, direction)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        import doctest
        doctest.testmod()
    else:
        LOG_LEVEL = logging.INFO
        logger.setLevel(LOG_LEVEL)
        ch = logging.StreamHandler()
        ch_file = logging.FileHandler(filename='weather.log')
        ch.setLevel(logging.ERROR)
        ch_file.setLevel(LOG_LEVEL)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        ch_file.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(ch_file)
        
        logger.info('Running weather.py')
        try:
            get_weather_data()
        except Exception, ex:
            logger.exception("Something awful happened! %s" % ex)
