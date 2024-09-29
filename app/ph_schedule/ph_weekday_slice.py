from datetime import datetime, timedelta

import polars as pl

from app.ph_schedule.ph_schedule_activity import PhScheduleActivity
from app.ph_schedule.ph_schedule_dataframe_utils import PhScheduleDataframeUtils

SLICE_Y_START_CELL_VALUE = "Tydzień"
SLICE_Y_END_CELL_VALUE = "2000-2045"


def excel_date_to_datetime(excel_date: str | float) -> datetime:
    excel_date = float(excel_date)
    base_date = datetime(1899, 12, 30)  # Excel's base date
    return base_date + timedelta(days=excel_date)


class PhWeekdaySlice:
    weekday = None
    date: datetime = None
    df: pl.DataFrame = None
    formatting_df: pl.DataFrame = None

    def __init__(self, df: pl.DataFrame, formatting_df: pl.DataFrame):
        self.weekday = df.item(1, 0)
        self.date = excel_date_to_datetime(float(df.item(1, 1)))
        self.df = pl.concat(
            [
                df.slice(0, 4),
                PhScheduleDataframeUtils.fill_cells_with_same_bg(
                    df.slice(4), formatting_df.slice(4)
                ),
            ]
        )
        self.formatting_df = formatting_df

    def get_activities(self, legend=None):
        activities = []
        rowsn, colsn = self.df.shape
        for col in range(1, colsn):
            row = 4
            while row < rowsn:
                activity = self.df.item(row, col)

                if not activity:
                    row += 1
                    continue

                offset = 1
                while row + offset < rowsn:
                    next_activity = self.df.item(row + offset, col)
                    if next_activity != activity:
                        break
                    offset += 1

                activities.append(
                    PhScheduleActivity(
                        title=activity,
                        start_slot=self.df.item(row, 0),
                        end_slot=self.df.item(row + offset - 1, 0),
                        date=excel_date_to_datetime(self.df.item(1, col)),
                        seminar_group=self.df.item(2, col),
                        exercise_group=self.df.item(3, col),
                        color=self.formatting_df.item(row, col),
                        legend=legend,
                    )
                )

                row += offset
        return activities

    @staticmethod
    def weekday_slices_from_df(data_df: pl.DataFrame, formatting_df: pl.DataFrame):

        current_start_y = None
        slices = []

        for y in range(data_df.shape[0]):
            cell_value = data_df.item(y, 0)

            if cell_value == SLICE_Y_START_CELL_VALUE:
                current_start_y = y
                continue

            if cell_value == SLICE_Y_END_CELL_VALUE and current_start_y is not None:
                slice_len = y - current_start_y + 1
                data_slice = data_df.slice(current_start_y, slice_len)
                formatting_slice = formatting_df.slice(current_start_y, slice_len)

                current_start_y = None

                slices.append(PhWeekdaySlice(data_slice, formatting_slice))
                continue
        return slices
