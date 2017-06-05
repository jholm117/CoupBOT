### EECS 349: Machine Learning
### Ryan Masson, Jeff Holm, Theo Bisdikian, Sebastian Garcia
### genetic, hill-climbing algorithm for learning a Coup game strategy

import random
import copy
import game
import decisionary


CHROMOSOME_SIZE = 173  # based on the hard-coded game tree; do not change unless tree changes
POPULATION_SIZE = 100  # must be even number
NUM_GENERATIONS = 2
CROSSOVER_RATE = 0.6
MUTATION_RATE = 0.01
NUMPLAYS = 250
DICTIONARY = {}
decisionary.MakeDD(DICTIONARY)


def genetic_coup():

    #### POPULATION CREATION
    botpop = {}
    for i in range(POPULATION_SIZE):
        # randomly create feature vector 
        bot_vector = [random.randint(0,100) for j in range(CHROMOSOME_SIZE)]
        # construct dictionary where bot_name --> vector, fitness
        botpop[i] = [bot_vector, 0]

    first_gen = copy.copy(botpop)

    for pop in range(NUM_GENERATIONS):
        botpop = generation_process(botpop)
        filename = "generation_" + str(pop+1) + ".csv"
        open(filename, 'w').close()
        for i in range(POPULATION_SIZE):
            write(filename, botpop[i][0])
        print "completed " + str(pop+1) + " generations"

    ##### EVALUATION OF ALL GENERATIONS
    fitness_sum = 0.0
    avg_gen_fitness = 0.0
    for i in range(NUM_GENERATIONS):
        for j in range(POPULATION_SIZE):
            filename = "generation_" + str(i+1) + ".csv"
            curr_bot = read(filename, j)
            # test every bot against the first generation and add its fitness to sum
            fitness_sum += test_one_bot_against_all(curr_bot, first_gen)
        avg_gen_fitness = fitness_sum / POPULATION_SIZE
        fitness_sum = 0.0
        print "the average fitness of bots in gen " + str(i+1) + " is " + str(avg_gen_fitness)


def generation_process(botpop):
    #### FITNESS TESTING 
    botpop = test_bot_fitness(botpop)
    #### SELECTION:
    botpop = select_and_crossover(botpop)
    # MUTATION:
    botpop = mutate(botpop)
    return botpop


def test_bot_fitness(botpop):
    # test each chromosome by running the game, assign a fitness score
    for bot_name, vec_fitness_pair in botpop.iteritems(): 
        bot_vector = vec_fitness_pair[0]
        # run the game, based on bot_vector 
        fitness = test_one_bot_against_all(bot_vector, botpop)
        botpop[bot_name][1] = fitness
    return botpop


def select_and_crossover(botpop):
    # selection new population based on probabilites weighted by fitness score, with crossover
    fitness_total = 0
    roulette_total = 0
    new_botpop = {}

    for bot_name, pair in botpop.iteritems():
        fitness_total += botpop[bot_name][1]

    # array of probabilities for each bot, based on fitness
    rel_fitness = [botpop[bot][1]/fitness_total for bot in botpop]

    # generate probability/roulette wheel intervals 
    probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]

    # draw new population
    i = 0
    while i < len(botpop):
        # select two bots
        newbots = []
        for k in range(2):
            r = random.random()
            for bot_name, pair in botpop.iteritems():
                if r <= probs[bot_name]:
                    newbots.append(bot_name)
                    break

        #### CROSSOVER
        cross = random.random()
        if cross < CROSSOVER_RATE:
            # choose the crossover point, crossover 
            crossover_point = random.randint(0, CHROMOSOME_SIZE)
            bot1 = botpop[newbots[0]]
            bot2 = botpop[newbots[1]]
            chrom1 = bot1[0]
            chrom1_copy = copy.copy(chrom1)
            chrom2 = bot2[0]
            chrom1[crossover_point:CHROMOSOME_SIZE] = chrom2[crossover_point:CHROMOSOME_SIZE]
            chrom2[crossover_point:CHROMOSOME_SIZE] = chrom1_copy[crossover_point:CHROMOSOME_SIZE]
            bot1[0] = chrom1
            bot2[0] = chrom2
            # add newbots to the new_botpop
            new_botpop[i] = bot1
            new_botpop[i+1] = bot2
        else:
            # add newbots to the new_botpop
            new_botpop[i] = botpop[newbots[0]]
            new_botpop[i+1] = botpop[newbots[1]]

        i += 2

    return new_botpop


def mutate(botpop):
    # loop through all the values of each chromosome; change a value with MUTATION_RATE probability
    # this gives some genetic diversity to the popualtion

    for bot_name, pair in botpop.iteritems():
        for i,val in enumerate(pair[0]):
            r = random.random()
            if r <= MUTATION_RATE:
                mutated = random.randint(1, 99)
                botpop[bot_name][0][i] = mutated 
    return botpop


def test_one_bot_against_all(vector, botpop):
    # play this bot/vector against every bot in the botpop
    wins = 0
    games_played = 0.0 
    for i in range(POPULATION_SIZE):
        for j in range(NUMPLAYS):
            wins += game.GeneticPlay(vector, botpop[i][0], DICTIONARY)
            games_played += 1.0
    win_percentage = wins / games_played
    return win_percentage


def read(filename, linenum):
    with open(filename, "r") as file:
        data = file.readlines()
    line = map(int, data[linenum].strip().split(','))
    file.close()
    return line


def write(filename, vector):
    file = open(filename, "a")
    write_str = ""
    for value in vector:
        write_str += str(value) + ","
    file.write(write_str[:-1] + '\n')
    file.close()

def normalize(vector, bounds):
    for bound in bounds:
        sum = 0.0
        indices = [i+bound[0] for i in range(bound[1]-bound[0]+1)]
        for index in indices:
            sum += vector[index]
        for index in indices:
            vector[index] = int(round(vector[index] * 100.0 / sum))


#genetic_coup()