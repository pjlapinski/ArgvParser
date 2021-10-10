# Python Argv Parser

A tool that provides an API to handle command line arguments easier. It is vaguely based on [Go flag package](https://pkg.go.dev/flag)

```python
import argv_parser
import sys

bool_flag = argv_parser.bool_flag('bool', 'A flag that tests a boolean')
int_flag = argv_parser.int_flag('int', 0, 'A flag that tests an integer', required=True)
float_flag = argv_parser.float_flag('float', 0.0, 'A flag that tests a floating point value')
str_flag = argv_parser.str_flag('str', '', 'A flag that tests a string')

if argv_parser.help_flag_present(sys.argv):
    print('Usage: program_name [Options]')
    print('\nAn elaborate description of the program')
    print('Options:')
    argv_parser.print_help()
    exit(0)

argv_parser.parse_flags(sys.argv)

print(bool_flag.value)
print(int_flag.value)
print(float_flag.value)
print(str_flag.value)
```
