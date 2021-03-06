assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# hard code diagonal units
diagonal_units = [
    list(map(lambda x:x[0]+x[1], zip(rows, cols))),
    list(map(lambda x:x[0]+x[1], zip(rows[::-1], cols)))]

# check whether this box is a diagonal box
def is_diagonal(box_key):
    return any(box_key in dia for dia in diagonal_units)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # naked twins in row
    # first I find out how many times each digit appears in each row, store the count of each digit in dict: twins_count
    # then find out the digit only appear twice in this row, eliminate it
    for row in row_units:
        twins_count = {}
        for k in row:
            v = values[k]
            if len(v) == 2:
                if twins_count.get(v) is None:
                    twins_count[v] = 1
                else:
                    twins_count[v] += 1

        for v, count in twins_count.items():
            if count == 2:
                for k in row:
                    if values[k] == v:
                        continue
                    for i in v:
                        values[k] = values[k].replace(i, '')

    # the method for column, is all the same as the row
    # a lot of duplicate code here, but i am too lazy to refactor it ...
    for col in column_units:
        twins_count = {}
        for k in col:
            v = values[k]
            if len(v) == 2:
                if twins_count.get(v) is None:
                    twins_count[v] = 1
                else:
                    twins_count[v] += 1

        for v, count in twins_count.items():
            if count == 2:
                for k in col:
                    if values[k] == v:
                        continue
                    for i in v:
                        values[k] = values[k].replace(i, '')

    # the method for diagonal is same too
    for diagonal in diagonal_units:
        twins_count = {}
        for k in diagonal:
            v = values[k]
            if len(v) == 2:
                if twins_count.get(v) is None:
                    twins_count[v] = 1
                else:
                    twins_count[v] += 1

        for v, count in twins_count.items():
            if count == 2:
                for k in col:
                    if values[k] == v:
                        continue
                    for i in v:
                        values[k] = values[k].replace(i, '')

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    res = {}
    for i, item in enumerate(grid):
        r = i // 9
        c = i % 9

        if item == '.':
            item = "123456789"
        res[rows[r]+cols[c]] = item

    return res


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for k in solved_values:
        v = values[k]
        for peer in peers[k]:
            values[peer] = values[peer].replace(v, '')

        # eliminate in diagonal
        for diagonal in diagonal_units:
            for d in diagonal:
                if k == d:
                    continue
                values[peer] = values[peer].replace(v, '')

    return values


def only_choice(values):
    # find out unsolved_values
    unsolved_values = [box for box in values.keys() if len(values[box]) != 1]
    for k in unsolved_values:
        v = values[k]

        # find out whether this box in on diagonal
        is_diag = is_diagonal(k)

        # for each digit in this unsolved box
        for digit in v:
            # use the condition `row[0][0] == k[0]`, find out the row which k belongs
            # for every p in this row, if digit in values[p], put this digit in list l
            # this can find out whether this digit is the only choice for its row
            l = [digit for row in row_units if row[0][0] == k[0] for p in row if digit in values[p]]
            if len(l) == 1:
                values[k] = digit
                break

            # same method for the column
            # this can find out whether this digit is the only choice for its column
            l = [digit for col in column_units if col[0][1] == k[1] for p in col if digit in values[p]]
            if len(l) == 1:
                values[k] = digit
                break

            # this can find out whether this digit is the only choice for its square
            l = [digit for square in square_units if k in square for p in square if digit in values[p]]
            if len(l) == 1:
                values[k] = digit
                break

            # this can find out whether this digit is the only choice for its diagonal
            if is_diag:
                l = [digit for diagonal in diagonal_units if k in diagonal for p in diagonal if digit in values[p]]
                if len(l) == 1:
                    values[k] = digit
                    break

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        # Your code here: Use the Only Choice Strategy

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
