from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, TypeVar, Generic
import re


T = TypeVar('T')
__FlagValue = Union[int, str, bool, float]


class FlagType(Enum):
    INT = auto()
    FLOAT = auto()
    STR = auto()
    BOOL = auto()
    REGEX = auto()


@dataclass
class Flag(Generic[T]):
    value: T
    required: bool
    typ: FlagType
    name: str
    default: T
    description: str
    regex: str


FLAGS: list[Flag] = []


def int_flag(name: str, description: str, default: int = 0, required: bool = False) -> Flag[int]:
    """
    Defines a flag, whose value is of type int.

    :param str name: the name of the flag, which will be searched. The name will be appended with a '-' when searching through argv
    :param str description: the description of the flag that will appear when the 'print_help' function is called
    :param int default: the default value of the parameter, for when it wasn't present in argv
    :param bool required: should 'parse_flags' function throw an error, when this flag is not present
    :return: a value of class Flag, whose .value field will be populated after calling the 'parse_flags' function
    """
    return __new_flag(name, default, description, FlagType.INT, required)


def str_flag(name: str, description: str, default: str = '', required: bool = False) -> Flag[str]:
    """
    Defines a flag, whose value is of type str.

    :param str name: the name of the flag, which will be searched. The name will be appended with a '-' when searching through argv
    :param str description: the description of the flag that will appear when the 'print_help' function is called
    :param str default: the default value of the parameter, for when it wasn't present in argv
    :param bool required: should 'parse_flags' function throw an error, when this flag is not present
    :return: a value of class Flag, whose .value field will be populated after calling the 'parse_flags' function
    """
    return __new_flag(name, default, description, FlagType.STR, required)


def regex_flag(name: str, description: str, regex: str = r'.+', default: str = '', required: bool = False) -> Flag[str]:
    """
    Defines a flag, whose value is of type str, that matchex the given regex input.

    :param str name: the name of the flag, which will be surrounded with '[ ]' in the 'print_help' function
    :param str description: the description of the flag that will appear when the 'print_help' function is called
    :param str regex: the input that will be matched when searching through argv
    :param str default: the default value of the parameter, for when it wasn't present in argv
    :param bool required: should 'parse_flags' function throw an error, when this flag is not present
    :return: a value of class Flag, whose .value field will be populated after calling the 'parse_flags' function
    """
    return __new_flag(name, default, description, FlagType.REGEX, required, regex)


def bool_flag(name: str, description: str) -> Flag[bool]:
    """
    Defines a flag, whose value is of type bool.

    :param str name: the name of the flag, which will be searched. The name will be appended with a '-' when searching through argv
    :param str description: the description of the flag that will appear when the 'print_help' function is called
    :return: a value of class Flag, whose .value field will be populated after calling the 'parse_flags' function
    """
    return __new_flag(name, False, description, FlagType.BOOL, False)


def float_flag(name: str, description: str, default: float = 0.0, required: bool = False) -> Flag[float]:
    """
    Defines a flag, whose value is of type float.

    :param str name: the name of the flag, which will be searched. The name will be appended with a '-' when searching through argv
    :param str description: the description of the flag that will appear when the 'print_help' function is called
    :param float default: the default value of the parameter, for when it wasn't present in argv
    :param bool required: should 'parse_flags' function throw an error, when this flag is not present
    :return: a value of class Flag, whose .value field will be populated after calling the 'parse_flags' function
    """
    return __new_flag(name, default, description, FlagType.FLOAT, required)


def help_flag_present(argv: list[str], flag_name: str = 'help') -> bool:
    """
    Checks if a help flag is present in argv.

    :param argv: sys.argv
    :param flag_name: the name, which will be prefixed with '-', that is a help flag. The default value is 'help'
    :return: if the help flag is present
    """
    return any([arg == f'-{flag_name}' for arg in argv])


def __new_flag(name: str, default: __FlagValue, description: str, typ: FlagType, required: bool, regex: str = '') -> Flag[T]:
    global FLAGS
    flag = Flag(default, required, typ, name, default, description, regex)
    FLAGS.append(flag)
    return flag


def parse_flags(argv: list[str]) -> None:
    """
    Parses argv and populates any .value fields of defined flags

    :param argv: sys.argv
    """
    flags = FLAGS[:]
    program_argv = argv[1:]
    while (argc := len(program_argv)) > 0:
        arg = program_argv.pop(0)
        argc -= 1
        if arg[0] != '-':
            # regex flags
            for i, flag in enumerate(flags):
                if flag.typ == FlagType.REGEX and re.match(flag.regex, arg):
                    flags.pop(i)
                    flag.value = arg
                    break
            else:
                raise ValueError(f'Expected a flag, got {arg} instead.')
            continue
        flag_idx = next((i for i, v in enumerate(flags) if v.name == arg[1:]), -1)
        if flag_idx == -1:
            raise ValueError(f'Unknown flag: {arg}.')
        flag = flags.pop(flag_idx)
        # bool flags
        if flag.typ is FlagType.BOOL:
            flag.value = True
            continue
        if argc == 0:
            raise ValueError(f'Flag mismatch: no value for the {arg} flag.')
        value = program_argv.pop(0)
        # int flags
        if flag.typ == FlagType.INT:
            try:
                flag.value = int(value)
            except Exception as e:
                raise TypeError(f'Type mismatch: {arg} flag expects an int.') from e
        # float flags
        if flag.typ == FlagType.FLOAT:
            try:
                flag.value = float(value)
            except Exception as e:
                raise TypeError(f'Type mismatch: {arg} flag expects a float.') from e
        # str flags
        else:
            flag.value = value
    for flag in flags:
        if flag.required:
            raise ValueError(f'The -{flag.name} flag is required.')


def print_help() -> None:
    """
    Prints the usage of all defined flags
    """
    for flag in FLAGS:
        is_bool = flag.typ == FlagType.BOOL
        is_regex = flag.typ == FlagType.REGEX
        if is_regex:
            print(f'     [{flag.name}]:')
        else:
            print(f'    -{flag.name}{(":" if is_bool else " <value>:")}')
        print(f'        {flag.description}')
        if is_bool or is_regex:
            continue
        if flag.typ == FlagType.STR:
            print(f"        Default: '{flag.default}'")
        else:
            print(f"        Default: {flag.default}")
