import re
import csv


class DataIngestion:
    """A helper class which contains the logic to translate the file into
    a format BigQuery will accept."""

    def parse_method(self, string_input, columns):
        """This method translates a single line of comma separated values to a
        dictionary which can be loaded into BigQuery.
         """
        if string_input == '\t':
            return None
        values = csv.reader([string_input], skipinitialspace=True)
        return dict(zip(columns, next(values)))