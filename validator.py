__author__ = "Eduardo Galeano"
__email__ = "cegard689@gmail.com"

import datetime
from helpers import spliter, validation_result, default_ok_validator, format_message
from validations import validations

pipe_spliter = spliter('|')
__dates_bounds = {
	"min_date": datetime.datetime.strptime("1920-01-01", '%Y-%m-%d').date(),
	"max_date": datetime.datetime.now().date()
}

def __validate_date_in_bounds(min_date, max_date):
	
	def validate_date_limits(string_date):
		is_ok = True
		message = None
		
		try:
			date = datetime.datetime.strptime(string_date, '%Y-%m-%d').date()
			is_ok = True if date >= min_date and date <= max_date else False
			message = None if is_ok else "field '{column}' is not in dates limits". \
										 format(column = string_date)
		
		except:
			is_ok = False
			message = "field '{column}' is not on yyyy-mm-dd format".format(column = string_date)
		
		return validation_result(is_ok, message)
		
	return validate_date_limits

__header_rules = [
	[validations["length"](1, 999)],
	[validations["length"](9, 9)],
	[validations["format"]("date")],
	[validations["length"](1, 999)],
]

__user_rules = [
	[validations["length"](1, 999)],
	[validations["length"](9, 9)],
	[
		validations["length"](2, 2),
		validations["values"](("CC", "TI", "CE"))
	],
	[validations["length"](5, 12)],
	[validations["length"](0, 20)],
	[validations["length"](0, 20)],
	[validations["length"](0, 20)],
	[validations["length"](0, 20)],
	[
		validations["format"]("date"),
		validations["custom"](__validate_date_in_bounds, __dates_bounds)
	],
	[
		validations["length"](1, 1),
		validations["values"](("M", "F"))
	],
	[
		validations["length"](1, 3)
	],
	[default_ok_validator]
]

def __validate_gestation_state(integer_val, genre, document_type):
	is_ok = True if (integer_val == 3 and genre == "M") or \
					(integer_val == 3 and genre == "F" and document_type == "TI") or \
					(integer_val != 3 and genre == "F" and document_type != "TI") else False
	message = "gestation state doesn't correspond with the rules"
	
	return validation_result(is_ok, message)

def __validate_line(line, rules):
	is_ok = True
	message = ""
	columns = pipe_spliter(line)
	
	for i in range(len(columns)):
		
		for j in range(len(rules[i])):
			result = rules[i][j](columns[i])
			is_ok = is_ok and result.is_ok
			message = format_message(message, result.message, columns[0])
			
			if i == 10:
				custom_column_result = __validate_gestation_state(columns[10],
																  columns[9], columns[2])
				is_ok = is_ok and custom_column_result.is_ok
				message = format_message(message, custom_column_result.message, columns[0])
	
	return validation_result(is_ok, message)

def __validate_content(opened_file):
	header_line = opened_file.readline()
	is_ok, message = __validate_line(header_line, __header_rules)
	
	for user_line in opened_file:
		line_result = __validate_line(user_line, __user_rules)
		is_ok = is_ok and line_result.is_ok
		message = "{previous_message} {result_message}". \
		format(previous_message = message, result_message = line_result.message or ""). \
		strip()
	
	return validation_result(is_ok, message)

def validate_file(file_to_open):
	result = None
	
	with open(file_to_open) as file:
		result = __validate_content(file)
	file.closed
	
	return result