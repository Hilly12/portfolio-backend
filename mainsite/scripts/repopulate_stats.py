import json
import pytz
import datetime
from stocks.models import Statistics


def run():
    entries = []
    with open("_temp/stats.json", "r") as f:
        entries = json.load(f)

    for entry in entries:
        entry.update({"timestamp": pytz.utc.localize(datetime.datetime.now())})

    Statistics.objects.all().delete()
    Statistics.objects.bulk_create(entries)

    print("Saved entries to database.")
