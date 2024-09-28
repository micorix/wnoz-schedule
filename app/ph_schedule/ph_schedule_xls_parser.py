import xlrd
from xlrd import Book
from xlrd.sheet import Cell, Sheet


class PhScheduleXLSParser:
    wb: Book
    ws: Sheet
    data_matrix: list[list[str]] = None
    formatting_matrix: list[list[str]] = None

    def __init__(self, file_path):
        self.wb = xlrd.open_workbook(file_path, formatting_info=True)
        self.ws = self.wb.sheet_by_index(1)  # Arkusz2

    def _get_cell_fill_color(self, cell: Cell) -> str | None:
        xf = self.wb.xf_list[cell.xf_index]
        if not xf.background:
            return None

        color = self.wb.colour_map.get(xf.background.pattern_colour_index)
        if not color:
            return None

        return " ".join(map(str, color))

    def _create_matrix_from_sheet(self, empty=False):
        return [
            [
                None if empty else self.ws.cell_value(row, col)
                for col in range(self.ws.ncols)
            ]
            for row in range(self.ws.nrows)
        ]

    def _create_formatting_matrix(self):
        self.formatting_matrix = self._create_matrix_from_sheet(empty=True)

        for row in range(self.ws.nrows):
            for col in range(self.ws.ncols):
                cell = self.ws.cell(row, col)
                bg_color = self._get_cell_fill_color(cell)
                if cell.value and bg_color:
                    self.formatting_matrix[row][col] = bg_color

    def _create_data_matrix(self):
        self.data_matrix = self._create_matrix_from_sheet(empty=False)

        for row_start, row_end, col_start, col_end in self.ws.merged_cells:
            merged_value = self.ws.cell_value(row_start, col_start)
            bg_color = self._get_cell_fill_color(self.ws.cell(row_start, col_start))

            # Fill all the cells in the merged range with this value
            for row in range(row_start, row_end):
                for col in range(col_start, col_end):
                    self.data_matrix[row][col] = merged_value
                    self.formatting_matrix[row][col] = bg_color

    def get_data_matrix(self):
        if not self.data_matrix or not self.formatting_matrix:
            self._create_formatting_matrix()
            self._create_data_matrix()
        return self.data_matrix

    def get_formatting_matrix(self):
        if not self.data_matrix or not self.formatting_matrix:
            self._create_formatting_matrix()
            self._create_data_matrix()
        return self.formatting_matrix
