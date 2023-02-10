"""
Transfoms date
"""
from datetime import datetime
import apache_beam as beam


def convert_date(date_string):
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d %B %Y'):
        try:
            date_obj = datetime.strptime(date_string, fmt)
            date = date_obj.strftime("%Y-%m-%d")
            return date
        except ValueError:
            pass

class ConvertDateFormat(beam.DoFn):
    def process(self, element):
        if isinstance(element, dict):
            date_string = element.get('date', None)
            converted_date = convert_date(date_string)
            element["date"] = converted_date
            yield element

        elif isinstance(element, list):
            for elem in element:
                date_string = elem.get('date', None)
                converted_date = convert_date(date_string)
                elem["date"] = converted_date
                yield elem