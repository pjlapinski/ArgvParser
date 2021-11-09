# Python Argv Parser

A tool that provides an API to handle command line arguments easier. It is vaguely based on [Go flag package](https://pkg.go.dev/flag)

## Note:
The regex flag is different than the others. When defined with a name, instead of searching for '-[name]' in argv, 
the flag will only try to find a string matching a given regex, i.e.

```python
regex_flag('name', 'description', r'.+\.py')
```

will not match on '-name'. Instead it will search argv for any string ending with '.py'. The name of a regex flag
is used only for documentation, in case the '-help' flag is present in argv.

## Example use:

```python
import argv_parser
import sys

bool_flag = argv_parser.bool_flag('bool', 'A flag that tests a boolean')
int_flag = argv_parser.int_flag('int', 'A flag that tests an integer', default=1, required=True)
float_flag = argv_parser.float_flag('float', 'A flag that tests a floating point value')
str_flag = argv_parser.str_flag('str', 'A flag that tests a string', default='empty')
regex_flag = argv_parser.regex_flag('regex', 'A flag that tests for a string matching a regex', regex=r'.+\.py')

if argv_parser.help_flag_present(sys.argv):
    print('Usage: program_name [Options]')
    print('\nAn elaborate description of the program')
    print('Options:')
    argv_parser.print_help()
    exit(0)

argv_parser.parse_flags(sys.argv)

print(f'{bool_flag.value=}')
print(f'{int_flag.value=}')
print(f'{float_flag.value=}')
print(f'{str_flag.value=}')
print(f'{regex_flag.value=}')
```
