__author__ = "Eduardo Galeano"
__email__ = "cegard689@gmail.com"

import sys
from validator import validate_file

if __name__ == "__main__":
	print(validate_file(sys.argv[1]))