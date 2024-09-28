import re
from datetime import datetime

import pytz
from ics import Event as IcsEvent

from app.ph_schedule.ph_schedule_legend import PhScheduleLegend

SCHEDULE_TIME_REGEXES = [
    r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}),*",
    r"(\d{2}\.\d{2})\s*-\s*(\d{2}\.\d{2}),*",
]
SCHEDULE_TIME_FORMATS = ["%H:%M", "%H.%M"]

LOCATION_REGEXES = [r"s\.\s+\d.*", r"sala.*"]

REMOVE_FROM_TITLE_REGEXES = [
    *SCHEDULE_TIME_REGEXES,
    *LOCATION_REGEXES,
    r"wykłady realizowane.*",
    r"wykład realizowany.*",
    r"wykłady odbywać się będą na platformie MS Teams",
    r"g\.",
    r"(,|-)",
    r"(wykłady|wykład)",
]


class PhScheduleActivity:
    raw_title: str

    seminar_group: str
    exercise_group: str

    title: str
    description: str
    location: str

    start_date: datetime
    end_date: datetime

    legend: PhScheduleLegend = None

    def __init__(
        self,
        title: str,
        start_slot: str,
        end_slot: str,
        date: datetime,
        seminar_group: str,
        exercise_group: str,
        legend: PhScheduleLegend = None,
    ):
        self.raw_title = title.strip()

        self.seminar_group = seminar_group.strip()
        self.exercise_group = exercise_group.strip()

        self.legend = legend

        self._parse_slots(date, start_slot, end_slot)
        self._fix_times()
        self._fix_tz()
        self._prepare_title()

    def _prepare_title(self):
        self.title = self.raw_title

        is_lecture = "wykład" in self.title.lower()

        for regex in REMOVE_FROM_TITLE_REGEXES:
            self.title = re.sub(regex, "", self.title).strip()

        word_split = self.title.split(" ")
        if self.legend and len(word_split) > 0:
            first_word = word_split[0].strip()
            legend_entry = self.legend.get_mapping().get(first_word)
            if legend_entry:
                self.title = self.title.replace(first_word, legend_entry["full_name"])

        self.title = " ".join(self.title.split()).strip()

        if is_lecture:
            self.title = f"{self.title} (wykład)"

    def _prepare_description(self):
        self.description = f"""
        {self.raw_title}
        Seminar group: {self.seminar_group}
        Exercise group: {self.exercise_group}
        """

    def _parse_time(self, slot: str, is_end: bool = False):
        time = slot.split("-")[int(is_end)].strip()
        time = f"{time[:2]}:{time[2:]}"
        return datetime.strptime(time, "%H:%M").time()

    def _fix_tz(self):
        # set to Warsaw
        local_tz = "Europe/Warsaw"

        self.start_date = pytz.timezone(local_tz).localize(self.start_date)
        self.end_date = pytz.timezone(local_tz).localize(self.end_date)

    def _parse_slots(self, date: datetime, start_slot: str, end_slot: str):
        self.start_date = datetime.combine(
            date, self._parse_time(start_slot, is_end=False)
        )
        self.end_date = datetime.combine(date, self._parse_time(end_slot, is_end=True))

    def _fix_times(self):
        # sometimes activities do not happen exactly between 2 slots
        # time regex HH:MM-HH:MM and spaces around hyphen can be optional

        title_match = None
        time_format = None
        for i, time_regex in enumerate(SCHEDULE_TIME_REGEXES):
            title_match = re.match(time_regex, self.raw_title)
            if title_match:
                time_format = SCHEDULE_TIME_FORMATS[i]
                break

        if not title_match:
            return

        inferred_start_time = datetime.strptime(
            title_match.group(1), time_format
        ).time()
        inferred_end_time = datetime.strptime(title_match.group(2), time_format).time()
        inferred_start_date = datetime.combine(self.start_date, inferred_start_time)
        inferred_end_date = datetime.combine(self.end_date, inferred_end_time)

        if self.start_date != inferred_start_date:
            self.start_date = inferred_start_date

        if self.end_date != inferred_end_date:
            self.end_date = inferred_end_date

    def serialize(self):
        return {
            "title": self.title,
            "seminar_group": self.seminar_group,
            "exercise_group": self.exercise_group,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }

    def to_ics_event(self):
        return IcsEvent(
            name=self.title,
            begin=self.start_date,
            end=self.end_date,
        )

    def __repr__(self):
        return f"{self.title} ({self.start_date.isoformat()} - {self.end_date.isoformat()})"
