### EECS 349: Machine Learning
### Ryan Masson, Jeff Holm, Theo Bisdikian, Sebastian Garcia
### genetic, hill-climbing algorithm for learning a Coup game strategy

import random
import copy
import game
import decisionary

DICTIONARY = {}
decisionary.MakeDD(DICTIONARY)

CHROMOSOME_SIZE = 172  # based on the hard-coded game tree; do not change unless tree changes
POPULATION_SIZE = 50    # must be even number
NUM_GENERATIONS = 100
CROSSOVER_RATE = 0.0
MUTATION_RATE = 0.00
BOUNDED_MUTATION_RATE = 0.00   
MUTATION_BOUND = 5
NUMPLAYS = 50
TRAIN_ON_ONE_BASEBOT = 1
TEST_ON_ONE_BASEBOT = 1   # if 1, will test each gen against just one bot in the first gen.
                          # else tests against the entire first generation 



def GeneticCoup():

    #### POPULATION CREATION
    botpop = {}
    for i in range(POPULATION_SIZE):
        # randomly create feature vector 
        bot_vector = [random.randint(1,100) for j in range(CHROMOSOME_SIZE)]
        bot_vector = Normalize(bot_vector, decisionary.delineation)
        # construct dictionary where bot_name --> vector, fitness
        botpop[i] = [bot_vector, 0.0]

    first_gen = copy.copy(botpop)
    base_bot = first_gen[0][0]

    fitness_sum = 0.0
    avg_gen_fitness = 0.0
    for pop in range(NUM_GENERATIONS):
        botpop = GenerationProcess(botpop, base_bot)

        filename = "generation_" + str(pop+1) + ".csv"
        open(filename, 'w').close()
        for i in range(POPULATION_SIZE):
            write(filename, botpop[i][0])

        print "completed " + str(pop+1) + " generations"

        for j in range(POPULATION_SIZE):
            filename = "generation_" + str(pop+1) + ".csv"
            curr_bot = read(filename, j)
            if TEST_ON_ONE_BASEBOT:
                # test every bot against only one bot, for consistency
                fitness_sum += TestOneBotAgainstOne(curr_bot, base_bot)
            else:
                # test every bot against the first generation and add its fitness to sum
                fitness_sum += TestOneBotAgainstAll(curr_bot, first_gen)

        avg_gen_fitness = fitness_sum / POPULATION_SIZE
        fitness_sum = 0.0
        print "the average fitness of bots in gen " + str(pop+1) + " is " + str(avg_gen_fitness)

    '''
    ##### EVALUATION OF ALL GENERATIONS  (uncomment this if you want to test after)
    fitness_sum = 0.0
    avg_gen_fitness = 0.0
    for i in range(NUM_GENERATIONS):
        for j in range(POPULATION_SIZE):
            filename = "generation_" + str(i+1) + ".csv"
            curr_bot = read(filename, j)
            if TEST_ON_ONE_BASEBOT:
                # test every bot against only one bot, for consistency
                fitness_sum += TestOneBotAgainstOne(curr_bot, first_gen[0][0])
            else:
                # test every bot against the first generation and add its fitness to sum
                fitness_sum += TestOneBotAgainstAll(curr_bot, first_gen)

        avg_gen_fitness = fitness_sum / POPULATION_SIZE
        fitness_sum = 0.0
        print "the average fitness of bots in gen " + str(i+1) + " is " + str(avg_gen_fitness)
    '''

def GenerationProcess(botpop, base_bot):
    botpop = TestBotFitness(botpop, base_bot)
    botpop = SelectAndCrossover(botpop)
    botpop = Mutate(botpop)
    return botpop


def TestBotFitness(botpop, base_bot):
    # test each chromosome by running the game, assign a fitness score
    for bot_name, vec_fitness_pair in botpop.iteritems(): 
        bot_vector = vec_fitness_pair[0]
        # run the game, based on bot_vector 
        if TRAIN_ON_ONE_BASEBOT:
            fitness = TestOneBotAgainstOne(bot_vector, base_bot)
        else:
            fitness = TestOneBotAgainstAll(bot_vector, botpop)
        botpop[bot_name][1] = fitness
    return botpop


def SelectAndCrossover(botpop):
    # selection new population based on probabilites weighted by fitness score, with crossover
    fitness_total = 0
    #roulette_total = 0
    new_botpop = {}

    for bot_name in botpop:
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
            for bot_name in botpop:
                if r <= probs[bot_name]:
                    newbots.append(bot_name)
                    break

        #### CROSSOVER
        newbots = Crossover(botpop,newbots)
        new_botpop[i] = newbots[0]
        new_botpop[i+1] = newbots[1]
        '''
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
        '''
        i += 2

    return new_botpop

def Crossover(botpop,newbots):
    # botx = [feature_vector[], fitness]
    bot1 = botpop[newbots[0]]
    bot2 = botpop[newbots[1]]

    vec1 = bot1[0]
    vec2 = bot2[0]

    for bound in decisionary.delineation:
        roll = random.random()
        if roll <= CROSSOVER_RATE:
            temp_vec = copy.copy(vec1)
            indices = [i+bound[0] for i in range(bound[1]-bound[0]+1)]
            for index in indices:
                vec1[index] = vec2[index]
                vec2[index] = temp_vec[index]

    bot1[0] = vec1
    bot2[0] = vec2
    return [bot1, bot2]

def Mutate(botpop):
    # botpop is a dictionary of botpop[bot_name] = [feature_vector[], fitness]
    for bot_name in botpop:
        for bound in decisionary.delineation:

            # FULL RANDOM MUTATION
            roll = random.random()
            if roll <= MUTATION_RATE:
                indices = [i+bound[0] for i in range(bound[1]-bound[0]+1)]
                for index in indices:
                    botpop[bot_name][0][index] = random.randint(1,100)
                botpop[bot_name][0] = Normalize(botpop[bot_name][0], [bound])

            # BOUNDED MUTATION
            roll = random.random()
            if roll <= BOUNDED_MUTATION_RATE:
                indices = [i+bound[0] for i in range(bound[1]-bound[0]+1)]
                for index in indices:
                    botpop[bot_name][0][index] += random.randint(-MUTATION_BOUND, MUTATION_BOUND)
                    botpop[bot_name][0][index] = max(botpop[bot_name][0][index], 0)
                    botpop[bot_name][0][index] = min(botpop[bot_name][0][index], 100)
                botpop[bot_name][0] = Normalize(botpop[bot_name][0], [bound])
                
    return botpop


def TestOneBotAgainstAll(vector, botpop):
    # play this bot/vector against every bot in the botpop
    wins = 0
    games_played = 0.0 
    for i in range(POPULATION_SIZE):
        for j in range(NUMPLAYS):
            wins += game.GeneticPlay(vector, botpop[i][0], DICTIONARY)
            games_played += 1.0
    win_percentage = wins / games_played
    return win_percentage


def TestOneBotAgainstOne(player, opponent):
    wins = 0
    games_played = 0.0 
    for i in range(NUMPLAYS):
        wins += game.GeneticPlay(player, opponent, DICTIONARY)
        games_played += 1.0
    win_percentage = wins / games_played
    return win_percentage


def read(filename, linenum):
    with open(filename, "r") as file:
        data = file.readlines()
    line = map(int, data[linenum].strip().split(','))
    file.close()
    return line

def Normalize(vector, bounds):
    for bound in bounds:
        sum = 0.0
        indices = [i+bound[0] for i in range(bound[1]-bound[0]+1)]
        for index in indices:
            sum += vector[index]
        for index in indices:
            vector[index] = int(round((vector[index] / sum) * 100.0))
    return vector


def write(filename, vector):
    file = open(filename, "a")
    write_str = ""
    for value in vector:
        write_str += str(value) + ","
    file.write(write_str[:-1] + '\n')
    file.close()

wGeneticCoup()