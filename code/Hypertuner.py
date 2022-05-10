from CheckFoundPuzzle import puzzle_complete
import argparse
import os
import random
from tqdm import tqdm, trange
import pandas as pd
from readftmodel import Model
import numpy as np
import copy
import pdb
import time

def main(model_path, fp):
    file_path = open('solver_10.txt', 'w')
    file_path.write("file, alpha, accuracy, time\n")
    prev_alpha = 0
    alpha = 1
    beta = 0
    prev_accuracy = .5
    model = Model(model_path)
    for subdir, dirs, files in os.walk(fp):
        for file in tqdm(files):
            i = .1
            file = os.path.join(subdir, file)
            accuracy, puz_time = puzzle_complete(model, file, i, beta)
            if accuracy:
                file_path.write(f"{file}, {i}, {accuracy}, {puz_time}\n")
            else:
                break
            if i <= 0:
                break
        file_path.close()
            # cur_alpha = grad_descent(alpha, prev_alpha, accuracy, prev_accuracy)
            # prev_alpha = copy.copy(alpha)
            # alpha = copy.copy(cur_alpha)
            # prev_accuracy = accuracy

def grad_descent(var, prev_var, accuracy, prev_accuracy):
    """
    Updates the value of var based on the stochastic gradient descent algorithm.
    :param alpha:
    :param prev_alpha:
    :param accuracy:
    :param prev_accuracy:
    :return:
    """
    if accuracy != 1.0:
        return random.uniform(var - .0001, var)
    else:
        return random.uniform(var, var + (.0001 * 1/5))
    # if accuracy > prev_accuracy:
    #     new_var = max(random.uniform(var, min(var + .001 * (prev_var - var)*(accuracy - prev_accuracy), 1)), 0)
    # elif accuracy < prev_accuracy:
    #     new_var = min(random.uniform(max(var + .001 * (prev_var - var)*(accuracy - prev_accuracy), 0), var), 1)
    if (prev_var - var)*(accuracy - prev_accuracy) == 0:
        new_var = var + random.uniform(-.1, .1)
    return new_var

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Tune the parameters.')
    my_parser.add_argument('-m','--model', help='The path to the fasttext model.', required=True)
    my_parser.add_argument('-xd', '--xd_path', help='Path to save the clues file', required=True)
    args = my_parser.parse_args()
    main(model_path=args.model, fp=args.xd_path)
