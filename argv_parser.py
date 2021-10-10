from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, TypeVar, Generic


T = TypeVar('T')
__FlagValue = Union[int, str, bool, float]


class FlagType(Enum):
    INT = auto()
    FLOAT = auto()
    STR = auto()
    BOOL = auto()


@dataclass
class Flag(Generic[T]):
    value: T
    required: bool
    typ: FlagType
    name: str
    default: T
    description: str


FLAGS: list[Flag] = []


def int_flag(name: str, default: int, description: str, required: bool = False) -> Flag[int]:
    return __new_flag(name, default, description, FlagType.INT, required)


def str_flag(name: str, default: str, description: str, required: bool = False) -> Flag[str]:
    return __new_flag(name, default, description, FlagType.STR, required)


def bool_flag(name: str, default: bool, description: str, required: bool = False) -> Flag[bool]:
    return __new_flag(name, default, description, FlagType.BOOL, required)


def float_flag(name: str, default: float, description: str, required: bool = False) -> Flag[float]:
    return __new_flag(name, default, description, FlagType.FLOAT, required)


def help_flag_present(argv: list[str]) -> bool:
    return any([arg == '-help' for arg in argv])


def __new_flag(name: str, default: __FlagValue, description: str, typ: FlagType, required: bool):
    global FLAGS
    flag = Flag(default, required, typ, name, default, description)
    FLAGS.append(flag)
    return flag


def parse_flags(argv: list[str]):
    flags = FLAGS[:]
    program_argv = argv[1:]
    while (argc := len(program_argv)) > 0:
        arg = program_argv.pop(0)
        argc -= 1
        if arg[0] != '-':
            raise ValueError(f'Expected a flag, got {arg} instead.')
        flag_idx = next((i for i, v in enumerate(
            flags) if v.name == arg[1:]), -1)
        if flag_idx == -1:
            raise ValueError(f'Unknown flag: {arg}.')
        flag = flags.pop(flag_idx)
        if flag.typ is FlagType.BOOL:
            flag.value = True
            return
        if argc == 0:
            raise ValueError(f'Flag mismatch: no value for the {arg} flag.')
        value = program_argv.pop(0)
        if flag.typ == FlagType.INT:
            try:
                flag.value = int(value)
            except Exception as e:
                raise TypeError(
                    f'Type mismatch: {arg} flag expects an int.') from e
        if flag.typ == FlagType.FLOAT:
            try:
                flag.value = float(value)
            except Exception as e:
                raise TypeError(
                    f'Type mismatch: {arg} flag expects an float.') from e
        else:
            flag.value = value
    for flag in flags:
        if flag.required:
            raise ValueError(f'The -{flag.name} flag is required.')


def print_help(program_description: str):
    print(program_description)
    for flag in FLAGS:
        print(f'    -{flag.name}')
        print(f'        {flag.description}')
        print(f'        Default: {flag.default}')
