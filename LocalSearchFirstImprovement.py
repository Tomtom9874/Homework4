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


def local_search_best_improvement():
    # variable to record the number of solutions evaluated
    solutions_checked = 0
    x_curr = initial_solution()  # x_curr will hold the current solution
    print("Init:", x_curr)
    x_best = x_curr[:]  # x_best will hold the best solution
    f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current solution
    f_best = f_curr[:]
    print("Init Evaluation:", f_curr)

    # begin local search overall logic ----------------
    done = 0
    while done == 0:
        neighborhood = get_larger_neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr
        for index, neighbor in enumerate(neighborhood):  # evaluate every member in the neighborhood of x_curr
            solutions_checked += 1
            if evaluate(neighbor)[0] > f_best[0]:
                x_best = neighbor[:]  # find the best member and keep track of that solution
                f_best = evaluate(neighbor)[:]  # and store its evaluation

        if f_best == f_curr:  # if there were no improving solutions in the neighborhood
            done = 1
        else:
            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]  # evaluate the current solution
            print("\nTotal number of solutions checked: ", solutions_checked)
            print("Best value found so far: ", f_best)

    print("\nFinal number of solutions checked: ", solutions_checked)
    print("Best value found: ", f_best[0])
    print("Weight is: ", f_best[1])
    print("Total number of items selected: ", np.sum(x_best))
    print("Best solution: ", x_best)
    return x_best, f_best


def local_search_first_improvement():
    # variable to record the number of solutions evaluated
    solutions_checked = 0
    x_curr = initial_solution()  # x_curr will hold the current solution
    print("Init:", x_curr)
    x_best = x_curr[:]  # x_best will hold the best solution
    f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current solution
    f_best = f_curr[:]
    print("Init Evaluation:", f_curr)

    # begin local search overall logic ----------------
    done = 0
    while done == 0:
        neighborhood = get_neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr
        for index, neighbor in enumerate(neighborhood):  # evaluate every member in the neighborhood of x_curr
            solutions_checked += 1
            if evaluate(neighbor)[0] > f_best[0]:
                x_best = neighbor[:]  # find the best member and keep track of that solution
                f_best = evaluate(neighbor)[:]  # and store its evaluation
                break   # Stop when solution is found.

        if f_best == f_curr:  # if there were no improving solutions in the neighborhood
            done = 1
        else:
            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]  # evaluate the current solution
            print("\nTotal number of solutions checked: ", solutions_checked)
            print("Best value found so far: ", f_best)


    print("\nFinal number of solutions checked: ", solutions_checked)
    print("Best value found: ", f_best[0])
    print("Weight is: ", f_best[1])
    print("Total number of items selected: ", np.sum(x_best))
    print("Best solution: ", x_best)
    return x_best, f_best


def main():
    local_search_first_improvement()


if __name__ == '__main__':
    main()
