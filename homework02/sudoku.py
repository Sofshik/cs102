from typing import Tuple, List, Set, Optional


def read_sudoku(filename: str) -> List[List[str]]:
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    rawGroup = []
    for i in range (0, len(values), n):
        rawGroup.append(values[i:i+n])
    return(rawGroup)

def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    row = pos[0]
    return(grid[row])

def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    col = pos[1]
    column = []
    for i in range(len(grid)):
        currentRow = grid[i]
        column.append(currentRow[col])
    return(column)

def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    blockRow = pos[0] // 3
    blockCol = pos[1] // 3
    block = []
    for i in range(blockRow * 3, blockRow * 3 + 3):
        line = grid[i]
        for p in range(blockCol * 3, blockCol * 3 + 3):
            block.append(line[p])
    return(block)

def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    for m in range(len(grid)):
        currentRow = grid[m]
        for l in range(len(currentRow)):
            symbol = currentRow[l]
            if symbol == '.':
                position = [m, l]
                return(position)


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    myRow = get_row(grid, pos)
    myCol = get_col(grid, pos)
    myBlock = get_block(grid, pos)
    values = set()
    for a in range(1, 10):
        a = str(a)
        if (a not in myRow) and (a not in myCol) and (a not in myBlock):
            values.add(a)
    return(values)

def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    position = find_empty_positions(grid)
    if position == None:
        return(grid)
    else:
        values = find_possible_values(grid, position)
        for i in values:
                row = position[0]
                col = position[1]
                grid[row][col] = i
                solution = solve(grid)
                if solution:
                    return(solution)
                grid[row][col] = '.'

def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    pass


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    pass


#if __name__ == '__main__':
    #for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        #grid = read_sudoku(fname)
        #display(grid)
        #solution = solve(grid)
        #if not solution:
            #print(f"Puzzle {fname} can't be solved")
        #else:
            #display(solution)
