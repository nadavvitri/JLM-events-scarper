from util import to_datetime
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
from event import Event


def get_events():
    """
    Parse and return list of events from the url address:
    https://www.itraveljerusalem.com/events/
    :return: Events list
    """
    url = "https://www.itraveljerusalem.com/events/"
    page = requests.get(url, timeout=5)
    soup = BeautifulSoup(page.text, 'html.parser')

    # get the events container
    event_containers = soup.findAll('div', class_="listing-item__info-wrap")
    return parse_event(event_containers)


def parse_event(event_containers):
    """
    Parse event container to summary, date_time, location, description, url and phone
    :param event_containers: list of events (with tags)
    :return: Events list
    """
    csv_file = csv.writer(open('index.csv', 'a'))
    csv_file.writerow(['Summary', 'DateTime', 'Location', 'Description', 'Url', 'Phone', 'Last update'])

    events = []
    for e in event_containers:
        try:
            summary = e.find('h3', class_="listing-item__title").text.strip()
        except:
            summary = None

        try:
            datetime_format = parse_date(e)
        except:
            datetime_format = None

        # load the "Read more" link
        try:
            link = e.a['href']
        except:
            link = None

        page = requests.get(link, timeout=5)
        soup = BeautifulSoup(page.text, 'html.parser')

        try:
            info_brand = soup.findAll('span', class_="info-content")
        except:
            info_brand = None

        try:
            location, phone = info_brand[1].text.strip(), info_brand[0].text.strip()
        except:
            location = phone = None

        try:
            description = parse_info(e)
        except:
            description = None

        updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # export to csv file
        csv_file.writerow([summary, datetime_format, location, description, link, phone, updated])

        # to Event object and append
        events.append(Event(summary, location, description, datetime_format, link, updated))

    return events


def parse_info(event):
    """
    Parse from the event "Read more" links the information about the event
    :param event: event container
    :return: full description of the event
    """
    # load the "Read more" link
    link = event.a['href']
    page = requests.get(link, timeout=5)
    soup = BeautifulSoup(page.text, 'html.parser')

    information_container = soup.find('div', class_="article__info-wrap")

    clean = information_container.find('ul', class_="meta-list meta-list_noborder")
    clean.extract()

    description = ""
    for tag in information_container:
        description += tag.text.strip()
    return description.rsplit('\n', 1)[0]


def parse_date(event):
    """
    Extract date from event container
    :param event: event container
    :return: formatted date: day, time
    """
    # find date container
    date_container = event.find('span', class_="page__date-info")

    text = [text for text in date_container.stripped_strings]
    return to_datetime(text[2], text[-1])


if __name__ == '__main__':
    get_events()
