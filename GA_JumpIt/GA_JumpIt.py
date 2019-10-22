#!/usr/bin/env python3

import random as rng

global cost, path, populationSize, population, fitness, crossOverRate, mutationRate, numberOfGenerations

cost = []
path = []
populationSize = 20
population = [[]]
fitness = []
crossOverRate = 0.85
mutationRate = 0.15
numberOfGenerations = 0

def checkForDouble0s(chromosomeID, precedingGeneID):
    if population[chromosomeID][precedingGeneID] == 0 and population[chromosomeID][precedingGeneID + 1] == 0:
        return True
    else:
        return False

def initialize(numOfGenes):
    global cost, path, populationSize, population, fitness, crossOverRate, mutationRate, numberOfGenerations
    cost = []
    path = []
    populationSize = 1
    population = [[]]
    fitness = []
    crossOverRate = 0.85
    mutationRate = 0.15
    numberOfGenerations = 0

    for i in range(0, populationSize):
        for ii in range(0, numOfGenes):
            population[i].append(rng.randint(0, 1))
            if ii > 0:
                if checkForDouble0s(i, ii - 1):
                    population[i][ii] = 1
    return

def mutate(chromosomeID):
    selectedGeneID = rng.nextint(0, len(population[chromosomeID]))
    if population[chromosomeID][selectedGeneID] == 0:
        population[chromosomeID][selectedGeneID] = 1
    else:
        population[chromosomeID][selectedGeneID] = 0
        if selectedGeneID > 0 and checkForDouble0s(chromosomeID, selectedGeneID - 1):
            population[chromosomeID][selectedGeneID] = 1
    return

def cross(parent1ChromosomeID, parent2ChromosomeID):
    temp = []
    selectedCrossPoint = rng.nextint(0, len(population[parent1ChromosomeID]))
    for i in range(0, selectedCrossPoint):
        temp[i] = population[parent1ChromosomeID][i]
        population[parent1ChromosomeID][i] = population[parent2ChromosomeID][i]
    for i in range(0, selectdeCrossPoint):
        population[parent2ChromosomeID][i] = temp[i]
    return

def calcFitness(chromosomeID):
    fitness[chromosomeID] = 1.0 / cost[chromosomeID]
    return

def calcCost(chromosomeID, board):
    cost.append(int())
    for geneID in range(0, len(population[chromosomeID])):
        if population[chromosomeID][geneID] == 1:
            cost[chromosomeID] += board[geneID]
    return

def GA_JumpIt(board):
    initialize(len(board))
    for chromosomeID in range(0, len(population)):
        calcCost(chromosomeID, board)
        calcFitness(chromosomeID)
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

def fileHandler(fileName):
    global cost, path, numberOfGenerations
    file = open(fileName, "r")
    for line in file:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        path = [0] * len(lyst)
        min_cost = GA_JumpIt(lyst)
        print("Generations Required: ", numberOfGenerations)
        print("game board:", lyst)
        print("cost: ", min_cost)
        displayPath(lyst)
        print("___________________________")
    return

def main():
    fileHandler("input1.txt")
    return

main()