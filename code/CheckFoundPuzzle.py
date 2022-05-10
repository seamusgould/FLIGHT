# https://www.boatloadpuzzles.com/playcrossword
# https://towardsdatascience.com/how-to-create-your-own-question-answering-system-easily-with-python-2ef8abc8eb5
# https://www.kaggle.com/darinhawley/new-york-times-crossword-clues-answers-19932021
# https://programming.vip/docs/61b844e73677c.html
import ast
import re
import time
from copy import deepcopy
import numpy as np
from Predictions import Predictions
import fasttext
from readftmodel import Model
import argparse
import pdb
from tqdm import tqdm
from ParseClues import parse_them

def puzzle_complete(model, fp, alpha, beta):
    """
    Main function to run the program.
    :param model: Path to the fasttext model.
    :param clues: Path to the file containing the clues.
    :param board:  Path to the file containing the board.
    :param alpha:  The alpha value for the predictions.  High alpha values will give low accuracy but take longer.
    :param beta: The rate of branching.  A high beta value will give a more accurate prediction but will take longer.
    :return: None
    """
    start = time.time()
    down, across, board, location_dict, answer = parse_them(fp)
    # model = Model('C:/Users/rrros/OneDrive/Documents/COMPSCI/CMPU366/Crosswords-BERT/ftmodel.bin')
    # --DELETED ABOVE WHEN DEPOLYING--

    # model = Model(model_path)

    precedence = model.get_precedence(across, down)

    board = complete_the_puzzle(model, [(1, board)], location_dict, alpha, precedence, beta)
    end = time.time()
    # print(board)
    # print(answer)
    if board[0] is None:
        print("No solution found")
        return None, None
    num_dots = np.count_nonzero(board == ".")
    number_of_equal_elements = np.sum(board == answer)
    total_elements = np.multiply(board.shape[0], board.shape[1])
    percentage = number_of_equal_elements / total_elements
    percentage_no_dots = number_of_equal_elements / (total_elements - num_dots)
    # print(f"Correct: {percentage}")
    # print(f"Correct letters: {percentage_no_dots}")
    # print(f"Time: {end - start}")
    return percentage, end - start
    # print(f"Time required for solving: {end - start}s")

# def parse_files(clues, board, loc_dict={}):
#     """
#     Parses the files and returns the clues and board.
#     :param clues: Path to the file containing the clues.
#     :param board: Path to the file containing the board.
#     :return down_dict: Dictionary of down clues.
#     :return across_dict: Dictionary of across clues.
#     :return location_dict: Dictionary of locations of the numbers.
#     :return board: The board as a numpy array.
#     """
#     # with open(r'C:\Users\rrros\OneDrive\Documents\COMPSCI\CMPU366\Crosswords-BERT\Boards\4-11-2022\4_11_board.txt', 'r') as the_file:
#     # --DELETED ABOVE WHEN DEPOLYING--
#     with open(board, 'r') as the_file:
#         board = the_file.read()
#
#     # with open(r'C:\Users\rrros\OneDrive\Documents\COMPSCI\CMPU366\Crosswords-BERT\Boards\4-11-2022\4_11_clues.txt', 'r') as the_file:
#     ## DELETED ABOVE WHEN DEPOLYING--
#     with open(clues, 'r') as the_file:
#         d_clues = {}
#         a_clues = {}
#         down = False
#         while True:
#             line1 = the_file.readline().replace('\n', '').replace('\r', '')
#             if not line1:  # EOF
#                 break
#             if line1 == 'ACROSS':
#                 continue
#             elif line1 == 'DOWN':
#                 down = True
#                 continue
#             if down:
#                 line2 = the_file.readline().replace('\n', '').replace('\r', '')
#                 d_clues[line1] = line2
#             else:
#                 line2 = the_file.readline().replace('\n', '').replace('\r', '')
#                 a_clues[line1] = line2
#     board = np.array(ast.literal_eval(board)[:-1])
#     location_dict, board = get_board(board, loc_dict)
#     return d_clues, a_clues, board, location_dict, answer_board

def complete_the_puzzle(model, branches, location_dict, alpha, precedence, beta):
    """
    Solves the board iteratively whilst dropping the threshold. Then fills in blanks. Combines other methods
    :param show: Whether it will print at every step. Default is False.
    :return:
    """
    if '.' not in branches[0][1] or not precedence:
        ret = branches[0][1]
        return ret
    # print("alpha: ", alpha)
    # print(f"Branches: {len(branches)}")
    # print(branches[0][1])
    leafs = []
    # Define a function that gets highest probability of a word returns dir and key of clue.
    # dir, word = get_max_prob(model, across, down,location_dict, board, threshold)
    item = precedence[0]
    begin = time.time()
    for board in tqdm(branches):
        temp_board = deepcopy(board)
        pct_board = add_word(item, model, temp_board, location_dict, alpha, item[3])
        leafs += pct_board
    leafs = sorted(leafs, key=lambda x: x[0], reverse=True)
    if len(leafs) == 0:
        leafs = branches
    else:
        lim = leafs[0][0]
        if alpha + beta >= 1:
            alpha = .99
        else:
            alpha = alpha + beta
        leafs = [leaf for leaf in leafs if leaf[0] >= alpha * lim]
    precedence.pop(0)
    return complete_the_puzzle(model, leafs, location_dict, alpha, precedence, beta)

def add_word(item, model, board, location_dict, max_score, beta):
    """
    Solves the rest of the board after threshold has been lowered iteratively. Fills in first likely
    guess using regex.
    :return:
    """
    sims = []

    dir = item[0]
    index = item[1]
    clue = item[2]

    partial = get_partial(index, dir, board[1], location_dict)
    regex = "^" + partial + "$"
    pct, words = model.clue_to_list_of_words(clue, regex, max_score, beta)
    for pct, word in zip(pct, words):
        temp_board = deepcopy(board[1])
        temp_board = write_word(word, index, dir, temp_board, location_dict)
        sims.append((pct * board[0], temp_board))
    return sims

def get_board(board, location_dict = {}):
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] != '*':
                location_dict[board[i][j]] = (i, j)
                board[i][j] = '.'
    return location_dict, board

def get_partial(num, direction, board, loc_dict):
        if direction == 'down':
            i, j = loc_dict[num]
            partial = ''
            while i < np.shape(board)[0]:
                if board[i][j] != '*':
                    partial += board[i][j]
                    i += 1
                else:
                    break
        else:
            i, j = loc_dict[num]
            partial = ''
            while j < np.shape(board)[1]:
                if board[i][j] != '*':
                    partial += board[i][j]
                    j += 1
                else:
                    break
        return partial

def write_word(word, num, direction, board, loc_dict):
    if direction == 'down':
        i, j = loc_dict[num]
        for char in word:
            board[i][j] = char
            i += 1
    else:
        i, j = loc_dict[num]
        for char in word:
            board[i][j] = char
            j += 1
    return board

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Scrape the data from the website.')
    my_parser.add_argument('-m','--model', help='The path to the fasttext model.', required=True)
    my_parser.add_argument('-xd', '--xd_path', help='Path to save the clues file', required=True)
    my_parser.add_argument('-a', '--alpha', type=float, help='Threshold to solve the clues.', required=True)
    my_parser.add_argument('-be', '--beta', type=float, help='Threshold to solve the clues.', required=True)
    args = my_parser.parse_args()
    main(model_path=args.model, fp=args.xd_path, alpha= args.alpha, beta= args.beta)

