from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/calendar'  # read&write permissions


class GoogleCalendar:
    def __init__(self):
        self.g_cal = setup()

    def add_events(self, events):
        """
        add events to g_cal calender
        :param events: list of Events
        """
        try:
            for event in events:
                e = self.g_cal.events().insert(
                    calendarId='primary',
                    sendNotifications=True,
                    body=event).execute()
                self.print_status(e, 'added')
        except Exception as err:
            print('Event was not created successfully')

    def print_status(self, e, operation):
        """
        Print the status of an event
        :param e: Event object
        :param operation: add / delete
        """
        print('''*** %r event %s:
            Start: %s
            End:   %s''' % (e['summary'], operation,
                            e['start']['dateTime'], e['end']['dateTime']))

    # def delete_events(self, events):
    #     """
    #     Deletes a list of events
    #     :param events: Events object
    #     :return: a list of deleted events
    #     """
    #     deleted = []
    #     for event in events:
    #         deleted.append(self.g_cal.events().delete(
    #             calendarId='primary',
    #             eventId=event['id']
    #             ).execute())
    #         self.print_status(event, 'deleted')
    #     return deleted

    # def get_events(self):
    #     """
    #     Gets all the event from calendar
    #     :return: google calendar events list
    #     """
    #     events_list = []
    #     page_token = None
    #     cur_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())  # get only events from current time and on
    #     while True:
    #         events = self.g_cal.events().list(calendarId=self.cal_id, pageToken=page_token, timeMin=cur_time).execute()
    #         for e in events['items']:
    #             events_list.append(e)
    #         page_token = events.get('nextPageToken')
    #         if not page_token:
    #             break
    #
    #     return events_list


def setup():
    """
    create calender
    :return: google calender object
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service
