from typing import List, Any
from pathlib import Path

def appendProgramFromFile(instruction_list: List[str], filename: str) -> None:
    """
    Wczytuje plik z kodem prostego języka i
    dokleja każdą niepustą linię jako string do instruction_list.
    """
    BASE_DIR = Path(__file__).parent.parent

    input_path = BASE_DIR / "fun"


    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                instruction_list.append(line)

def constructNumberInH(num : int,instruction_list: List[str]):
    instruction_list.append("RST h")

    binary = ""

    while num > 0:
        binary = str(num % 2) + binary
        num = num // 2

    for c in binary:
        instruction_list.append("SHL h")
        if c=='1':
            instruction_list.append("INC h")
