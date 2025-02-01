import heapq


def heuristic(state):
    cost = 0
    for stack in state:
        if len(stack) > 4 or (len(stack) > 0 and len(set(stack)) != 1):
            cost += len(stack)
    return cost


def is_goal_state(state):
    for stack in state:
        if len(stack) > 4 or (len(stack) > 0 and len(set(stack)) != 1):
            return False
    return True


def generate_next_states(state):
    next_states = []
    for from_col in range(len(state)):
        for to_col in range(len(state)):
            if from_col != to_col and state[from_col]:
                new_state = [stack[:] for stack in state]
                top_gear_color = new_state[from_col][-1]

                if not new_state[to_col] or new_state[to_col][-1] == top_gear_color:
                    gears_to_move = []
                    while new_state[from_col] and new_state[from_col][-1] == top_gear_color:
                        gears_to_move.append(new_state[from_col].pop())
                    
                    if len(new_state[to_col]) + len(gears_to_move) <= 4:
                        for gear in reversed(gears_to_move):
                            new_state[to_col].append(gear)
                        next_states.append((new_state, (from_col, to_col)))
    return next_states


def solve_game(start_position):
    priority_queue = [(heuristic(start_position), 0, [stack[:] for stack in start_position], [])]
    visited = set()
    visited.add(tuple(tuple(stack) for stack in start_position))

    while priority_queue:
        _, cost, current_state, moves = heapq.heappop(priority_queue)
        if is_goal_state(current_state):
            return moves
        for next_state, move in generate_next_states(current_state):
            state_tuple = tuple(tuple(stack) for stack in next_state)
            if state_tuple not in visited:
                visited.add(state_tuple)
                heapq.heappush(priority_queue, (cost + heuristic(next_state), cost + 1, next_state, moves + [move]))
    return None


if __name__ == "__main__":
    start_position = [
        ["4", "3", "2", "1"],
        ["3", "2", "6", "5"],
        ["4", "4", "7", "1"],
        ["9", "4", "2", "8"],
        ["12", "5", "11", "10"],
        ["8", "12", "3", "6"],
        ["2", "8", "10", "5"],
        ["9", "1", "7", "1"],
        ["9", "6", "3", "7"],
        ["5", "11", "9", "11"],
        ["8", "7", "10", "6"],
        ["10", "12", "12", "11"],
        [],
        [],
    ]

    solution = solve_game(start_position)
    if solution:
        print("  |  ".join([f"{move[0] + 1} » {move[1] + 1}" for move in solution]))
        print(f"\nШагов: {len(solution)}")
    else:
        print("\n\033[31mНет решений!\033[0m\n")

