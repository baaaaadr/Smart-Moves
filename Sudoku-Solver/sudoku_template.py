"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.1.1
licence: WTFPL <https://www.wtfpl.net/txt/copying/>
"""

import subprocess
from model import model
from TP3 import generate_problem
from TP3 import clauses_to_dimacs
from TP3 import model_to_grid
from TP3 import print_grid

# alias de types
Grid = list[list[int]]
PropositionalVariable = int
Literal = int
Clause = list[Literal]
ClauseBase = list[Clause]
Model = list[Literal]

example: Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]


empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#### fonctions fournies


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(filename: str, cmd: str = r"C:/Users/bdrak/Desktop/GI02/IA02/TP_3_Sudoku_Nics/gophersat.exe", encoding: str = "utf8") -> tuple[bool, list[int]]:
    try:
        result = subprocess.run(
            [cmd, filename], capture_output=True, check=True, encoding=encoding
        )
    except subprocess.CalledProcessError as e:
        print("Error executing gophersat:", e.stderr)  # Print the error message
        return False, []

    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")
    return True, [int(x) for x in model]

def main():
    grid = example
    clauses = generate_problem(grid)
    dimacs = clauses_to_dimacs(clauses, 729)  # 9 * 9 * 9 variables
    write_dimacs_file(dimacs, "sudoku.cnf")

    satisfiable, model = exec_gophersat("sudoku.cnf")

    if satisfiable:
        solved_grid = model_to_grid(model)
        print("Solved Sudoku Grid:")
        print_grid(solved_grid)  # Display the solved grid
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()