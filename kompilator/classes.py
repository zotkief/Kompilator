from dataclasses import dataclass, field
from typing import List, Any, Tuple

@dataclass
class declaration:
    dataStart           : int
    dataEnd             : int
    isTable             : bool
    varName             : str
    indexStart          : int
    writable            : bool
    readable            : bool
    isRefrence          : bool
    refrencedIdentifier : str
    

@dataclass
class programm_all:
    instruction_list: List[str]

@dataclass
class declarations:
    identifierHashMap: dict = field(default_factory=dict)


@dataclass
class commands:
    comms: List[Any] = field(default_factory=list)

@dataclass
class main:
    decs : declarations
    comms : commands

@dataclass
class proc_head:
    proc_name : str
    args_tab: List[Tuple[type, str]]

@dataclass
class proc_call:
    proc_name : str
    args_list: List[str]

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
class type:
    t : str

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
    args_list: List[str]


@dataclass
class args_decl:
    args_tab: List[Any] = field(default_factory=list)

@dataclass
class procedure:
    head: Any
    declarations: declarations = field(default_factory=declarations)
    body: Any = field(default_factory=lambda: commands([]))


@dataclass
class procedures:
    procedure_list: List[procedure] = field(default_factory=list)