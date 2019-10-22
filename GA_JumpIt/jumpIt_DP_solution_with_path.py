"""
Dynamic Programming solution to the jump-It problem
The solution finds the cheapest cost to play the game along with the path leading
to the cheapest cost
"""
global cost, path

cost = [] # global table to cache results - cost[i] stores minimum cost of playing the game starting at cell i
path = [] #global table to store path leading to cheapest cost
def jumpIt(board):
    #Bottom up dynamic programming implementation
    #board - list with cost associated with visiting each cell
    #return minimum total cost of playing game starting at cell 0
    
    n = len(board)
    cost[n - 1] = board[n - 1] #cost if starting at last cell
    path[n - 1] = -1 # special marker indicating end of path "destination/last cell reached"
    cost[n - 2] = board[n - 2] + board[n - 1] #cost if starting at cell before last cell
    path[n -2] = n - 1 #from cell before last, move into last cell
    #now fill the rest of the table
    for i in range(n-3, -1, -1):
        #cost[i] = board[i] + min(cost[i+1], cost[i+2])
        if cost[i +  1] < cost[i + 2]: # case it is cheaper to move to adjacent cell
            cost[i] = board[i] +  cost[i + 1]
            path[i] = i + 1 #so from cell i, one moves to adjacent cell
        else: 
            cost[i] = board[i] + cost[i + 2]
            path[i] = i + 2 #so from cell i, one jumps over cell
    return cost[0]

def displayPath(board):
    #Display path leading to cheapest cost - method displays indices of cells visited
    #path - global list where path[i] indicates the cell to move to from cell i
    cell = 0 # start path at cell 0
    print("path showing indices of visited cells:", end = " ")
    print(0, end ="")
    path_contents = "0" # cost of starting/1st cell is 0; used for easier tracing
    while path[cell] != -1: # -1 indicates that destination/last cell has been reached
        print(" ->", path[cell], end = "")
        cell = path[cell]
        path_contents += " -> " + str(board[cell])
    print()
    print("path showing contents of visited cells:", path_contents)

    
def main():
    f = open("input1.txt", "r") #input.txt
    global cost, path
    for line in f:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        cost = [0] * len(lyst) #create the cache table
        path = cost[:] # create a table for path that is identical to path
        min_cost = jumpIt(lyst)
        print("game board:", lyst)
        print("cost: ", min_cost)
        displayPath(lyst)
        print("___________________________")

if __name__ == "__main__":
    main()
