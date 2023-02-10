"""Data ingestion"""
import re
import csv


class DataIngestion:
    """Transform data to a BigQuery format."""

    def parse_method(self, string_input, columns):
        """Parse csv data to a dictionary which can be loaded into BigQuery."""
        if string_input == '\t':
            return None
        values = csv.reader([string_input], skipinitialspace=True)
        return dict(zip(columns, next(values)))