#'''
import random, math

from deap import base, creator, tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("IndividualPoint", list, fitness=creator.FitnessMin)


def generatePoints(n):
    points = []
    for p in range(n):
        points.append((random.randint(-100, 100), random.randint(-100, 100)))
    return points

n = 100
points = generatePoints(n)

toolbox_q = base.Toolbox()
toolbox_q.register("permutation", random.sample, range(n), n)

toolbox_q.register("individual", tools.initIterate, creator.IndividualPoint, toolbox_q.permutation)
toolbox_q.register("population", tools.initRepeat, list, toolbox_q.individual)

def evalPoints(individual):
    dist = 0
    for i in range(len(individual)-1):
        point1 = points[individual[i]]
        point2 = points[individual[i+1]]
        dist += math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)
    return dist,

def cxPartiallyMatched(ind1, ind2):
    size = len(ind1)
    p1 = p2 = [0] * size

    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i

    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint1 < cxpoint2: cxpoint2 += 1
    else: cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    for i in range(cxpoint1, cxpoint2):
        temp1, temp2 = ind1[i], ind2[i]

        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2

        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp1] = p2[temp2], p2[temp1]
    
    return ind1, ind2

def mutOneSwap(individual, prob):
    for i in range(len(individual) - 1):
        if random.random() < prob:
            individual[i], individual[i+1] = individual[i+1], individual[i]
    return individual

toolbox_q.register("evaluate", evalPoints)
toolbox_q.register("mate", cxPartiallyMatched)
toolbox_q.register("mutate", mutOneSwap, prob=2.0/n)
toolbox_q.register("select", tools.selTournament, tournsize=3)

pop = toolbox_q.population(n=300)

fitnesses = list(map(toolbox_q.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

gen = range(100)
avg_list = []
max_list = []
min_list = []

for g in gen:
    print("-- Generation %i --" % g)

    offspring = toolbox_q.select(pop, len(pop))
    offspring = list(map(toolbox_q.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:
            toolbox_q.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    
    for mutant in offspring:
        if random.random() < 0.2:
            toolbox_q.mutate(mutant)
            del mutant.fitness.values
    
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(map(toolbox_q.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    pop[:] = offspring

    fits = [ind.fitness.values[0] for ind in pop]
    length = len(fits)
    mean = sum(fits) / length
    g_max = max(fits)
    g_min = min(fits)

    avg_list.append(mean)
    max_list.append(g_max)
    min_list.append(g_min)

    print("Min %s" % g_min)
    print("Max %s" % g_max)
    print("Average %s" % mean)

print("-- End of evolution process --")

best_ind = tools.selBest(pop, 1)[0]
worst_ind = tools.selWorst(pop, 1)[0]
print("Best individual has a distance of %s: %s" % (best_ind.fitness.values, best_ind))

print(avg_list, len(avg_list))

import matplotlib.pyplot as plt

plt.plot(gen, avg_list, label="average")
plt.plot(gen, min_list, label="minimum")
plt.plot(gen, max_list, label="maximum")
plt.title("I'm just that guy")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="upper right")
plt.show()


x, y = [points[i][0] for i in worst_ind], [points[j][1] for j in worst_ind]
plt.plot(x, y, color='blue')
x, y = [points[i][0] + 200 for i in best_ind], [points[j][1] for j in best_ind]
plt.plot(x, y, color='red')
plt.show()
'''

import random, math

from deap import base, creator, tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("IndividualPoint", list, fitness=creator.FitnessMin)


def generatePoints(n):
    points = []
    for p in range(n):
        points.append((random.randint(-100, 100), random.randint(-100, 100)))
    return points

def findDistance(c1, c2):
    return math.sqrt((c2[0]-c1[0])**2+(c2[1]-c1[1])**2)

n = 100
points = generatePoints(n)

pointsLeft = points[:]

def nearestNeighbor():
    individual = []
    currentPoint = pointsLeft[0]
    del pointsLeft[0]
    individual.append(currentPoint)
    pointsLeftLeft = points[:]
    shortest = math.inf
    while pointsLeftLeft:
        for pointIndex in range(len(pointsLeftLeft)):
            dist = findDistance(currentPoint, pointsLeftLeft[pointIndex])
            if dist < shortest:
                shortest = dist
                closestPointIndex = pointIndex
        currentPoint = pointsLeftLeft[closestPointIndex]
        del pointsLeftLeft[pointIndex]
        individual.append(currentPoint)
    return individual


toolbox_q = base.Toolbox()
toolbox_q.register("permutation", nearestNeighbor)

toolbox_q.register("individual", tools.initIterate, creator.IndividualPoint, toolbox_q.permutation)
toolbox_q.register("population", tools.initRepeat, list, toolbox_q.individual)

def evalPoints(individual):
    dist = 0
    for i in range(len(individual)-1):
        point1 = points[individual[i]]
        point2 = points[individual[i+1]]
        dist += math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)
    return dist,

def cxPartiallyMatched(ind1, ind2):
    size = len(ind1)
    p1 = p2 = [0] * size

    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i

    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint1 < cxpoint2: cxpoint2 += 1
    else: cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    for i in range(cxpoint1, cxpoint2):
        temp1, temp2 = ind1[i], ind2[i]

        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2

        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp1] = p2[temp2], p2[temp1]
    
    return ind1, ind2

def mutOneSwap(individual, prob):
    for i in range(len(individual) - 1):
        if random.random() < prob:
            individual[i], individual[i+1] = individual[i+1], individual[i]
    return individual

toolbox_q.register("evaluate", evalPoints)
toolbox_q.register("mate", cxPartiallyMatched)
toolbox_q.register("mutate", mutOneSwap, prob=2.0/n)
toolbox_q.register("select", tools.selTournament, tournsize=3)

pop = toolbox_q.population(n=100)

fitnesses = list(map(toolbox_q.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

gen = range(100)
avg_list = []
max_list = []
min_list = []

for g in gen:
    print("-- Generation %i --" % g)

    offspring = toolbox_q.select(pop, len(pop))
    offspring = list(map(toolbox_q.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:
            toolbox_q.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    
    for mutant in offspring:
        if random.random() < 0.2:
            toolbox_q.mutate(mutant)
            del mutant.fitness.values
    
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(map(toolbox_q.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    pop[:] = offspring

    fits = [ind.fitness.values[0] for ind in pop]
    length = len(fits)
    mean = sum(fits) / length
    g_max = max(fits)
    g_min = min(fits)

    avg_list.append(mean)
    max_list.append(g_max)
    min_list.append(g_min)

    print("Min %s" % g_min)
    print("Max %s" % g_max)
    print("Average %s" % mean)

print("-- End of evolution process --")

best_ind = tools.selBest(pop, 1)[0]
worst_ind = tools.selWorst(pop, 1)[0]
print("Best individual has a distance of %s: %s" % (best_ind.fitness.values, best_ind))

print(avg_list, len(avg_list))

import matplotlib.pyplot as plt

plt.plot(gen, avg_list, label="average")
plt.plot(gen, min_list, label="minimum")
plt.plot(gen, max_list, label="maximum")
plt.title("I'm just that guy")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="upper right")
plt.show()


x, y = [points[i][0] for i in worst_ind], [points[j][1] for j in worst_ind]
plt.plot(x, y, color='blue')
x, y = [points[i][0] + 200 for i in best_ind], [points[j][1] for j in best_ind]
plt.plot(x, y, color='red')
plt.show()
'''
