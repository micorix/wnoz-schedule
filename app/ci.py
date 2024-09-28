import os

from ics import Calendar

from app.ph_schedule.ph_schedule_downloader import PhScheduleDownloader
from app.ph_schedule.ph_schedule_reader import PhScheduleReader
import json

ARTIFACTS_DIR = os.path.join(
    os.path.dirname(__file__), "../artifacts/2024-licencjackie-stacjonarne"
)
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "../downloads")


def filter_schedules(s):
    return all(
        [
            s["Semestr"].lower() == "zimowy",
            s["Rok"] == "1",
            s["Poziom"].lower() == "licencjackie",
            s["Tryb"].lower() == "stacjonarne",
        ]
    )


def serialize_activities(activities):
    return [a.serialize() for a in activities]


def main():
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    downloader = PhScheduleDownloader()
    downloader.scrape()
    schedule_files = downloader.download(filter_schedules, DOWNLOADS_DIR)

    assert len(schedule_files) == 1, "Expected one file to be downloaded"

    filename = schedule_files[0]

    reader = PhScheduleReader(filename)
    activities_by_exercise_group = {}

    for activity in reader.read_schedule():
        if activity.exercise_group not in activities_by_exercise_group:
            activities_by_exercise_group[activity.exercise_group] = []

        activities_by_exercise_group[activity.exercise_group].append(activity)

    groups = list(activities_by_exercise_group.keys())

    for group in groups:
        activities = activities_by_exercise_group[group]

        # ensure dir
        os.makedirs(os.path.join(ARTIFACTS_DIR, group), exist_ok=True)

        # save to file
        with open(os.path.join(ARTIFACTS_DIR, group, "activities.json"), "w") as f:
            f.write(json.dumps(serialize_activities(activities), indent=2))

        calendar = Calendar()
        calendar.events = [activity.to_ics_event() for activity in activities]

        with open(os.path.join(ARTIFACTS_DIR, group, "calendar.ics"), "w") as f:
            f.write(calendar.serialize())

        print(f"{group} - {len(activities)} activities")


if __name__ == "__main__":
    main()
