# pylint: disable=missing-module-docstring
import time
import os
import json
from datetime import datetime, timedelta
from panel_app.config import TIME_FILE

def get_date(tm=None):
    if tm is None:
        date = datetime.now()
    else:
        date = datetime.fromtimestamp(tm)
    year = date.year % 2000
    month = f'{date.month}'.zfill(2)
    day = f'{date.day}'.zfill(2)

    return int(f'{year}{month}{day}')


def get_tm(date):
    # pylint: disable=missing-function-docstring
    if isinstance(date, str):
        date = int(date)
    year = 2000 + date // 10000
    month = date % 10000 // 100
    day = date % 100
    date = datetime(
        year=year,
        month=month,
        day=day,
        hour=1,
        minute=0,
        second=0,
        microsecond=0
    )

    return int(date.timestamp())


def get_ex_date(date):
    # pylint: disable=missing-function-docstring
    if isinstance(date, str):
        date = int(date)
    year = 2000 + date // 10000
    month = date % 10000 // 100
    day = date % 100
    date = datetime(
        year=year,
        month=month,
        day=day,
        hour=23,
        minute=59,
        second=59,
        microsecond=0
    )
    return date


def get_yesterday(tm=None, date=None):
    """获取昨天的日期
    """
    if tm is None:
        tm = time.time() - 60 * 60 * 24
    if date is not None:
        tm = get_tm(date) - 60 * 60 * 24
    return get_date(tm)


def label_date(date=None, tm=None):
    if date:
        tm = get_tm(date)
    dd = datetime.fromtimestamp(tm)
    return f'{dd.month}月{dd.day}日'



class DateSettings():

    def __init__(self):
        self._file = TIME_FILE
        if not os.path.exists(self._file):
            raise OSError('文件不存在')


    def get_default(self, module):
        with open(self._file, 'r') as f:
            data = json.load(f)
        
        module = str(module)
        if not data.get(module):
            raise ValueError('该模块不存在:{0}'.format(module))

        default = data.get(module).get('default')
        if default == '1':
            step = data.get(module).get(default).get('step')
            
            end_time = datetime.today().strftime('%y%m%d')
            begin_time = (datetime.today() - timedelta(days=step)).strftime('%y%m%d')  
            return int(begin_time), int(end_time)
        
        elif default == '2':
            begin_time = data.get(module).get(default).get('start')
            end_time = data.get(module).get(default).get('end')
        
        else:
            begin_time = data.get(module).get(default).get('start')
            end_time = datetime.today().strftime('%y%m%d')

        return int(begin_time), int(end_time)


    def get_yestday(self):
        pass

    def get_today(self):
        pass

