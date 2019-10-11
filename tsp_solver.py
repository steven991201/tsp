import random
import math
import csv
import argparse


parser = argparse.ArgumentParser(description='typing p, f')
parser.add_argument('name', help = "filename")
parser.add_argument('-p', required=False, default="100", help = "population")
parser.add_argument('-f', required=False, default="1000", help = "max Fitness evaluations")

args = parser.parse_args()
name = args.name
f = open(name, "r")



DataList = []
DistanceList = []
Population = int(args.p)
PopulationList = []
OrderList = []
OptimalGene = 0
mutationlate = 0.05
maxrepeat = int(args.f)

def data_setting():
    a = f.readline()
    while not("DIMENSION" in a.split(" ")[0]):
        a = f.readline()
    dimension = int(a[:-1].split(" ")[-1])
    while not("1" in a.split(' ')):
        a = f.readline()
    b = a[:-1].split(" ")
    while('' in b):
        b.remove('')
    DataList.append([float(b[1]), float(b[2])])
    for i in range(dimension-1):
        b  = f.readline()[:-1].split(" ")
        while ('' in b):
            b.remove('')
        DataList.append([float(b[1]), float(b[2])])
    f.close()

    for i in range(dimension):
        OrderList.append(i)
    return dimension


dimension = data_setting()

def evaluate_distance(a, b):
    return math.sqrt(abs(DataList[a][0] - DataList[b][0]) ** 2 + abs(DataList[a][1] - DataList[b][1]) ** 2)


def distance_setting():
    for i in range(dimension):
        DistanceList.append([])
        for j in range(dimension):
            DistanceList[i].append(None)



def initial_gene(population):
    for i in range(population):
        random.shuffle(OrderList)
        PopulationList.append(OrderList + [])


def calculate_dist(gene):
    sum = 0
    for i in range(len(gene) - 1):
        if(DistanceList[gene[i]][gene[i+1]] != None) :
            sum += DistanceList[gene[i]][gene[i+1]]
        else :
            DistanceList[gene[i]][gene[i+1]] = evaluate_distance(gene[i], gene[i+1])
            sum += DistanceList[gene[i]][gene[i + 1]]
    if(DistanceList[gene[0]][gene[len(gene) - 1]] != None):
        sum += DistanceList[gene[0]][gene[len(gene) - 1]]
    else:
        DistanceList[gene[0]][gene[len(gene) - 1]] = evaluate_distance(gene[i], gene[i+1])
        sum += DistanceList[gene[0]][gene[len(gene) - 1]]
    return sum


def calculate_optimal(problist,total):
    Optimal = 1 / (max(problist) * total)
    return Optimal


def calculate_index(population, populationlist):
    total = 0
    for i in range(population):
        total += 1 / calculate_dist(populationlist[i])
    problist = []
    for i in range(population):
        problist.append((1 / calculate_dist(populationlist[i])) / total)
    index = problist.index(max(problist))
    return index


def calculate_all(population, populationlist):
    a = []
    for i in range(population):
        a.append(calculate_dist(populationlist[i]))
    return a


def calculate_wheel(population, populationlist, problist):
    pick = random.uniform(0, 1)
    sum1 = 0
    for i in range(population):
        sum1 += problist[i]
        if pick <= sum1:
            return populationlist[i]


def crossover(parent1, parent2):
    ##division1 = random.randint(0, dimension//3)
    ##division2 = random.randint(dimension*2//3,dimension)
    division = random.randint(0, dimension)
    part1 = parent1[:division] + []
    ##part1 = parent1[dimension//3:dimension*2//3]+[]
    part2 = parent2 + []
    for i in part1:
        part2.remove(i)
    offspring = part1 + part2
    return offspring


def mutation(offspring):
    if random.uniform(0,1) < mutationlate:
        a = random.randint(0, dimension - 1)
        b = random.randint(0, dimension - 1)
        while a == b:
            b = random.randint(0, dimension-1)
        newvalue = offspring[a]
        offspring[a] = offspring[b]
        offspring[b] = newvalue
    return offspring


def make_offspring(populationlist, problist):
    currentlist = []
    for i in range(Population):
        a = calculate_wheel(Population, populationlist, problist)
        b = calculate_wheel(Population, populationlist, problist)
        currentlist.append(mutation(crossover(a, b)))
    return currentlist


def big_cycle(populationlist):
    total = 0
    for i in range(Population):
        total += 1 / calculate_dist(populationlist[i])
    problist1 = []
    for i in range(Population):
        problist1.append((1 / calculate_dist(populationlist[i])) / total)
    mindist = calculate_optimal(problist1, total)
    optimapopulation = populationlist
    for i in range(maxrepeat):
        total = 0
        for j in range(Population):
            total += 1 / calculate_dist(populationlist[j])
        problist2 = []
        for j in range(Population):
            problist2.append((1 / calculate_dist(populationlist[j])) / total)
        currentlist = make_offspring(populationlist, problist2)
        populationlist = currentlist
        localmin = calculate_optimal(problist2, total)
        if mindist > localmin:
            mindist = localmin
            optimapopulation = populationlist
        ##print(i)
    return mindist, optimapopulation


def main():
    distance_setting()
    initial_gene(Population)
    (mindist, optimalpopulation) = big_cycle(PopulationList)
    index = calculate_index(Population, optimalpopulation)
    print(mindist)
    result = [x+1 for x in optimalpopulation[index]]
    csvfile = open("TSP.csv", "w")
    csvwriter = csv.writer(csvfile)
    for row in result:
        csvwriter.writerow([row])
    csvfile.close()


main()