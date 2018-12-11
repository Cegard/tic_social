__author__ = "Eduardo Galeano"
__email__ = "cegard689@gmail.com"

import datetime
from helpers import spliter, validation_result


def __validate_date_format(field):
	is_date_format = True
	message = None
	
	try:
		datetime.datetime.strptime(field, '%Y-%m-%d').date().isoformat()
	
	except:
		is_date_format = False
		message = "field '{column}' is not on yyyy-mm-dd format".format(column = field)
	
	return validation_result(is_date_format, message)

__formats = {
	"date": __validate_date_format
}

def __validate_length(field, min_length, max_length):
	field_length = len(field)
	is_in_limits = True if field_length >= min_length and field_length <= max_length else False
	message = "field '{column}' out of bounds".format(column = field) \
			if not is_in_limits else None
	
	return validation_result(is_in_limits, message)

def __validate_format(field, format_type):
	
	return __formats[format_type](field)

def __validate_values(field, values):
	is_field_in_values = True if field in values else False
	message = None if is_field_in_values else \
		   "field '{column}' is not in the values {options}". \
		   format(column = field, options = values)
	
	return validation_result(is_field_in_values, message)

def __validate_custom_rules(field, custom_function, custom_args):
	
	return custom_function(**custom_args)(field)

__length_validation = lambda min_length, max_length : \
					  lambda field : __validate_length(field, min_length, max_length)
__format_validation = lambda format_type : \
					  lambda field : __validate_format(field, format_type)
__values_validation = lambda values : \
					  lambda field : __validate_values(field, values)
__custom_validation = lambda custom_function, custom_args : \
					  lambda field : __validate_custom_rules(field, custom_function, custom_args)

validations = {
	"length": __length_validation,
	"format": __format_validation,
	"values": __values_validation,
	"custom": __custom_validation,
}