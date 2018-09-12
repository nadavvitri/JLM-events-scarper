from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime


def get_events():
    """
    Parse and return list of events from the url address:
    https://www.itraveljerusalem.com/events/
    """
    url = "https://www.itraveljerusalem.com/events/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # get the events container
    event_containers = soup.findAll('div', class_="listing-item__info-wrap")
    parse_event(event_containers)


def parse_event(event_containers):
    """
    Parse event container to title, date, location and info
    :param event_containers: list of events (with tags)
    :return: formatted event to title, date, location, info
    """
    csv_file = csv.writer(open('index.csv', 'a'))
    csv_file.writerow(['Title', 'Date', 'Location', 'Information', 'Phone', 'Last update'])

    for event in event_containers:
        title = event.find('h3', class_="listing-item__title").text.strip()
        date = parse_date(event)

        # load the "Read more" link
        link = event.a['href']
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')

        info_brand = soup.findAll('span', class_="info-content")
        location, phone = info_brand[1].text.strip(), info_brand[0].text.strip()
        information = parse_info(event)

        # export to csv file
        csv_file.writerow([title, date, location, information, phone, datetime.now()])


def parse_info(event):
    """
    Parse from the event "Read more" links the information about the event
    :param event: event container
    :return: full description of the event
    """
    # load the "Read more" link
    link = event.a['href']
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')

    information_container = soup.find('div', class_="article__info-wrap")

    clean = information_container.find('ul', class_="meta-list meta-list_noborder")
    clean.extract()

    information = ""
    for tag in information_container:
        information += tag.text.strip()
    return information.rsplit('\n', 1)[0]


def parse_date(event):
    """
    Extract date from event container
    :param event: event container
    :return: formatted date: day, time
    """
    # find date container
    date_container = event.find('span', class_="page__date-info")

    text = [text for text in date_container.stripped_strings]
    return text[2] + ", " + text[-1]


if __name__ == '__main__':
    get_events()
