from app.ph_schedule.ph_schedule_activity import PhScheduleActivity
from app.ph_schedule.ph_schedule_legend import PhScheduleLegend
from app.ph_schedule.ph_schedule_xls_parser import PhScheduleXLSParser
from app.ph_schedule.ph_weekday_slice import PhWeekdaySlice
import polars as pl


class PhScheduleReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_schedule(self):
        xls_parser = PhScheduleXLSParser(self.file_path)

        data_matrix = xls_parser.get_data_matrix()
        formatting_matrix = xls_parser.get_formatting_matrix()

        data_matrix_df = pl.DataFrame(data_matrix, strict=False).transpose()
        formatting_matrix_df = pl.DataFrame(formatting_matrix, strict=False).transpose()

        weekday_slices = PhWeekdaySlice.weekday_slices_from_df(
            data_matrix_df, formatting_matrix_df
        )

        legend = PhScheduleLegend(data_matrix_df)

        for weekday_slice in weekday_slices:
            for activity in weekday_slice.get_activities(legend):
                yield activity

    def to_ics(self, filter_func=None):
        from ics import Calendar

        calendar = Calendar()

        for activity in self.read_schedule():
            if filter_func is None or filter_func(activity):
                calendar.events.add(activity.to_ics_event())

        return calendar

    @staticmethod
    def sort_activities(activities: list[PhScheduleActivity]):
        return sorted(activities, key=lambda activity: activity.start_date)
