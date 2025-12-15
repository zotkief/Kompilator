from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class declaration:
    dataStart       : int
    dataEnd         : int
    isTable         : bool
    varName         : str
    indexStart      : int
    writable        : bool
    readable        : bool
    

@dataclass
class programm_all:
    instruction_list: List[str]

@dataclass
class procedures:
    instruction_list: List[str]

@dataclass
class declarations:
    identifierHashMap={}


@dataclass
class commands:
    comms: List['command'] = field(default_factory=list)

@dataclass
class main:
    decs : declarations
    comms : commands

@dataclass
class proc_head:
    instruction_list: List[str]

@dataclass
class command:
    commType    : str
    arguments    : List[Any]

@dataclass
class identifier:
    isTable: bool = False
    name: str = ""
    index: int | str = 0


@dataclass
class value:
    val : int|identifier

@dataclass
class expression:
    isDouble    : bool
    val1        : value
    val2        : value
    operation   : str


@dataclass
class condition:
    val1        : value
    val2        : value
    operation   : str


@dataclass
class args:
    instruction_list: List[str]