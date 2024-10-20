import datetime


def convert_timestamp(timestamp):
    converted_timestamp = datetime.datetime.strptime(
        timestamp, "%Y-%m-%dT%H:%M:%S.%f%z"
    ) + datetime.timedelta(hours=5, minutes=30)
    return converted_timestamp.strftime("%d %b %y, %I:%M %p")
