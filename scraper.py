import argparse
import itraveljerusalem_scraper
from google_calendar import GoogleCalendar

SCRAPERS = [itraveljerusalem_scraper]
SCRAPERS_NAMES = [x.__name__ for x in SCRAPERS]


def parse_arguments():
    """
    Parses scraper arguments
    """
    parser = argparse.ArgumentParser(description='Extract events in jerusalem to csv file and '
                                                 '(optional) to Google calendar')
    parser.add_argument('-g', '--g',
                        help="Calendar symbolic name where events will be added into.",
                        action="store_true")
    parser.add_argument('--csv', '-csv',
                        help="export event to csv file",
                        action='store_true')
    parser.add_argument('--all', '-all',
                        help="activate all scrapers",
                        action='store_true')
    parser.add_argument('--scraper', '-scraper', nargs='+',
                        help="List of scrapers that will be used. Currently supporting:" +
                             (" \'{}\'" * len(SCRAPERS)).format(*SCRAPERS_NAMES))
    return parser, parser.parse_args()


def add(events):
    """
    Add Event to events in google calendar
    :param events: Events object
    :return:
    """
    calendar = GoogleCalendar()
    calendar.add_events(events)


if __name__ == '__main__':
    parser, args = parse_arguments()
    # no -all flag or scrapers list was accepted
    if not (args.all or args.scraper):
        parser.error('No scraper selected, use --all or --scraper SCRAPER [SCRAPER ...]')
    # both -all and scrapers list was accepted
    if args.all and args.scraper:
        parser.error('--all and --scraper is ambiguous. Use only one of them.')
    if args.all:
        args.scraper = SCRAPERS_NAMES

    events = []
    for scraper in SCRAPERS:
        if scraper.__name__ in args.scraper:
            events += scraper.get_events()

    if args.g:
        add(events)


