import os
import requests
from ics import Calendar, Event

TOKEN = os.environ["EVENTBRITE_TOKEN"]

URL = "https://www.eventbriteapi.com/v3/users/me/orders/?expand=event&page_size=100"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

calendar = Calendar()

seen = set()

while URL:

  response = requests.get(URL, headers=headers)

print(response.status_code)
print(response.text)

response.raise_for_status()

    data = response.json()

    for order in data["orders"]:

        if order["status"] != "placed":
            continue

        event = order["event"]

        event_id = event["id"]

        if event_id in seen:
            continue

        seen.add(event_id)

        e = Event()

        e.uid = event_id

        e.name = event["name"]["text"]

        e.begin = event["start"]["utc"]

        e.end = event["end"]["utc"]

        description = ""

        if event.get("summary"):
            description += event["summary"] + "\n\n"

        description += event["url"]

        e.description = description

        e.url = event["url"]

        calendar.events.add(e)

    pagination = data["pagination"]

    if pagination["has_more_items"]:
        next_page = pagination["page_number"] + 1
        URL = f"https://www.eventbriteapi.com/v3/users/me/orders/?expand=event&page={next_page}&page_size=100"
    else:
        URL = None

with open("eventbrite.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print(f"Wrote {len(calendar.events)} events.")
