class Event:
    """
    Represents a calendar event
    """

    def __init__(self, summary, location, description, datetime, url, updated):
        """
        Initializes an event
        :param summary: short title of event
        :param location: free text
        :param description: more info about the event
        :param datetime: iso 8601 format
        :param url: link to event page (under itraveljerusalem.com)
        :param updated: last time checked with the script
        """
        self.summary = summary
        self.location = location
        self.description = description
        self.datetime = datetime
        self.url = url
        self.updated = updated

    def to_google_format(self):
        """
        :return: Representation of an event as body of google calendar event
        """
        return {
            'htmlLink': self.url,
            'updated': self.updated,
            'summary': self.summary,
            'description': self.description,
            'location': self.location,
            'start': {'dateTime': self.datetime,
                      'timeZone': 'Asia/Jerusalem'}
                }

    def __repr__(self):
        """
        Representation of an event contains title, start date and location.
        """
        return 'title: ' + self.summary + ', start_date: ' + str(self.datetime) + ', location: ' + self.location + '\n'
