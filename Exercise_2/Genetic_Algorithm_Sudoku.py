import numpy as np
import random
import operator
import math
from past.builtins import range


random.seed()

# For grid 9*9, we have 9 subgrid with size 3x3. In genetic algorithm,
# each row: gene
# each chromosome: 9 row - 9 gene

grid_size = 9 # Number of element in row, column or subgird
epsilon = 1e-5

class Chromosome(object):
    """ A chromosome for a sudoku puzzle"""

    def __init__(self):
        self.values = np.zeros((grid_size, grid_size))
        self.fitness = 0

    def update_fitness(self):
        """The fitness function is determined by how closed it is to being actual
        solution of the puzzle"""


        column_count = np.zeros(grid_size)
        subgrid_count = np.zeros(grid_size)
        column_fitness_sum = 0.0
        subgrid_fitness_sum = 0.0

        self.values = self.values.astype(int) # Change to int type because of slice :

        for column in range(grid_size):
            for row in range(grid_size):
                column_count[self.values[row][column] - 1] += 1

            for i in range(grid_size):
                if column_count[i] == 1:
                    column_fitness_sum += (1.0/ grid_size)/ grid_size

            column_count = np.zeros(grid_size) #Reset

        for i in range(0, grid_size, 3):
            for j in range(0, grid_size, 3):
                subgrid_count[self.values[i][j] - 1] += 1
                subgrid_count[self.values[i+1][j] - 1] += 1
                subgrid_count[self.values[i+2][j] - 1] += 1
                subgrid_count[self.values[i][j+1] - 1] += 1
                subgrid_count[self.values[i+1][j+1] - 1] += 1
                subgrid_count[self.values[i+2][j+1] - 1] += 1
                subgrid_count[self.values[i][j+2] - 1] += 1
                subgrid_count[self.values[i+1][j+2] - 1] += 1
                subgrid_count[self.values[i+2][j+2] - 1] += 1

                for k in range(grid_size):
                    if subgrid_count[k] == 1:
                        subgrid_fitness_sum += (1.0/grid_size)/grid_size

                subgrid_count = np.zeros(grid_size) #Reset

        if (abs(column_fitness_sum - 1.0) < epsilon) and (abs(subgrid_fitness_sum - 1.0) < epsilon):
            fitness = 1.0
        else:
            fitness = column_fitness_sum * subgrid_fitness_sum

        self.fitness = fitness
        return

    def mutate(self, mutation_rate, given_grid):
        """
            - mutation_rate: The rate in order to specify the probability of mutation
                             of a chromosome
            - given_grid: The given grid before handle, read from file
            - Mutation operator: Choose one row and 2 element in that row and swap if
                                 it not a predetermined element in a given_grid
        """

        r = random.uniform(0, 1)

        mutate_occurred = False # Determine whether the mutation is occurred

        if r < mutation_rate: #Mutate
            while not mutate_occurred:
                row = random.randint(0, grid_size - 1)

                random_column = np.random.choice(grid_size, size=2 ,replace=False)

                from_column, to_column = random_column[0], random_column[1]

                if given_grid.values[row][from_column] == 0 and given_grid.values[row][to_column] == 0:
                    if not given_grid.is_column_duplicate(to_column, self.values[row][from_column])  \
                        and not given_grid.is_column_duplicate(from_column, self.values[row][to_column]) \
                        and not given_grid.is_subgrid_duplicate(row, to_column, self.values[row][from_column]) \
                        and not given_grid.is_subgrid_duplicate(row, from_column, self.values[row][to_column]):

                        temp = self.values[row][from_column]
                        self.values[row][from_column] = self.values[row][to_column]
                        self.values[row][to_column] = temp
                        mutate_occurred = True

        return mutate_occurred


class Fixed(Chromosome):

    def __init__(self, values):
        self.values = values
        return

    def is_row_duplicate(self, row, value):
        """ Check duplicate in a row. """
        for column in range(grid_size):
            if self.values[row][column] == value:
                return True
        return False

    def is_column_duplicate(self, column, value):
        """ Check duplicate in a column. """
        for row in range(0, grid_size):
            if self.values[row][column] == value:
                return True
        return False

    def is_subgrid_duplicate(self, row, column, value):
        """ Check duplicate in a subgrid. """
        h = self.make_index(row)
        k = self.make_index(column)

        for i in range(h, h + 3):
            for j in range(k, k + 3):
                if self.values[i][j] == value:
                    return True
        return False

    def make_index(self, v):
        if v < 9 and v >= 0:
            return 3 * (v // 3)
        else:
            raise Exception("Exceed grid_size")

    def no_duplicate(self):
        for row in range(grid_size):
            for column in range(grid_size):
                if self.values[row][column] != 0:
                    row_check = list(self.values[row]).count(self.values[row][column])
                    col_check = list(self.values[:,column]).count(self.values[row][column])

                    h = self.make_index(row)
                    k = self.make_index(column)

                    block_check = self.values[h: h + 3, k: k + 3]
                    block_check = [int(x) for y in block_check for x in y]
                    block_check = block_check.count(self.values[row][column])

                    if row_check > 1 or  col_check > 1 or block_check > 1:
                        return False
        return True

class Population(object):
    """ A set of chromosome solutions to the Sudoku puzzle."""
    def __init__(self):
        self.chromosomes = []


    """
        Generate the population
    """
    def generate_chromosomes(self, population_size, given_grid):
        self.chromosomes = []

        # Determine the legal values that each square can take.
        helper = Chromosome()

        helper.values = [[[] for j in range(0, grid_size)] for i in range(0, grid_size)]

        for row in range(grid_size):
            for col in range(grid_size):
                for value in range(1, 10):
                    if given_grid.values[row][col] == 0 and \
                        not (given_grid.is_column_duplicate(col, value) \
                             or given_grid.is_subgrid_duplicate(row, col, value) \
                             or given_grid.is_row_duplicate(row, value)):
                        helper.values[row][col].append(value)
                    elif given_grid.values[row][col] != 0:
                        helper.values[row][col].append(given_grid.values[row][col])
                        break
        # Generate a population
        for p in range(0, population_size):
            g = Chromosome()
            for i in range(0, grid_size):  # New row: gene in chromosome.
                row = np.zeros(grid_size)

                # Fill in the givens.
                for j in range(0, grid_size):  # New column j value in row i.

                    # If value is already given, don't change it.
                    if given_grid.values[i][j] != 0:
                        row[j] = given_grid.values[i][j]
                    # Fill in the gaps using the helper board.
                    elif given_grid.values[i][j] == 0:
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                # If we don't have a valid board, then try again. max iteration 500,000
                # There must be no duplicates in the row.
                ii = 0
                while len(list(set(row))) != grid_size:
                    ii += 1
                    if ii > 500000:
                        return 0
                    for j in range(0, grid_size):
                        if given_grid.values[i][j] == 0:
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                g.values[i] = row
            # print(g.values)
            self.chromosomes.append(g)
            # print(self.chromosomes[0])
            # Compute the fitness of all chromosome in the population.

        self.update_fitness()


        # print("Seeding complete.")

        return 1

    def update_fitness(self):
        """ Update fitness of every chromosome. """
        for chromosome in self.chromosomes:
            chromosome.update_fitness()
        return

    def sort(self):
        """ Sort the population based on fitness. Ascending order"""
        self.chromosomes = sorted(self.chromosomes, key=operator.attrgetter('fitness'))
        return

class Tournament(object):
    """ The crossover function requires two parents to be selected from the population pool. The Tournament class is used to do this.
    Two individuals are selected from the population pool and a random number in [0, 1] is chosen. If this number is less than the 'selection rate' (e.g. 0.85), then the fitter individual is selected; otherwise, the weaker one is selected.
    """

    def __init__(self):
        return

    def compete(self, chromosomes):
        """ Pick 2 random candidates from the population and get them to compete against each other. """
        c1 = chromosomes[random.randint(0, len(chromosomes) - 1)]
        c2 = chromosomes[random.randint(0, len(chromosomes) - 1)]
        f1 = c1.fitness
        f2 = c2.fitness

        # Find the fittest and the weakest.
        if (f1 > f2):
            fittest = c1
            weakest = c2
        else:
            fittest = c2
            weakest = c1


        selection_rate = 0.80
        r = random.uniform(0, 1)

        if (r < selection_rate):
            return fittest
        else:
            return weakest

class Crossover(object):
    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        pass

class CycleCrossover(Crossover):
    """ Crossover relates to the analogy of genes within each parent candidate
    mixing together in the hopes of creating a fitter child candidate.
    Cycle crossover is used here (see e.g. A. E. Eiben, J. E. Smith.
    Introduction to Evolutionary Computing. Springer, 2007). """

    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes. """
        child1 = Chromosome()
        child2 = Chromosome()

        # Make a copy of the parent genes.
        child1.values = np.copy(parent1.values)
        child2.values = np.copy(parent2.values)

        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)

        # Perform crossover.
        if (r < crossover_rate):
            # Pick a crossover point. Crossover must have at least 1 row (and at most Nd-1) rows.
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)
            while (crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(1, 9)

            if (crossover_point1 > crossover_point2):
                temp = crossover_point1
                crossover_point1 = crossover_point2
                crossover_point2 = temp

            for i in range(crossover_point1, crossover_point2):
                child1.values[i], child2.values[i] = self.crossover_rows(child1.values[i], child2.values[i])

        return child1, child2

    def crossover_rows(self, row1, row2):
        child_row1 = np.zeros(grid_size)
        child_row2 = np.zeros(grid_size)

        remaining = [*range(1, grid_size + 1)]
        cycle = 0

        while ((0 in child_row1) and (0 in child_row2)):  # While child rows not complete...
            if (cycle % 2 == 0):  # Even cycles.
                # Assign next unused value.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row1[index]
                child_row2[index] = row2[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row1[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row2[index]
                    next = row2[index]

                cycle += 1

            else:  # Odd cycle - flip values.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row2[index]
                child_row2[index] = row1[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]
                    next = row2[index]

                cycle += 1

        return child_row1, child_row2

    def find_unused(self, parent_row, remaining):
        for i in range(0, len(parent_row)):
            if (parent_row[i] in remaining):
                return i

    def find_value(self, parent_row, value):
        for i in range(0, len(parent_row)):
            if (parent_row[i] == value):
                return i

class Sinusoidal_Motion_Crossover(Crossover):
    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        pass



class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.population = None
        self.given_grid = None

    def load_data(self, given):
        self.given_grid = Fixed(given)
        return

    def solve(self):
        self.population = None
        population_size = 1000                          # Population size
        num_elites = int(0.05 * population_size)        # Number of elites
        num_generations = 10000                         # Number of generations
        num_mutations = 0                               # Number of mutations

        # Mutation parameter
        phi = 0
        sigma = 1
        mutation_rate = 0.06

        # Check given_grid one first
        if self.given_grid.no_duplicate() == False:
            return (-1, 1)

        # Create an initial population
        self.population = Population()
        print("create an initial population.")

        if self.population.generate_chromosomes(population_size, self.given_grid) == 1:
            pass
        else:
            return (-1, 1)

        # For up to 10000 generations...
        stale = 0
        for generation in range(num_generations):
            # Check for a solution
            best_fitness = 0.0
            for c in range(population_size):
                fitness = self.population.chromosomes[c].fitness
                if fitness == 1:
                    print("Solution found at generation %d!" % generation)
                    return (generation, self.population.chromosomes[c])

                if fitness > best_fitness:
                    best_fitness = fitness

            print("Generation:", generation, " Best fitness:", best_fitness)

            # Create the next population.
            next_population = []

            # Select elites (the fittest candidates) and preserve them for the next generation.
            self.population.sort()
            elites = []
            for i in range(num_elites):
                elite = Chromosome()
                elite.values = np.copy(self.population.chromosomes[i].values)
                elites.append(elite)

            # Create the rest of chromosomes
            for count in range(num_elites, population_size, 2):
                # Select parents from population via a tournament.
                t = Tournament()
                parent1 = t.compete(self.population.chromosomes)
                parent2 = t.compete(self.population.chromosomes)

                # Crossover
                cr = CycleCrossover()
                child1, child2 = cr.crossover(parent1, parent2, crossover_rate=1.0)

                # Mutate child1
                child1.update_fitness()
                old_fitness = child1.fitness
                success = child1.mutate(mutation_rate, self.given_grid)
                child1.update_fitness()
                if success:
                    num_mutations += 1
                    if child1.fitness > old_fitness: # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Mutate child2.
                child2.update_fitness()
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate, self.given_grid)
                child2.update_fitness()
                if success:
                    num_mutations += 1
                    if child2.fitness > old_fitness:  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1


                next_population.append(child1)
                next_population.append(child2)

            # Append elites onto the end of the population. These will not have been affected by crossover or mutation.
            for e in range(0, num_elites):
                next_population.append(elites[e])

            # Select next generation.
            self.population.chromosomes = next_population
            self.population.update_fitness()

            # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule).
            # This is to stop too much mutation as the fitness progresses towards unity.
            if num_mutations == 0:
                phi = 0  # Avoid divide by zero.
            else:
                phi = phi / num_mutations

            if phi > 0.2:
                sigma = sigma / 0.998
            elif phi < 0.2:
                sigma = sigma * 0.998

            mutation_rate = abs(np.random.normal(loc=0.0, scale=sigma, size=None))

            # Check for stale population.
            self.population.sort()
            if self.population.chromosomes[0].fitness != self.population.chromosomes[1].fitness:
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 100 generations have passed
            # with the fittest two candidates always having the same fitness.
            if (stale >= 100):
                print("The population has gone stale. Re-seeding...")
                self.population.generate_chromosomes(population_size, self.given_grid)
                stale = 0
                sigma = 1
                phi = 0
                mutation_rate = 0.06

        print("No solution found.")
        return (-2, 1)

