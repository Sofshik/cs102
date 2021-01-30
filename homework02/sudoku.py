import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    blockRow = pos[0] // 3
    blockCol = pos[1] // 3
    return [
        grid[i][p]
        for i in range(blockRow * 3, blockRow * 3 + 3)
        for p in range(blockCol * 3, blockCol * 3 + 3)
    ]


def get_diags(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Optional[tp.Union[tp.List[tp.List[str]], tp.List[str]]]:
    """Возвращает все значения для диагональных линий для позиции pos при их наличии
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    None
    >>> get_block(grid, (4, 4))
    [['5', '.', '8', '.', '.', '.', '2', '.', '.'],['.', '.', '.', '.', '.', '.', '.', '.', '.']]
    >>> get_block(grid, (8, 8))
    ['5', '.', '8', '.', '.', '.', '2', '.', '.']
    """
    firstDiag = []
    secondDiag = []
    for i in range(9):
        firstDiag.append(grid[i][i])
        secondDiag.append(grid[i][(i - 8) * -1])
    if pos == [4, 4]:
        diags = [firstDiag, secondDiag]
        return diags
    elif pos[0] == pos[1]:
        return firstDiag
    elif pos[0] == (pos[1] - 8) * -1:
        return secondDiag
    else:
        return None


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for m in range(len(grid)):
        currentRow = grid[m]
        for l in range(len(currentRow)):
            symbol = currentRow[l]
            if symbol == ".":
                position = m, l
                return position
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Union[tp.Set[str], None]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values = set()
    for i in range(1, 10):
        a = str(i)
        if (
            (a not in get_row(grid, pos))
            and (a not in get_col(grid, pos))
            and (a not in get_block(grid, pos))
        ):
            values.add(a)
    if not values:
        return None
    return values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    position = find_empty_positions(grid)
    if not position:
        return grid
    values = find_possible_values(grid, position)
    if values:
        for i in values:
            grid[position[0]][position[1]] = i
            solution = solve(grid)
            if solution:
                return solution
            grid[position[0]][position[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(0, 9):
        for j in range(0, 9):
            pos = (i, j)
            if solution[i][j] == ".":
                return False
            if len(set(get_row(solution, pos))) != len(get_row(solution, pos)) or len(
                set(get_col(solution, pos))
            ) != len(get_col(solution, pos)):
                return False
            diags = get_diags(solution, pos)
            if diags:
                if pos == (4, 4):
                    if len(diags[0]) != len(set(diags[0])) or len(diags[1]) != len(set(diags[1])):
                        return False
                if len(diags) != len(set(diags)):
                    return False
                if solution[i][j] in set(diags):
                    return False
    for r in (0, 3, 6):
        for c in (0, 3, 6):
            if len(set(get_block(solution, (r, c)))) != len(get_block(solution, (r, c))):
                return False
    return True


def generate_sudoku(N: int) -> tp.Optional[tp.List[tp.List[str]]]:
    """Генерация судоку заполненного на N элементов
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
    grid = [["."] * 9 for _ in range(9)]
    sud = solve(grid)
    if sud:
        N = 81 - min(81, max(0, N))
        while N:
            row = random.randrange(0, 9)
            col = random.randrange(0, 9)
            if sud:
                line = sud[row]
            if line:
                if line[col] != ".":
                    line[col] = "."
                    N -= 1
    return sud


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt", "hard_puzzles.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
