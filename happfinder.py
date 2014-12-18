from icalendar import Calendar, Event, vDatetime
import requests

class Happening():

	def __init__(self, component):
		self.timestamp = component.decoded('dtstamp')
		self.uid = component.get('uid')
		self.url = component.get('url')
		self.summary = component.get('summary')
		self.location = component.get('location')
		self.duration = component.decoded('duration')
		self.organizer = component.get('organizer')
		self.start = component.decoded('dtstart')
		self.description = component.get('description')

	def ascii_string(self):
		out = "%s\n" % self.timestamp
		out += "%s\n" % self.uid
		out += "%s\n" % self.url.encode('ascii', 'ignore')
		out += "%s\n" % self.summary.encode('ascii', 'ignore')
		out += "%s\n" % self.location.encode('ascii', 'ignore')
		out += "%s\n" % self.duration
		out += "%s\n" % self.organizer.encode('ascii', 'ignore')
		out += "%s\n" % self.start
		out += "%s\n" % self.description.encode('ascii', 'ignore')
		return out


class Happfinder():

	def __init__(self):
		self.cal = Calendar()
		self.update_calendar()

	def update_calendar(self):
		ical = requests.get("https://www.samfundet.no/arrangement/ical")
		if ical.status_code == 200:
			self.cal = Calendar.from_ical(ical.text)

	def find_happenings(self, **kwargs):
		happenings = []
		for component in self.cal.walk():
			if component.name == "VEVENT":
				for key, value in kwargs.items():
					if component.get(key) != value:
						if component in happenings:
							happenings.remove(component)
						continue
					else:
						if component not in happenings:
							happenings.append(component)
		for i in range(len(happenings)):
			happenings[i] = Happening(happenings[i])
		return happenings