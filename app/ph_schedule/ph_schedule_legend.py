import polars as pl


class PhScheduleLegend:
    data_matrix_df: pl.DataFrame
    legend: dict[str, dict[str, str]] = {}

    def __init__(self, data_matrix_df: pl.DataFrame):
        self.data_matrix_df = data_matrix_df

    def _get_legend_start_row(self):
        empty_count = 0
        threshold = 3

        for i in range(self.data_matrix_df.shape[0]):
            if not self.data_matrix_df.item(i, 0):
                empty_count += 1
            else:
                empty_count = 0
            if empty_count == threshold:
                return i - threshold + 1 + 1
        return -1

    def _parse_legend(self):
        legend = {}
        is_empty = False
        i = self._get_legend_start_row()

        while not is_empty:
            val = self.data_matrix_df.item(i, 2)
            is_empty = not val

            val = val.split("-")
            if len(val) >= 2:
                short_name = val[0].strip()
                full_name = val[1].strip()
                legend[short_name] = {
                    "short_name": short_name,
                    "full_name": full_name,
                }
            i += 1
        self.legend = legend

    def get_mapping(self):
        if not self.legend:
            self._parse_legend()
        return self.legend
