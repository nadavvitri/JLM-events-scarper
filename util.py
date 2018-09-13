from time import strftime, strptime
from datetime import datetime

MONTHS = {
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nob': '11',
    'Dec': '12',
}

EXAMPLE_EVENTS = [{
    'htmlLink': 'https://www.itraveljerusalem.com/evt/mifgashim-tour',
    'updated': '2018-09-06T13:00:00',
    'summary': 'Test',
    'description': 'bla bla more information',
    'location': 'first station',
    'start': {'dateTime': '2018-09-06T13:00:00',
              'timeZone': 'Asia/Jerusalem'},
}]


def to_datetime(date, time):
    """
    Change to datetime format (iso 8601)
    :param date: e.g "Oct 12"
    :param time: e.g "7:30AM"
    :return: formatted datetime
    """
    month, day = date.split()
    if len(day) == 1:
        day = "0" + day

    year = str(datetime.today().year)
    month = MONTHS[month]
    strt = strptime(" ".join([time[:-2], time[-2:]]), '%I:%M %p')
    time = "T" + strftime('%H:%M', strt) + ":00"
    return "-".join([year, month, day]) + time
