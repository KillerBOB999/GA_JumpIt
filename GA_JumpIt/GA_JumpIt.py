#!/usr/bin/env python3

import sys
import random as rng
import copy

global DP_cost, DP_path, DP_min_cost
global GA_cost, GA_path, GA_min_cost, GA_minCostID 
global populationSize, population, fitness, mutationRate, generationCount

GA_cost = dict()
GA_path = []
population = [[]]
fitness = dict()
GA_min_cost = sys.maxsize
GA_minCostID = int()
generationCount = 1

def checkForDouble0s(selectedPopulation, chromosomeID, precedingGeneID):
    if selectedPopulation[chromosomeID][precedingGeneID] == 0 and selectedPopulation[chromosomeID][precedingGeneID + 1] == 0:
        return True
    else:
        return False

def initialize(numOfGenes):
    global GA_cost, GA_path, populationSize, population, fitness, mutationRate
    GA_cost = dict()
    GA_path = []
    populationSize = numOfGenes
    population = [[]]
    fitness = dict()
    mutationRate = 0.25
    GA_min_cost = sys.maxsize
    GA_minCostID = int()
    generationCount = 1

    for i in range(0, populationSize):
        population.append([])
        for ii in range(0, numOfGenes):
            if ii == 0 or ii == numOfGenes - 1:
                population[i].append(1)
            else:
                population[i].append(rng.randint(0, 1))
            if ii > 0:
                if checkForDouble0s(population, i, ii - 1):
                    population[i][ii] = 1
    population.pop()
    return

def mutate(newPopulation, chromosomeID):
    for i in range(1, len(newPopulation[chromosomeID]) - 1):
        if rng.random() >= mutationRate:
            if newPopulation[chromosomeID][i] == 0:
                newPopulation[chromosomeID][i] = 1
            else:
                newPopulation[chromosomeID][i] = 0
                if checkForDouble0s(newPopulation, chromosomeID, i - 1) or checkForDouble0s(newPopulation, chromosomeID, i):
                    newPopulation[chromosomeID][i] = 1
    return

def cross(newPopulation, parent1ChromosomeID, parent2ChromosomeID, targetChromosomeID):
    if newPopulation[0] == []:
        newPopulation.pop()
    newPopulation[targetChromosomeID] = population[parent1ChromosomeID]
    selectedCrossPoint = rng.randint(1, len(population[parent1ChromosomeID]) - 2)
    for i in range(selectedCrossPoint, len(population[parent2ChromosomeID])):
        newPopulation[targetChromosomeID][i] = copy.deepcopy(population[parent2ChromosomeID][i])
        if checkForDouble0s(newPopulation, targetChromosomeID, i-1):
            newPopulation[targetChromosomeID][i] = 1
    if rng.random() <= mutationRate:
        mutate(newPopulation, targetChromosomeID)
    return

def calcFitness(chromosomeID):
    fitness.update({chromosomeID : 1.0 / GA_cost[chromosomeID]})
    return

def calcCost(chromosomeID, board):
    GA_cost.update({chromosomeID : 0})
    for geneID in range(0, len(population[chromosomeID])):
        if population[chromosomeID][geneID] == 1:
            if chromosomeID not in GA_cost:
                GA_cost.update({chromosomeID : board[geneID]})
            else:
                GA_cost[chromosomeID] += board[geneID]
    return

def populate():
    global populationSize, generationCount, GA_minCostID, population, fitness
    generationCount += 1
    leastFitID = (0, 0)
    for chromosomeID in GA_cost:
        if GA_cost[chromosomeID] > leastFitID[1]:
            leastFitID = (chromosomeID, GA_cost[chromosomeID])
    parents = []
    chanceOfMating = dict()
    totalFitness = 0
    for fitnessContribution in fitness:
        totalFitness += fitness[fitnessContribution]
    first = True
    for index in fitness:
        if first:
            chanceOfMating.update({index : (0, fitness[index] / totalFitness)})
            first = False
        else:
            chanceOfMating.update({index : (chanceOfMating[index - 1][1], (fitness[index] / totalFitness) + chanceOfMating[index - 1][1])})
    while len(parents) != 2:
        rand = rng.random()
        for key in chanceOfMating:
            if rand >= chanceOfMating[key][0] and rand <= chanceOfMating[key][1]:
                parents.append(key)
                if len(parents) == 2:
                    cross(population, parents[0], parents[1], leastFitID[0])
    return

def GA_JumpIt(board):
    initialize(len(board))
    global GA_min_cost, DP_min_cost, GA_cost, GA_minCostID, generationCount
    GA_min_cost = sys.maxsize
    forceDo = True
    while (forceDo or GA_min_cost > DP_min_cost):# and generationCount < 2000:
        if forceDo != True:
                populate()
        for chromosomeID in range(0, len(population)):
            calcCost(chromosomeID, board)
            calcFitness(chromosomeID)
            if GA_cost[chromosomeID] < GA_min_cost:
                GA_min_cost = GA_cost[chromosomeID]
                GA_minCostID = chromosomeID
        forceDo = False
    return GA_cost[GA_minCostID]

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

def fileHandler(fileName):
    global DP_cost, GA_cost, DP_path, GA_path, DP_min_cost, GA_min_cost, population, generationCount
    numCorrect = 0
    total = 0
    file = open(fileName, "r")
    for line in file:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        DP_cost = [0] * len(lyst)
        DP_path = DP_cost[:]
        DP_min_cost = DP_JumpIt(lyst)
        print()
        print("game board:", lyst)
        print("___________________________")
        print("DP Solution")
        print("Minimum Cost: ", DP_min_cost)
        displayPath(lyst, False)
        print("___________________________")
        generationCount = 1
        GA_JumpIt(lyst)
        if DP_min_cost == GA_min_cost:
            numCorrect += 1
        total += 1
        for i in range(0, len(population[GA_minCostID])):
            if population[GA_minCostID][i] == 1:
                GA_path.append(i)
        GA_path.append(-1)
        print("GA Solution")
        print("Generations Iterated: ", generationCount)
        print("Minimum Cost (fitness): ", GA_min_cost)
        displayPath(lyst, True)
        print("___________________________")
    print()
    print("GA Overall Accuracy: ", (numCorrect / total) * 100, end = "%")
    print()
    return

def main():
    fileHandler("input1.txt")
    return

main()