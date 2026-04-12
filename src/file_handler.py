import csv
import pandas as pd


class FileHandler:
    def read_lines_from_file(self, filename):
        with open(filename) as f:
            return f.readlines()

    def get_lines_from_csv_file(self, filename, delimiter=","):
        with open(filename) as f:
            csv_reader = csv.reader(f, delimiter=delimiter)
            rows = [row for row in csv_reader]
        return rows

    def export_dataframe_to_csv(self, df, filename):
        return df.to_csv(filename, index=False)

    def open_xlsx_file_to_df(
        self, filename, sheet, skiprows=None, usecols=None, converters=None
    ):
        xls = pd.ExcelFile(filename)
        return pd.read_excel(
            xls, sheet, skiprows=skiprows, usecols=usecols, converters=converters
        )

    def read_csv_to_df(self, filename):
        return pd.read_csv(filename)

    def write_lines_to_file(self, filename, lines):
        with open(filename, "w") as f:
            for line in lines:
                f.write("{}\n".format(line))
