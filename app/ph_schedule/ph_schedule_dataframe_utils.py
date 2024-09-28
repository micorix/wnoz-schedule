import polars as pl


def dedupe_list_with_order(list_str: list[str]):
    seen = set()
    result = []
    for item in list_str:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


WHITE_COLOR = "255 255 255"


class PhScheduleDataframeUtils:
    @staticmethod
    def fill_cells_with_same_bg(
        data_matrix_df: pl.DataFrame, formatting_matrix_df: pl.DataFrame
    ) -> pl.DataFrame:
        for i in range(data_matrix_df.shape[0]):
            for j in range(data_matrix_df.shape[1]):
                data_cell = data_matrix_df.item(i, j)
                formatting_cell = formatting_matrix_df.item(i, j)

                if formatting_cell is None or formatting_cell == WHITE_COLOR:
                    continue

                merged_content_candidate = [data_cell]

                offset_formatting_cell = formatting_cell

                is_artificial_merged_cell = False

                offset = 1
                while i + offset + 1 < data_matrix_df.shape[0]:
                    prev_formatting_cell = offset_formatting_cell
                    offset_data_cell = data_matrix_df.item(i + offset, j)
                    offset_formatting_cell = formatting_matrix_df.item(i + offset, j)

                    does_formatting_match = (
                        offset_formatting_cell
                        and offset_formatting_cell == prev_formatting_cell
                    )

                    if does_formatting_match:
                        merged_content_candidate.append(offset_data_cell)
                        offset += 1

                    if not does_formatting_match:
                        # mark as merged cell if at least last 2 cells have different content
                        is_artificial_merged_cell = (
                            len(set(merged_content_candidate)) > 1
                        )
                        break

                merged_value = " ".join(
                    dedupe_list_with_order(merged_content_candidate)
                )
                if offset > 1 and is_artificial_merged_cell:
                    for k in range(offset):
                        data_matrix_df[i + k, j] = merged_value
        return data_matrix_df
