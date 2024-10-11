import CircuitEquivalentEC13 as CE
import numpy as np
import random
import converterNum as CN

input = CE.Z_total
y_ref = input

f = CE.dec_step(1e-2, 1e5, 72)

# 11 to 47 : generate single E value. Number of E's = Number of calls to gen_num()
def gen_comp(component_type):
    if component_type == "r":
        value = random.randint(15, 100000)
    elif component_type == "c":
        value = random.uniform(1e-6, 1e-3)
    elif component_type == "l":
        value = random.uniform(1, 20)
    elif component_type == "y":
        value = random.uniform(1e-6, 1e-3)
    elif component_type == "n":
        value = random.uniform(0.5, 1)
    elif component_type == "w":
        value = random.randint(1, 5000)
    else:
        raise ValueError("Invalid component type")

    return CN.conv2seq(value)

# generate 8 values of each component
def generate_components():
    components = {}
    for component_type in ["r", "c", "l", "y", "n", "w"]:
        components[component_type] = [gen_comp(component_type) for _ in range(8)]
    return components
    # o/p is a dictionary

# concatenate components in order to get a single string and get cnt
def concatenate_components(components):
    output = "".join([components[component_type][i] for i in range(8) for component_type in ["r", "l", "c", "w", "y", "n"]])
    cnt = np.random.randint(2, size=5)
    output += "".join(str(cnt[i]) for i in range(5))
    return output
    
def gen_num():
    components = generate_components()
    return concatenate_components(components)


# 50 to 56 : generate pool of E values by generate_pool(100)
def generate_pool(pool_size):
    pool = []
    for i in range(pool_size):
        E_pool = gen_num()
        pool.append(E_pool)
    return pool
 

# 59 to 78 : generate fitness array for whole population by line 80
def fitness_function(E, y_ref):
    
    # Calculate the frequency response of the circuit equivalent
    y = np.array([CE.gen_freq_response(E,freq) for freq in f])
    
    # Calculate the mean absolute error
    if len(y) != len(y_ref):
        raise ValueError("Arrays must have the same length.")

    # Calculate absolute differences between corresponding elements
    absolute_differences = [abs(a - b) for a, b in zip(y, y_ref)]

    # Calculate the mean of absolute differences
    mae = sum(absolute_differences) / len(y)
    
    # calculate rms of mae
    rms = np.sqrt(np.mean(np.square(mae)))
    
    return rms
    
# init_fitness = [fitness_function(E, y_ref) for E in initial_population]

# 82 to 117 : defines crossover,mutate,IfMutate functions
def CrossOver(E1,E2):
    E1 = str(E1)
    E2 = str(E2)
    # Choose a random crossover point
    crossover_point = random.randint(1, len(E1) - 1)
    
    # Perform crossover
    E1_new = E1[:crossover_point] + E2[crossover_point:]
    E2_new = E2[:crossover_point] + E1[crossover_point:]
    
    return E1_new,E2_new

def Mutate(E):
    E = str(E)
    # Choose a random mutation point
    mutation_point = random.randint(0, len(E) - 1)
    
    # check which digits are not present in E and form the set
    digitsNotPresent = set("0123456789") - set(E)
    if not digitsNotPresent:
        digitsNotPresent = set("0123456789")

    if (mutation_point > 431) or ((mutation_point + 1) % 8 == 0):
        mutated_bit = random.randint(0, 1)
    else:
        # Choose a random digit to replace the current digit from the set
        mutated_bit = random.choice(list(digitsNotPresent))
    
    # Perform mutation
    E_new = E[:mutation_point] + str(mutated_bit) + E[mutation_point + 1:]
    
    return E_new

def IfMutate():
    return random.random()

# To Note : Here the lower the fitness, the better it is.

def GeneticAlgorithm(population, y_ref, mutation_rate, generations):
    fitness = [fitness_function(E, y_ref) for E in population]
    tolerance = 144*3
    
    for generation in range(generations):
        while min(fitness) > tolerance:

            #print(f"Generation {generation + 1}...")

            # Select parents which have best fitness
            parent_indices = np.argsort(fitness)[:2]

            parent1 = population[parent_indices[0]]
            parent2 = population[parent_indices[1]]

            # Perform crossover : always
            child1, child2 = CrossOver(parent1, parent2)

            # Mutate children : coin toss
            if IfMutate() < mutation_rate:
                child1 = Mutate(child1)
            if IfMutate() < mutation_rate:
                child2 = Mutate(child2)

            # Calculate fitness for children
            fitness_child1 = fitness_function(child1, y_ref)
            fitness_child2 = fitness_function(child2, y_ref)

            # Replace parents with children if they have better fitness
            if fitness_child1 < fitness[parent_indices[0]]:
                population[parent_indices[0]] = child1
                fitness[parent_indices[0]] = fitness_child1
            if fitness_child2 < fitness[parent_indices[1]]:
                population[parent_indices[1]] = child2
                fitness[parent_indices[1]] = fitness_child2

    print(f"Generation reached: {generation + 1}")
    if fitness_function(child1, y_ref) < fitness_function(child2, y_ref):
        return child1, fitness_function(child1, y_ref)
    else:
        return child2, fitness_function(child2, y_ref)
    

# Running Trial...
population = generate_pool(100)
E, fitness = GeneticAlgorithm(population, y_ref, 0.5, 10_000_000)
print(f"E: {E}, Fitness: {fitness}")
r,l,c,w,y,n,cnt = CE.get_component_values(E)
print(f"R: {r},\n L: {l},\n C: {c},\n W: {w},\n Y: {y},\n N: {n},\n CNT: {cnt},\n")

"""
1. some complex exponentiation error
2. all blocks are running:
    i. do we need to restrict some blocks? as in best fit to nth block
    ii. --forgot--  minimize the number of blocks
"""