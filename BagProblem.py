import pandas as pd
import matplotlib.pyplot as plt
import random
import time

crossover_probability = 0.9
mutation_probability = 0.1
population_size = 400
elite_size = 20
load_capacity = 250
number_generations = 100

objects = pd.read_csv('objetos.txt', sep=';')

number_genes = len(objects)


def individual():
    individual = [random.randint(0, 1) for i in range(number_genes)]
    validate(individual)
    return individual


def validate(individual):
    load = calculate_load(individual)
    less_position = 0
    values = sorted(objects['valor'])
    while (load > load_capacity):
        load = 0
        less = values[less_position]
        index = objects['valor'].values.tolist().index(less)
        individual[index] = 0
        less_position += 1
        load = calculate_load(individual)


def create_population():
    return [individual() for i in range(population_size)]


def fitness(individual):
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            fitness += objects.at[i, 'valor']
    return fitness


def calculate_load(individual):
    load = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            load += objects.at[i, 'peso']
    return load


def selection_and_crossover(population):
    scored = sort_population(population)
    population = scored
    elite = population[(len(population) - elite_size):]
    for i in range(len(population) - elite_size):
        if (random.random() <= crossover_probability):
            point = random.randint(1, number_genes - 1)
            parents = random.sample(elite, 2)
            population[i][:point] = parents[0][:point]
            population[i][point:] = parents[1][point:]
            validate(population[i])
    return population


def mutation(population):
    for i in range(len(population) - elite_size):
        if (random.random() <= mutation_probability):
            point = random.randint(0, number_genes - 1)
            new_value = random.randint(0, 1)
            while (new_value == population[i][point]):
                new_value = random.randint(0, 1)
            population[i][point] = new_value
            validate(population[i])
    return population


def sort_population(population):
    return [i[1] for i in sorted([(fitness(j), j) for j in population])]


print('-' * 45)
print('Algoritmo da Mochila')
print('-' * 45)
print('N??mero de genes dos indiv??duos: {}\n'.format(number_genes))
print('Taxa de crossover: {}%\n'.format(crossover_probability * 100))
print('Taxa de muta????o: {}%\n'.format(mutation_probability * 100))
print('Tamanho da popula????o: {} indiv??duos\n'.format(population_size))
print('Elitismo: {} indiv??duos\n'.format(elite_size))
print('Peso m??ximo suportado pela mochila: {}'.format(load_capacity))
print('-' * 45)
print('\n')
population = create_population()
elite = [None] * len(population)
elite = sort_population(population)[(len(population) - elite_size):]
print('Elite inicial:\n')
for i in elite:
    print('Indiv??duo: {} | Valor: {} | Peso: {}\n'.format(
        i, fitness(i), calculate_load(i)))
print('Realizando o crossover e muta????o para 100 gera????es...\n')
generations = []
generation_fitness = []
tempExec = []

l = 1
for j in range(2, 11):
    number_generations = j*10
    ini = time.time()
    generations.append((l + 1)*10)
    l=l+1
    for i in range(number_generations):
        generation_fitness.append(
            fitness(sort_population(population)[population_size - 1]))
        population = selection_and_crossover(population)
        population = mutation(population)
    fim = time.time()
    tempExec.append(fim-ini)
print('Elite final:\n')
elite = sort_population(population)[(len(population) - elite_size):]
for i in elite:
    print('Indiv??duo: {} | Valor: {} | Peso: {}\n'.format(
        i, fitness(i), calculate_load(i)))

print(tempExec)
plt.plot(generations, tempExec)
plt.title('Tempo levado')
plt.xlabel('Gera????es')
plt.ylabel('Tempo(s)')
plt.show()