__author__ = "Eduardo Galeano"
__email__ = "cegard689@gmail.com"

from collections import namedtuple

validation_result = namedtuple("Validation_Result", ["is_ok", "message"])
spliter = lambda char_spliter : lambda line : line.split(char_spliter)
default_ok_validator = lambda field : validation_result(True, None)

def format_message(message, result_message, line_consecutive):
	line_message = "{row_message} on consecutive {consecutive};".\
			format(row_message = result_message, consecutive = line_consecutive) if \
			result_message else ""
	
	return "{previous_message} {result_message}". \
			format(previous_message = message, result_message = line_message). \
			strip()