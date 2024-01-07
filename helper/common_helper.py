from datetime import datetime
import pytz


def convert_date_to_utc_datetime(
    date: str,
    date_type: str = "start",
):
    """
    date 형식의 string 을 UTC datetime 객체로 변환합니다.

    date: '2024-01-01'
    date_type:
        - start
        - end

    """

    if date_type == 'start':
        time_str = '00:00:00'
    elif date_type == 'end':
        time_str = '23:59:59'
    else:
        raise ValueError("date_type must be 'start' or 'end'")

    # 주어진 날짜 및 시간 문자열
    input_datetime_str = f'{date} {time_str}'

    # 문자열을 datetime 객체로 변환합니다. 기본적으로 로컬 시간으로 가정합니다.
    input_datetime = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')

    # 현지 시간대로 설정 (UTC+9)
    local_timezone = pytz.timezone('Asia/Seoul')
    local_datetime = local_timezone.localize(input_datetime)

    # 로컬 시간을 UTC로 변환합니다.
    utc_datetime = local_datetime.astimezone(pytz.utc)

    return utc_datetime

