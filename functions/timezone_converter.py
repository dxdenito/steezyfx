from datetime import datetime

import pytz

def convert_timezone(input_time_str, from_tz_str, to_tz_str):
    from_tz = pytz.timezone(from_tz_str)
    to_tz = pytz.timezone(to_tz_str)

    naive_dt = datetime.strptime(input_time_str, '%Y-%m-%dT%H:%M')
    from_dt = from_tz.localize(naive_dt)
    to_dt = from_dt.astimezone(to_tz)

    return to_dt.strftime('%y-%m-%d %H:%M %p')