import problem
from node import Node
from priority_queue import PriorityQueue
import time

class SearchTimeOutError(Exception):
    pass


def compute_g(algorithm, node, goal_state):
    """
    Evaluates the g() value.

    Parameters
    ==========
    algorithm: str
        The algorithm type based on which the g-value will be computed.
    node: Node
        The node whose g-value is to be computed.
    goal_state: State
        The goal state for the problem.

    Returns
    =======
    int
        The g-value for the node.
    """

    if algorithm == "bfs":
        return node.get_depth()

    if algorithm == "astar":
        return node.get_total_action_cost()

    elif algorithm == "gbfs":
        return 0

    elif algorithm == "ucs":
        return node.get_total_action_cost()

    elif algorithm == "custom-astar":
        return node.get_total_action_cost()

    # Should never reach here.
    assert False
    return float("inf")


def compute_h(algorithm, node, goal_state):
    """
    Evaluates the h() value.

    Parameters
    ==========
    algorithm: str
        The algorithm type based on which the h-value will be computed.
    node: Node
        The node whose h-value is to be computed.
    goal_state: State
        The goal state for the problem.

    Returns
    =======
    int
        The h-value for the node.
    """

    if algorithm == "bfs":
        return 0

    if algorithm == "astar":
        return get_manhattan_distance(node.get_state(), goal_state)

    elif algorithm == "gbfs":
        return get_manhattan_distance(node.get_state(), goal_state)

    elif algorithm == "ucs":
        return 0

    elif algorithm == "custom-astar":
        return get_custom_heuristic(node.get_state(),goal_state)

    # Should never reach here.
    assert False
    return float("inf")


def get_manhattan_distance(from_state, to_state):
    return abs(from_state.x - to_state.x) + abs(from_state.y - to_state.y)


def turnning(a,b):
    z = abs(a -b)
    final = min(z, 4-z)
    return final

def get_custom_heuristic(from_state, to_state):
    x = from_state.get_x() - to_state.get_x()
    y = from_state.get_y() - to_state.get_y()
    absx = abs(x)
    absy = abs(y)
    manhattan = absx + absy


    if manhattan == 0:
        return 0
    
    direction_index = {"NORTH": 0, "EAST": 1, "SOUTH": 2, "WEST": 3}
    direction = from_state.get_orientation()
    index = direction_index.get(direction,0)
    
    if x == 0:
        turn_northsouth = min(turnning(index, direction_index["NORTH"]),
                    turnning(index, direction_index["SOUTH"]))
        turnning_cost = turn_northsouth * 2 
        return manhattan + turnning_cost

    if y == 0:
        turn_eastwest = min(turnning(index, direction_index["EAST"]),
                    turnning(index, direction_index["WEST"]))
        turnning_cost = turn_eastwest * 2
        return manhattan + turnning_cost

    turn_eastwest = min(turnning(index, direction_index["EAST"]), turnning(index, direction_index["WEST"]))
    turn_northsouth = min(turnning(index, direction_index["NORTH"]),
                turnning(index, direction_index["SOUTH"]))
    final_cost = min(turn_eastwest, turn_northsouth) * 2

    return manhattan + final_cost + 2






def graph_search(algorithm, time_limit):
    """
    Performs a search using the specified algorithm.

    Parameters
    ==========
    algorithm: str
        The algorithm to be used for searching.
    time_limit: int
        The time limit in seconds to run this method for.

    Returns
    =======
    tuple(list, int)
        A tuple of the action_list and the total number of nodes expanded.
    """

    # The helper allows us to access the problem functions.
    helper = problem.Helper()

    # Get the initial and the goal states.
    init_state = helper.get_initial_state()
    goal_state = helper.get_goal_state()[0]

    # Initialize the init node of the search tree and compute its f_score
    init_node = Node(init_state, None, 0, None, 0)
    f_score = compute_g(algorithm, init_node, goal_state) \
              + compute_h(algorithm, init_node, goal_state)

    # Initialize the fringe as a priority queue.
    priority_queue = PriorityQueue()
    priority_queue.push(f_score, init_node)

    # action_list should contain the sequence of actions to execute 
    # to reach from init_state to goal_state
    action_list = []

    # total_nodes_expanded maintains the total number of nodes expanded during the search
    total_nodes_expanded = 0

    time_limit = time.time() + time_limit

    # ========================
    # YOUR CODE HERE

    def priority(algorithm, gn, hn):
        if algorithm == "bfs":
            return gn
        if algorithm == "ucs":
            return gn
        if algorithm == "gbfs":
            return hn
        if algorithm == "astar":
            return gn + hn
        if algorithm == "custom-astar":
            return gn + hn
        

    def reconstruct(goal):
        plan = []
        current_node  = goal
        while current_node is not None and current_node.get_action():
            plan.append(current_node.get_action())
            current_node =current_node.get_parent()
        plan.reverse()
        return plan
    
    final_g = {}
    final_g[init_state] = compute_g(algorithm, init_node, goal_state)

    while not priority_queue.is_empty():
        if time.time() >= time_limit:
            raise SearchTimeOutError("Search timed out after %u secs." % (time_limit))
        try:
            current_node = priority_queue.pop()
        except IndexError:
            break
    

        current_state = current_node.get_state()

        if current_state.get_x() == -1 or current_state.get_y() == -1:
            continue

        current_g = compute_g(algorithm, current_node, goal_state)
        if current_state in final_g and current_g > final_g[current_state]:
            continue
        if helper.is_goal_state(current_state):
            action_list = reconstruct(current_node)
            return action_list, total_nodes_expanded
        
        total_nodes_expanded += 1
        successor = helper.get_successor(current_state)

    
    
        for action, (next_state, step_cost) in successor.items():
            if next_state.get_x() == -1 or next_state.get_y() == -1:
                continue

            parent_cost = current_node.get_total_action_cost()
            child = Node(
                next_state,
                current_node,
                current_node.get_depth() + 1,
                action,
                step_cost 
            )

            g_child = compute_g(algorithm, child, goal_state)
            h_child = compute_h(algorithm, child, goal_state)

            if (next_state not in final_g) or (g_child < final_g[next_state]):
                final_g[next_state] = g_child
                priority_queue.push(priority(algorithm, g_child, h_child), child)

    # ========================
    # Remove "raise NotImplementedError()" and add your code.
    # Your code for graph search should populate action_list and 
    # set total_nodes_expanded.
    # The automated script will verify their values.

    if time.time() >= time_limit:
        raise SearchTimeOutError("Search timed out after %u secs." % (time_limit))

    return action_list, total_nodes_expanded
