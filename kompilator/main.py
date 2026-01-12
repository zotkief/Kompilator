from kompilator.lexer import lexer
from kompilator.parser import parser
from pathlib import Path
import logging
import sys

def main():
    if len(sys.argv) != 3:
        print("Użycie: python main.py <plik_wejsciowy> <plik_wyjsciowy>")
        return
    
    logging.basicConfig(
        #level = logging.DEBUG,
        filename = "parser.out",
        filemode = "w"
    )

    BASE_DIR = Path(__file__).parent

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    input_path = BASE_DIR / input_filename
    output_path = BASE_DIR / output_filename

    lexer.input(open(input_path).read())

    #for tok in lexer:
    #    print(tok)


    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    result = parser.parse(content, lexer=lexer)#, debug=True)

    with open(output_path, "w", encoding="utf-8") as f:
        
        if result and hasattr(result, "instruction_list"):
            i=0
            for instr in result.instruction_list:
                f.write(instr + "\n")
                i+=1
        elif result:
            print("Kompilacja zakończona pomyślnie, ale lista instrukcji jest pusta.")
        else:
            print("Błąd parsowania. Wynik jest pusty.")


if __name__ == "__main__":
    main()
"""

from kompilator.lexer import lexer
from pathlib import Path
import sys


def main():
    if len(sys.argv) != 3:
        print("Użycie: python main.py <plik_wejsciowy> <plik_wyjsciowy>")
        return

    BASE_DIR = Path(__file__).parent

    input_path = BASE_DIR / sys.argv[1]
    output_path = BASE_DIR / sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    lexer.input(content)

    with open(output_path, "w", encoding="utf-8") as f:
        for tok in lexer:
            f.write(
                f"type={tok.type}, value={tok.value}, "
                f"line={tok.lineno}, pos={tok.lexpos}\n"
            )


if __name__ == "__main__":
    main()"""
