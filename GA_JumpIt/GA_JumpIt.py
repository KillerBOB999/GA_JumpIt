#!/usr/bin/env python3

# INFORMATION--------------------------------------------------------------------------
# DEVELOPER:        Anthony Harris
# SLATE:            Anthony999
# DATE:             30 October 2019
# PURPOSE:          Use the concept of Genetic Algorithms to compute the optimal path
#                   in a game of JumpIt.
#--------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# IMPORTS------------------------------------------------------------------------------
import sys
import random as rng
import copy
#--------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# GLOBALS------------------------------------------------------------------------------
rng.seed(999)           # Seed the random number generator to produce reliable results

GA_cost = dict()        # A dictionary to be defined as (chromosomeID, costOfChromome)
                        # key-value pairs

GA_path = []            # Represents the indices of the tiles occupied by the
                        # calculated solution output by the GA

population = [[]]       # A set of chromosomes, where each chromosome is defined as a
                        # set of genes, which are represented by a 0 or a 1, which
                        # represents the boolean decision to occupy or jump a tile
                        # in the game board (occupy = 1, jump = 0)
                        # EX: [c1=[1,0,1], c2=[1,1,1]]

populationSize = int()  # The desired size of the populations to be tested. Will be
                        # based upon the length of the JumpIt game board

mutationRate = float()  # The liklihood of a mutation occurring in the genome of an
                        # entity in the population

crossRate = float()     # The liklihood of 2 entities successfully crossing their
                        # genomes to create a new entity.

fitness = dict()        # A dictionary to be defined as (chromosomeID, fitnessScore)
                        # key-value pairs where the fitnessScore is defined by
                        # 1 / GA_cost[chromosomeID]

GA_min_cost = int()     # The minimum calculated cost determined by the GA

GA_minCostID = int()    # The chromosomeID of the chromosome associated with the
                        # minimum calculated cost

generationCount = int() # The number of iterations of the GA

changedIDs = []         # The list of IDs that have changed since last iteration
#--------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    checkForDouble0s
# Parameters:       chromosomeID(int)
#                       Use:    Used to grab the target chromosome from the population
#                               for manipulation
#                   precedingGeneID(int)
#                       Use:    Used to find the gene point of reference within the
#                               genome and for comparing the point of reference with
#                               the current gene to check for repeating 0s
# Returns:          True if there are repeating 0s, 
#                   False otherwise
# Description:      A helper function that checks for repeating 0s in a genome, given
#                   the chromosomeID and point of reference geneID
#--------------------------------------------------------------------------------------
def checkForDouble0s(chromosomeID, precedingGeneID):
    if population[chromosomeID][precedingGeneID] == 0 and population[chromosomeID][precedingGeneID + 1] == 0:
        return True
    else:
        return False

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    initialize
# Parameters:       numOfGenes(int)
#                       Use:    Represents the size of the game board, which is used
#                               as the number of genes in each chromosome for the
#                               current species
# Returns:          N/A
# Description:      The function that is called when starting a new game board. This
#                   function initializes the global variables for use during the
#                   GA, and created the initial population using random values of
#                   0 and 1 for all genes except for the first and last, which must be
#                   initialized to 1 for the JumpIt game logic to be upheld
#--------------------------------------------------------------------------------------
def initialize(numOfGenes):
    # Give access to global variables
    global GA_cost, GA_path, populationSize, population, fitness, mutationRate, crossRate

    # Initialize the global variables
    GA_cost = dict()                # See global declaration for description
    GA_path = []                    # See global declaration for description
    populationSize = 3 * numOfGenes # See global declaration for description
    population = [[]]               # See global declaration for description
    fitness = dict()                # See global declaration for description
    mutationRate = 0.01             # See global declaration for description
    crossRate = 0.85                # See global declaration for description
    GA_min_cost = sys.maxsize       # See global declaration for description
    GA_minCostID = int()            # See global declaration for description
    generationCount = 1             # See global declaration for description
    changedIDs = []                 # See global declaration for description

    # Itratively generate the population
    for i in range(0, populationSize):
        population.append([])       # Add an entity to the population
        # Iteratively generate the genes of the current entity
        for ii in range(0, numOfGenes):
            # Check for first and last gene
            if ii == 0 or ii == numOfGenes - 1:
                population[i].append(1)
            # Otherwise
            else:
                population[i].append(rng.randint(0, 1))
            # Ensure no repeating 0s
            if ii > 0:
                if checkForDouble0s(i, ii - 1):
                    population[i][ii] = 1
    population.pop()    # Removes unnecessary empty entity
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    mutate
# Parameters:       chromosomeID(int)
#                       Use:    Used to grab the target chromosome from the population
#                               for manipulation
# Returns:          N/A
# Description:      Used to simulate biological mutation in the biological reproductive
#                   cycle. Iterates through each of the genes in a selected chromosomal
#                   genome and attempts to mutate them
#--------------------------------------------------------------------------------------
def mutate(chromosomeID):
    # Give access to global variables
    global population, mutationRate

    # Iteratively step through the selected entity's genome and attempt to mutate the
    # genes therein, ignoring the first and last genes.
    for i in range(1, len(population[chromosomeID]) - 1):
        # If probability says to mutate, then attempt to mutate, otherwise do nothing
        if rng.random() <= mutationRate:
            if population[chromosomeID][i] == 0:
                population[chromosomeID][i] = 1
            else:
                population[chromosomeID][i] = 0
                # Check both the preceding and following genes to ensure no double 0s
                if checkForDouble0s(chromosomeID, i - 1) or checkForDouble0s(chromosomeID, i):
                    population[chromosomeID][i] = 1
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    testCanCross
# Parameters:       attemptedCrossPoint(int)
#                       Use:    Used as the locus of the genetic crossover event
#                   parent1ChromosomeID(int)
#                       Use:    Used to grab the target chromosome of the first parent
#                               from the population for manipulation
#                   parent2ChromosomeID(int)
#                       Use:    Used to grab the target chromosome of the second parent
#                               from the population for manipulation
#                   targetChromosomeIDs((int, int))
#                       Use:    The tuples of chromosomalIDs used to grab the target
#                               chromosomes of the 2 entities targeted for replacement
#                               from amongst the population
#
# Returns:          True if successfully crossed the genomes of the parents, 
#                   False otherwise
# Description:      Serves as the biological cross-over equivalent. Returns boolean
#                   representations of the results to ensure that it can be used in a
#                   loop until a successful child is created.
#--------------------------------------------------------------------------------------
def testCanCross(attemptedCrossPoint, parent1ChromosomeID, parent2ChromosomeID, targetChromosomeIDs):
    # Give access to global variables
    global population

    # Initialize local children variables used to test the success of the crossover
    # without losing the valid data in the existing population.
    child1 = []
    child2 = []

    # Iteratively create the children based upon the parents genomes and the selected
    # crossover point
    for i in  range(0, len(population[parent1ChromosomeID])):
        if i < attemptedCrossPoint:
            child1.append(population[parent1ChromosomeID][i])
            child2.append(population[parent2ChromosomeID][i])
        else:
            child1.append(population[parent2ChromosomeID][i])
            child2.append(population[parent1ChromosomeID][i])

    # Check the genomes of the children for double 0s
    for i in range(0, len(child1) - 1):
        # If a double 0 sequence is found, the crossover failed, so return False
        if (child1[i] == 0 and child1[i+1] == 0) or (child2[i] == 0 and child2[i+1] == 0):
            return False
    # If no double 0 sequence was found, the cross succeeded, so change the genomes of
    # the targeted chromosomes to represent the cross and return True
    population[targetChromosomeIDs[0]] = child1
    population[targetChromosomeIDs[1]] = child2
    return True

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    mate
# Parameters:       parent1ChromosomeID(int)
#                       Use:    Used to grab the target chromosome of the first parent
#                               from the population for manipulation
#                   parent2ChromosomeID(int)
#                       Use:    Used to grab the target chromosome of the second parent
#                               from the population for manipulation
#                   targetChromosomeIDs((int, int))
#                       Use:    The tuples of chromosomalIDs used to grab the target
#                               chromosomes of the 2 entities targeted for replacement
#                               from amongst the population 
# Returns:          N/A
# Description:      Mates the 2 parent chromosomes and replaces the chromosomes of the
#                   selected less-fit entites with the result of the mating process
#--------------------------------------------------------------------------------------
def mate(parent1ChromosomeID, parent2ChromosomeID, targetChromosomeIDs):
    # Give access to global variables
    global crossRate, population, populationSize

    # Reassign the values of the targeted, less-fit genomes to the values of the 
    # more-fit parents. These values will be used if probability decides not to cross
    # the genomes of the parents
    population[targetChromosomeIDs[0]] = copy.deepcopy(population[parent1ChromosomeID])
    population[targetChromosomeIDs[1]] = copy.deepcopy(population[parent2ChromosomeID])

    # Generate a random float value between 0 and 1 and use it to decide whether or not
    # to cross the genomes of the parents
    rand = rng.random()
    if rand <= crossRate:
        canCross = False    # Assume you cannot cross the genomes until proven otherwise
        crossAttempts = 0   # Attempts to cross
        # Until the genomes are successfully crossed or the maximum number of attempts
        # have been made, try to cross them
        while not canCross and crossAttempts < populationSize:
            # Randomly select a locus for the crossover point
            selectedCrossPoint = rng.randint(1, len(population[parent1ChromosomeID]) - 2)
            # Attempt the crossover
            canCross = testCanCross(selectedCrossPoint, parent1ChromosomeID, parent2ChromosomeID, targetChromosomeIDs)
    
    # Attempt to mutate the new entities
    mutate(targetChromosomeIDs[0])
    mutate(targetChromosomeIDs[1])
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    calcFitness
# Parameters:       chromosomeID(int)
#                       Use:    Used to grab the target chromosome from the population
#                               for manipulation    
# Returns:          N/A
# Description:      A helper function that simply calculates the fitness of each
#                   entity in the population and stores it in the global fitness
#                   dictionary using the chromosomeID as the key and the calculated
#                   fitness as the value
#--------------------------------------------------------------------------------------
def calcFitness(chromosomeID):
    # Give access to global variables
    global fitness, GA_cost

    # Calculate and store the fitness
    fitness.update({chromosomeID : 1.0 / GA_cost[chromosomeID]})
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    calcCost
# Parameters:       chromosomeID(int)
#                       Use:    Used to grab the target chromosome from the population
#                               for manipulation 
#                   board(list(map(int, string.split())))
#                       Use:    Represents the game board where each entry is a tile
#                               with a cost represented by the value of the entry
# Returns:          N/A
# Description:      A helper funtion that Determines the cost associated with the 
#                   genome of the entity identified in the population by the 
#                   chromosomeID and stores it in the global GA_cost dictionary with
#                   the key being the chromosomeID and the value being the cost
#--------------------------------------------------------------------------------------
def calcCost(chromosomeID, board):
    # Give access to global variables
    global population, GA_cost

    # Initialize the associated cost of the chromosome in the dictionary to 0
    GA_cost.update({chromosomeID : 0})

    # Iterate through the genes of the selected entity and calculate the cost based
    # upon the cost of each visited tile
    for geneID in range(0, len(population[chromosomeID])):
        # If the tile is to be visited, add the cost of the tile to the genome cost
        if population[chromosomeID][geneID] == 1:
            GA_cost[chromosomeID] += board[geneID]
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    findLeastFit
# Parameters:       N/A 
# Returns:          leastFitIDs where leastFitIDs is defined as a list of 
#                   chromosomalIDs representing the least fit entities of the current 
#                   population in consideration
# Description:      This function determines the chromosomalIDs of the least fit
#                   entities of the population and returns it for use elsewhere
#--------------------------------------------------------------------------------------
def findLeastFit():
    # Give access to global variables
    global GA_cost, changedIDs

    # Initialize local variables
    leastFitIDs = []                            # List to be returned
    orderedCost = [GA_cost[k] for k in GA_cost] # Copy of the values of the cost dict
    orderedCost.sort()                          # Now sorted
    numOfLosers = int(len(orderedCost) / 2)     # How many entities to replace

    # Make sure the number of entities to be replaced is even for easier logic
    if numOfLosers % 2 != 0:
        numOfLosers += 1

    # Iterate through the orderedCost list and find the corresponding chromosomalIDs
    # by comparing the costs to the costs found in the global GA_cost dictionary
    for orderedCostIndex in range(numOfLosers, len(orderedCost)):
        for unorderedCostIndex in GA_cost:
            # If the costs match up
            if GA_cost[unorderedCostIndex] == orderedCost[orderedCostIndex]:
                # Add the chromosomalID to the list of leastFitIDs
                leastFitIDs.append(unorderedCostIndex)
    # Sort the determined list for easier logic and return the newly sorted list
    leastFitIDs.sort()
    changedIDs = leastFitIDs
    return leastFitIDs

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    findChanceOfMating
# Parameters:       N/A
# Returns:          chanceOfMating where chanceOfMating is a dictionary that is
#                   defined by (chromosomeID, calculatedLiklihoodOfMating) key-value
#                   pairs and represents the roulette wheel approach to reproduction
# Description:      Calculates the liklihood of reproduction for each entity in the
#                   population and returns this to be used elsewhere
#--------------------------------------------------------------------------------------
def findChanceOfMating():
    # Give access to global variables
    global fitness

    # Initialize local variables
    chanceOfMating = dict() # To be returned
    totalFitness = 0        # Sum of the fitnesses of all entities in the population

    # Iteratively calculate the totalFitness
    for fitnessContribution in fitness:
        totalFitness += fitness[fitnessContribution]

    # Iteratively calculate the relative liklihood of each entity to reproduce, given
    # the ratio of their fitness to the totalFitness and store this value in a
    # number line between 0 and 1 based upon their ordering in the population
    first = True    # Signifies the first iteration
    for index in fitness:
        # If on the first iteration, start the corresponding number line at 0
        if first:
            chanceOfMating.update({index : (0, fitness[index] / totalFitness)})
            first = False
        # Otherwise, start the corresponding number line at the end point of the
        # previous entry
        else:
            chanceOfMating.update({index : (chanceOfMating[index - 1][1], (fitness[index] / totalFitness) + chanceOfMating[index - 1][1])})
    return chanceOfMating

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    populate
# Parameters:       N/A
# Returns:          N/A
# Description:      Generates the next population of entities                   
#--------------------------------------------------------------------------------------
def populate():
    # Give access to global variables
    global populationSize, generationCount, GA_minCostID, population, fitness, GA_cost

    # If you need to create a new population, then you need to increment the generation
    generationCount += 1

    # Initialize local variables
    leastFitIDs = findLeastFit()            # The list of IDs of the least fit half of 
                                            # the entities in the population

    parents = []                            # The list of parents whose genomes will
                                            # be passed on to the new entities

    chanceOfMating = findChanceOfMating()   # The likilhood of each entity in the
                                            # population to reproduce, placed on a
                                            # number line based upon the ordering of
                                            # the entities in the population

    # Iteratively create the new population by modifying the least fit entities of the
    # existing population to match the newly generated genomes. Use a step size of 2
    # to replace 2 entities per iteration
    for i in range(0, len(leastFitIDs), 2):
        # While you don't have a full set of parents
        while len(parents) != 2:
            # Generate a random float between 0 and 1 to use as the random point on
            # the number line
            rand = rng.random()
            # Iteratively check to see where the randomly generated float falls on the
            # number line of liklihoods of mating found in the chanceOfMating dict
            for key in chanceOfMating:
                # If the randomly generated number falls in the current range
                if rand >= chanceOfMating[key][0] and rand <= chanceOfMating[key][1]:
                    # Add the current entity to the list of parents
                    parents.append(key)
                    # If both parents have been found
                    if len(parents) == 2:
                        # Mate them
                        mate(parents[0], parents[1], (leastFitIDs[i], leastFitIDs[i+1]))
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    GA_JumpIt
# Parameters:       board(list(map(int, string.split())))
#                       Use:    Represents the game board where each entry is a tile
#                               with a cost represented by the value of the entry
# Returns:          N/A
# Description:      Performs the GA to determine the most optimal solution to the
#                   JumpIt game, given a game board
#--------------------------------------------------------------------------------------
def GA_JumpIt(board):
    # Give access to global variables
    global GA_min_cost, DP_min_cost, GA_cost, GA_minCostID, generationCount, populationSize, changedIDs

    # Initialize global variables
    initialize(len(board))
    GA_min_cost = sys.maxsize   # Set initial minimum cost to the largest number
                                # allowed to ensure it is always greater than the
                                # calculated minimum upon completion of the first
                                # iteration of the algorithm

    previousMin = GA_min_cost
    numTimesSameMin = 0
    # Emulate a Do-While loop because python doesn't have one
    forceDo = True
    # Check for (forceDo||stagnant growth) && generationCount < maximumAllowedIterations
    while (forceDo or numTimesSameMin < 7.5 * populationSize) and generationCount < 15 * populationSize:
        # If not first iteration, evolve the population
        if forceDo != True:
                populate()
        # Calculate the cost and fitness of each chromosome in the population
        for chromosomeID in range(0, len(population)):
            if chromosomeID in changedIDs or forceDo:
                calcCost(chromosomeID, board)
                calcFitness(chromosomeID)
            # If the minimum fitness has improved, record it
            if GA_cost[chromosomeID] < GA_min_cost:
                GA_min_cost = GA_cost[chromosomeID]
                GA_minCostID = chromosomeID
                numTimesSameMin = 0
                previousMin = GA_min_cost
        # Check for stagnant growth
        if GA_min_cost == previousMin:
            numTimesSameMin += 1
                
        forceDo = False
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    DP_JumpIt
# Description:      Code provided by Dr. Jamil Saquer of Missouri State University
#                   to calculate the true optimal solution of the given game board
#                   for use as a reference in calculating the accuracy of the GA
#--------------------------------------------------------------------------------------
def DP_JumpIt(board):
    #Bottom up dynamic programming implementation
    #board - list with cost associated with visiting each cell
    #return minimum total cost of playing game starting at cell 0
    
    n = len(board)
    DP_cost[n - 1] = board[n - 1] #cost if starting at last cell
    DP_path[n - 1] = -1 # special marker indicating end of path "destination/last cell reached"
    DP_cost[n - 2] = board[n - 2] + board[n - 1] #cost if starting at cell before last cell
    DP_path[n -2] = n - 1 #from cell before last, move into last cell
    #now fill the rest of the table
    for i in range(n-3, -1, -1):
        #cost[i] = board[i] + min(cost[i+1], cost[i+2])
        if DP_cost[i +  1] < DP_cost[i + 2]: # case it is cheaper to move to adjacent cell
            DP_cost[i] = board[i] +  DP_cost[i + 1]
            DP_path[i] = i + 1 #so from cell i, one moves to adjacent cell
        else: 
            DP_cost[i] = board[i] + DP_cost[i + 2]
            DP_path[i] = i + 2 #so from cell i, one jumps over cell
    return DP_cost[0]

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    displayPath
# Description:      Code provided by Dr. Jamil Saquer of Missouri State University
#                   to display the information to the screen. Modified slightly by me
#                   to display the information of both the DP and GA solutions.
#--------------------------------------------------------------------------------------
def displayPath(board, isGA):
    #Display path leading to cheapest cost - method displays indices of cells visited
    #path - global list where path[i] indicates the cell to move to from cell i
    cell = 0 # start path at cell 0
    print("path showing indices of visited cells:", end = " ")
    print(0, end ="")
    path_contents = "0" # cost of starting/1st cell is 0; used for easier tracing
    if isGA:
        cell += 1
        while GA_path[cell] != -1:
            print(" ->", GA_path[cell], end = "")
            path_contents += " -> " + str(board[GA_path[cell]])
            cell += 1
    else:
        while DP_path[cell] != -1: # -1 indicates that destination/last cell has been reached
            print(" ->", DP_path[cell], end = "")
            cell = DP_path[cell]
            path_contents += " -> " + str(board[cell])
    print()
    print("path showing contents of visited cells:", path_contents)
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    driver
# Parameters:       filename(string)
#                       Use:    Specifies the file to be opened and interpreted as
#                               game boards for the JumpIt game
# Returns:          N/A
# Description:      Some code provided by Dr. Jamil Saquer of Missouri State University
#                   namely the code for file handling and performing actions per line
#                   in the file. Modified slightly by me to include GA code interaction
#                   and calculation/display of GA statistics
#--------------------------------------------------------------------------------------
def driver(fileName):
    # Give access to global variables
    global DP_cost, GA_cost, DP_path, GA_path, DP_min_cost, GA_min_cost, population, generationCount

    # Initialize local variables
    numCorrect = 0  # For use when calculating GA accuracy
    total = 0       # For use when calculating GA accuracy

    # File Handling
    file = open(fileName, "r")
    # For each game board in the file, do stuff
    for line in file:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        DP_cost = [0] * len(lyst)
        DP_path = DP_cost[:]
        DP_min_cost = DP_JumpIt(lyst)   # Calculate the minimum using the DP approach
        print()
        print("=====================================================================================")
        print("game board:", lyst)
        print("___________________________")
        print("DP Solution")
        print("Minimum Cost: ", DP_min_cost)
        displayPath(lyst, False)
        print("___________________________")

        # My implementation of this function starts largely from here
        generationCount = 1     # Reset generation counter
        GA_JumpIt(lyst)         # Perform the GA

        # Update the data for accuracy calculation
        if DP_min_cost == GA_min_cost:
            numCorrect += 1
        total += 1

        # Update the path taken by the GA, based upon the most fit chromosome
        for i in range(0, len(population[GA_minCostID])):
            if population[GA_minCostID][i] == 1:
                GA_path.append(i)
        # Add a value that signifies the end of the path
        GA_path.append(-1)

        # Display information
        print("GA Solution")
        print("Generations Iterated: ", generationCount)
        print("Minimum Cost (fitness): ", GA_min_cost)
        displayPath(lyst, True)
        print("___________________________")
    print()
    print("=====================================================================================")

    # Display overal accuracy of the GA
    print("GA Overall Accuracy: ", (numCorrect / total) * 100, end = "%")
    print()
    return

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    main
# Parameters:       N/A
# Returns:          N/A
# Description:      The main driver used to run the program
#--------------------------------------------------------------------------------------
def main():
    # The following string represents the fileName of a file that contains a string
    # representation of game boards for a JumpIt game. This is where you define the
    # file to be used.
    fileName = "input2.txt"
    driver(fileName)
    return

main()