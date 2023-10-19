from pickle import GLOBAL
from Queue import Queue

Puzzle_size = 8
Mat_size = 3 #Matrix Size
number_of_nodes = 0

#Definitions for the Puzzle class
class Puzzle(object):
    def __init__(temp, initial_state=None):
            temp.initial_state = initial_state
            temp.explored = []
            temp.path=[]
#getting the initial state
    def get_initial_state(temp):
            return temp.initial_state
#printing the initial state
    def print_initial_state(temp):
            print_current_state(temp.initial_state)
#test if goal is achieved
    def test_goal(temp, node, move):
            temp.explored.append(node)
            temp.path.append(move)
            return node == temp.goal_state  
#get length of explored nodes          
    def get_explored_nodes_length(temp):
            return len(temp.explored)
#check if node is explored
    def is_node_explored(temp, node):
            return node in temp.explored
#getting the goal state
    def get_goal_state(temp,goal_state=None):
            temp.goal_state=goal
            return temp.goal_state 

            
#checking the misplaced tile heuristic 
def misplaced_tile(nodes, new_nodes):
    while not new_nodes.empty():
            node = new_nodes.get_first_element()
            nodes.insert_element(node[3], heuristic_misplaced_tiles(node[3]), node[2], heuristic_misplaced_tiles(node[3]) + node[2],node[4])
    print ("\n")
    
#manhattan distance heuristic
def manhattan_distance(nodes, new_nodes):
    while not new_nodes.empty():
            node = new_nodes.get_first_element()
            nodes.insert_element(node[3], heuristic_manhattan_distance(node[3]), node[2], heuristic_manhattan_distance(node[3]) + node[2],node[4])
    print ("\n")
    
#Calculating the heuristic of misplaced tiles 
def heuristic_misplaced_tiles(node):
    count = 0
    goal = Puzzle.get_goal_state()
    for i in range(Puzzle_size+1):
            if node[i] == 0:
                continue
            if goal[i] != node[i]:
                    count += 1
    return count

#Calculating the heuristic of manhattan distance 
def heuristic_manhattan_distance(node):
    count = 0
    goal = Puzzle.get_goal_state()
    for i in range(Puzzle_size+1):
            if i == 0:
                continue
            goal_index = goal.index(i)
            index = node.index(i)
            row_difference = abs((goal_index / Mat_size) - (index / Mat_size))
            column_difference = abs((goal_index % Mat_size) - (index % Mat_size))
            count += (row_difference + column_difference)
    return count

#Main search strategy
def main_strategy(Puzzle, heuristic_func):
    depth = 0
    nodes = Queue()
    nodes.insert_element(Puzzle.get_initial_state())
    while not nodes.empty():
            total_node = nodes.get_first_element()
            node = total_node[3]
            move = total_node[4]
            if (total_node[2] or total_node[1]):
                    print ("The Next Best Node to Expand is with g(n) = %d and h(n) = %d " % (total_node[2], total_node[1]),)
            print_current_state(node)
            if Puzzle.test_goal(node,move):
                    print ("We finally reached Goal State")
                    print("The Goal Path is \n")
                    for path in Puzzle.path:
                        print(path,end="->")
                    print ("\nTotal Number of Nodes Expanded are %d ." % Puzzle.get_explored_nodes_length())
                    print ("The Number of Unexpanded Nodes are %d."% nodes.get_len_elements())
                    print ("The Depth of the Goal Node is %d." % total_node[2])
                    return None
            print ("After expanding this node\n")
            print ("->\n")
            heuristic_func(nodes, node_expansion(total_node, Puzzle))
            depth += 1


#All the possible nodes are generated and added to priority queue if not explored
def node_expansion(node, Puzzle):
    expanded_nodes = Queue()
    node1 = empty_tile_u(node[3][:], Mat_size)
    node2 = empty_tile_d(node[3][:], Mat_size, Puzzle_size)
    node3 = empty_tile_l(node[3][:], Mat_size)
    node4 = empty_tile_r(node[3][:], Mat_size)
    if node1 and not Puzzle.is_node_explored(node1):
            expanded_nodes.insert_element(node1, 0, node[2] + 1, 0,'u')
    if node2 and not Puzzle.is_node_explored(node2):
            expanded_nodes.insert_element(node2, 0, node[2] + 1, 0,'d')
    if node3 and not Puzzle.is_node_explored(node3):
            expanded_nodes.insert_element(node3, 0, node[2] + 1, 0,'l')
    if node4 and not Puzzle.is_node_explored(node4):
            expanded_nodes.insert_element(node4, 0, node[2] + 1, 0,'r')
    global number_of_nodes
    number_of_nodes = number_of_nodes + len(expanded_nodes.elements)
    return expanded_nodes

    
#Print the current state in the Puzzle solving
def print_current_state(mat_input):
    print ("-" * 20)
    for index, value in enumerate(mat_input):
            if (index + 1) % Mat_size == 0:
                    print (value if value != 0 else "0", end="\n")
            else:
                    print (value if value != 0 else "0", " ", end=" ")
    print ("-" * 20)
            

#Move the blank tile upwards
def empty_tile_u(mat_input, MAT_SIZE):
    if mat_input.index(0) >= MAT_SIZE:
        index = mat_input.index(0)
        mat_input[index -  MAT_SIZE], mat_input[index] = mat_input[index], mat_input[index -  MAT_SIZE]
        return mat_input
    return None

#Move the blank tile downwards
def empty_tile_d(mat_input, MAT_SIZE, Puzzle_size):
    if mat_input.index(0) < Puzzle_size + 1 - MAT_SIZE:
        index = mat_input.index(0)
        mat_input[index + MAT_SIZE], mat_input[index] = mat_input[index], mat_input[index + MAT_SIZE]
        return mat_input
    return None

#Move the blank tile towards left
def empty_tile_l(mat_input, MAT_SIZE):
    if mat_input.index(0) % MAT_SIZE != 0:
            index = mat_input.index(0)
            mat_input[index - 1], mat_input[index] = mat_input[index], mat_input[index - 1]
            return mat_input
    return None

#Move the blank tile towards right
def empty_tile_r(mat_input, MAT_SIZE):
    if mat_input.index(0) % MAT_SIZE != MAT_SIZE - 1:
            index = mat_input.index(0)
            mat_input[index + 1], mat_input[index] = mat_input[index], mat_input[index + 1]
            return mat_input
    return None


#Logic where initial state and goal state are given and search strategy is defined for 8 Puzzle program
if __name__ == "__main__":
    
    print ("Enter Elements for Intial State")
    mat_input = list(map(int,input("\nEnter numbers for intial state : ").strip().split()))[:9]
    print ("Enter Goal State Elements ")
    print ("NOTE: Use \"0\" for blank.\n")
    goal = list(map(int,input("\nEnter numbers for goal state : ").strip().split()))[:9]
    Puzzle = Puzzle(mat_input)
    print ("Initial State",)
    Puzzle.print_initial_state()
    print ("Goal State",)
    print_current_state(Puzzle.get_goal_state())
    print ("\n")
    print ("Enter Algorithm:\n1. A* with the Misplaced Tile Heuristic.\n2. A* with the Manhattan Distance Heuristic.")
    enterchoice = int(input())
    t1 = 0
    if enterchoice == 1:
            main_strategy(Puzzle, misplaced_tile)
    elif enterchoice == 2:
            main_strategy(Puzzle, manhattan_distance)
    else:
            print ("Invalid choice.")
    print ("The algorithm has generated %d nodes in total including Goal State." % number_of_nodes)
    
