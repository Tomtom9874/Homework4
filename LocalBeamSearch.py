# basic hill climbing search provided as base code for the DSA/ISE 5113 course
# author: Charles Nicholson

#  NOTE: YOU MAY CHANGE ALMOST ANYTHING YOU LIKE IN THIS CODE.
#  However, I would like all students to have the same problem instance,
#  therefore please do not change anything relating to:
#   random number generation
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

# ------------------------------------------------------------------------------

# Student name: Thomas Welborn
# Date: 4/3/2020


# need some python libraries
import copy
from random import Random  # need this for the random number generation -- do not change
import numpy as np

# to setup a random number generator, we will specify a "seed" value
# need this for the random number generation -- do not change
seed = 5113
my_pseudo = Random(seed)

# to get a random number between 0 and 1, use this:             myPRNG.random()
# to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
# to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

# number of elements in a solution
num_elements = 150

# create an "instance" for the knapsack problem
value = []
for _ in range(0, num_elements):
    value.append(round(my_pseudo.triangular(5, 1000, 200), 1))

weights = []
for _ in range(0, num_elements):
    weights.append(round(my_pseudo.triangular(10, 200, 60), 1))

# define max weight for the knapsack
max_weight = 1500


# change anything you like below this line ------------------------------------


# function to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)
    total_value = np.dot(a, b)  # compute the value of the knapsack selection
    total_weight = np.dot(a, c)  # compute the weight value of the knapsack selection
    if total_weight > max_weight:
        return [-1, -1]  # Returns solution that will never replace best
    return [total_value, total_weight]  # returns a list of both total value and total weight


# here is a simple function to create a neighborhood
# 1-flip neighborhood of solution x
def get_neighborhood(x):
    neighbors = []
    for i in range(0, num_elements):
        neighbors.append(x[:])
        if neighbors[i][i] == 1:
            neighbors[i][i] = 0
        else:
            neighbors[i][i] = 1
    return neighbors


def get_larger_neighborhood(x):
    neighbors = []
    for i in range(0, num_elements):
        for j in range(0, num_elements):
            position = i * num_elements + j
            neighbors.append(x[:])
            if neighbors[position][i] == 1:
                neighbors[position][i] = 0
            else:
                neighbors[position][i] = 1
            if neighbors[position][j] == 1:
                neighbors[position][j] = 0
            else:
                neighbors[j][j] = 1
    return neighbors


# create the initial solution
def initial_solution(odds=0.2):
    valid = False
    x = []  # i recommend creating the solution as a list
    while not valid:
        x = []
        for i in range(num_elements):
            random_number = my_pseudo.random()
            if odds > random_number:
                x.append(1)
            else:
                x.append(0)
        val, _ = evaluate(x)
        if val > 0:
            valid = True
    return x


def local_search_best_improvement(x_curr, f_curr):
    neighborhood = get_neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr
    solutions_checked = 0
    new_improvements = []
    for neighbor in neighborhood:  # evaluate every member in the neighborhood of x_curr
        solutions_checked += 1
        if evaluate(neighbor)[0] > f_curr[0]:
            new_improvements.append(neighbor)
    return new_improvements, solutions_checked


def initialize_beam():
    x_curr = initial_solution()  # x_curr will hold the current solution
    f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current solution
    return x_curr, f_curr


def main():
    # Variable Initialization
    solutions_checked = 0
    parallel_beams = 10  # This changes how meany beams to use
    f_curr = []
    x_curr = []  # Holds solution for each beam
    x_best = None
    f_best = [-1, -1]

    # Initial Solutions
    for i in range(parallel_beams):
        x, f = initialize_beam()
        x_curr.append(x)
        f_curr.append(f)
        if f_curr[i][0] > f_best[0]:
            f_best = f_curr[i]
            x_best = x_curr[i]
        print(f_best, x_best)

    # Beam Search
    while True:
        new_improvements = []
        # Collect Improvements
        for i in range(parallel_beams):
            improvements, checked = local_search_best_improvement(x_curr[i], f_curr[i])
            solutions_checked += checked
            new_improvements.extend(improvements)

        # Get the top improvements
        top_improvements = []
        for improvement in new_improvements:
            top_improvements.append(improvement)
            if len(top_improvements) > parallel_beams:
                top_improvements.sort(key=lambda var: evaluate(var)[0])
                top_improvements.pop(0)

        # Case when no new improvements found
        if not top_improvements:
            break

        # Handles the common case when there is a improved solution for each neighbor
        elif len(top_improvements) == parallel_beams:
            for i, solution in enumerate(top_improvements):
                x_curr[i] = solution
                f_curr[i] = evaluate(solution)

        # This is for the end when the number of solutions < number of beams.
        else:
            length = len(top_improvements)
            for beam in range(length):
                x_curr[beam] = top_improvements[beam]
                f_curr[beam] = evaluate(top_improvements[beam])
            # For any excess beams, assign the first improvement.
            for beam in range(length, parallel_beams):
                x_curr[beam] = top_improvements[length - 1]
                f_curr[beam] = evaluate(top_improvements[length - 1])

        x_best = top_improvements[len(top_improvements) - 1]
        f_best = evaluate(top_improvements[len(top_improvements) - 1])
        print("\nSolutions checked so far: ", solutions_checked)

    # End Results
    print("\nTotal number of solutions checked: ", solutions_checked)
    print("Best Overall Value:", f_best[0])
    print("Weighs:", f_best[1])
    print("Total Items selected:", sum(x_best))
    print("Best Overall Solution:", x_best)


if __name__ == '__main__':
    main()
