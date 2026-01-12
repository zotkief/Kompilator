import curses
import sys
import copy

REG_NAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
MEM_SIZE = 263
MEM_VIEW = 30


class VMError(Exception):
    pass


class VM:
    def __init__(self, program, input_data):
        self.program = program
        self.input_data = input_data
        self.reset()

    def reset(self):
        self.reg = {r: 0 for r in REG_NAMES}
        self.mem = [0] * MEM_SIZE
        self.k = 0
        self.halted = False
        self.input_ptr = 0

    def snapshot(self):
        return {
            'k': self.k,
            'reg': copy.deepcopy(self.reg),
            'mem': self.mem[:],
            'halted': self.halted
        }

    def step(self):
        if self.halted:
            return

        if self.k < 0 or self.k >= len(self.program):
            raise VMError(f"Invalid instruction pointer: {self.k}")

        instr, arg = self.program[self.k]

        def rx(x):
            if x not in self.reg:
                raise VMError(f"Invalid register: {x}")
            return self.reg[x]

        def set_rx(x, v):
            if x not in self.reg:
                raise VMError(f"Invalid register: {x}")
            self.reg[x] = max(v, 0)

        if instr == "READ":
            if self.input_ptr >= len(self.input_data):
                raise VMError("READ: brak danych wejściowych")
            self.reg['a'] = self.input_data[self.input_ptr]
            self.input_ptr += 1
            self.k += 1

        elif instr == "WRITE":
            print(self.reg['a'])
            self.k += 1

        elif instr == "LOAD":
            self.reg['a'] = self.mem[arg]
            self.k += 1

        elif instr == "STORE":
            self.mem[arg] = self.reg['a']
            self.k += 1

        elif instr == "RLOAD":
            self.reg['a'] = self.mem[rx(arg)]
            self.k += 1

        elif instr == "RSTORE":
            self.mem[rx(arg)] = self.reg['a']
            self.k += 1

        elif instr == "ADD":
            self.reg['a'] += rx(arg)
            self.k += 1

        elif instr == "SUB":
            self.reg['a'] = max(self.reg['a'] - rx(arg), 0)
            self.k += 1

        elif instr == "SWP":
            self.reg['a'], self.reg[arg] = self.reg[arg], self.reg['a']
            self.k += 1

        elif instr == "RST":
            set_rx(arg, 0)
            self.k += 1

        elif instr == "INC":
            set_rx(arg, rx(arg) + 1)
            self.k += 1

        elif instr == "DEC":
            set_rx(arg, rx(arg) - 1)
            self.k += 1

        elif instr == "SHL":
            set_rx(arg, 2 * rx(arg))
            self.k += 1

        elif instr == "SHR":
            set_rx(arg, rx(arg) // 2)
            self.k += 1

        elif instr == "JUMP":
            self.k = arg

        elif instr == "JPOS":
            self.k = arg if self.reg['a'] > 0 else self.k + 1

        elif instr == "JZERO":
            self.k = arg if self.reg['a'] == 0 else self.k + 1

        elif instr == "CALL":
            self.reg['a'] = self.k + 1
            self.k = arg

        elif instr == "RTRN":
            self.k = self.reg['a']

        elif instr == "HALT":
            self.halted = True

        else:
            raise VMError(f"Unknown instruction: {instr}")


def parse_program(path):
    program = []
    with open(path) as f:
        for line in f:
            line = line.split('#')[0].strip()
            if not line:
                continue
            parts = line.split()
            instr = parts[0].upper()
            arg = None
            if len(parts) == 2:
                p = parts[1]
                arg = int(p) if p.isdigit() else p
            program.append((instr, arg))
    return program


def parse_input(path):
    data = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            data.append(int(line))
    return data


def draw(stdscr, before, after, program):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    instr = program[before['k']] if before['k'] < len(program) else ("<END>", None)

    stdscr.addstr(0, 0, f"Instrukcja k={before['k']}: {instr}")
    stdscr.addstr(1, 0, "=" * (w - 1))

    col_w = w // 4
    base_y = 3

    titles = [
        "PAMIĘĆ PRZED",
        "REJESTRY PRZED",
        "PAMIĘĆ PO",
        "REJESTRY PO"
    ]

    for i, t in enumerate(titles):
        stdscr.addstr(base_y, i * col_w, t.center(col_w - 1))

    stdscr.addstr(base_y + 1, 0, "-" * (w - 1))

    def draw_mem(st, col):
        for i in range(MEM_VIEW):
            y = base_y + 2 + i
            if y >= h - 2:
                break
            stdscr.addstr(
                y,
                col * col_w,
                f"p[{i:02}] = {st['mem'][i]}".ljust(col_w - 1)
            )

    def draw_regs(st, col):
        for i, r in enumerate(REG_NAMES):
            y = base_y + 2 + i
            if y >= h - 2:
                break
            stdscr.addstr(
                y,
                col * col_w,
                f"{r} = {st['reg'][r]}".ljust(col_w - 1)
            )

    draw_mem(before, 0)
    draw_regs(before, 1)
    draw_mem(after, 2)
    draw_regs(after, 3)

    stdscr.addstr(
        h - 1,
        0,
        "→ : krok   ← : cofanie   q : wyjście"
    )
    stdscr.refresh()


def main(stdscr, program, input_data):
    curses.curs_set(0)

    vm = VM(program, input_data)
    history = [vm.snapshot()]
    idx = 0

    while True:
        before = history[idx]
        after = history[idx + 1] if idx + 1 < len(history) else before

        draw(stdscr, before, after, program)
        key = stdscr.getch()

        if key == curses.KEY_RIGHT:
            if idx + 1 < len(history):
                idx += 1
            else:
                vm.step()
                history.append(vm.snapshot())
                idx += 1

        elif key == curses.KEY_LEFT and idx > 0:
            idx -= 1

        elif key == ord('q'):
            break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 vm_simulator.py program.txt input.txt")
        sys.exit(1)

    program = parse_program(sys.argv[1])
    input_data = parse_input(sys.argv[2])
    curses.wrapper(main, program, input_data)
