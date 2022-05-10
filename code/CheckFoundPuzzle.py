import time
from copy import deepcopy
import numpy as np
import argparse
from tqdm import tqdm
from ParseClues import parse_them
from Readftmodel import Model

def main(model_path, fp, alpha):
    """
    Main function to run the program.
    :param model: Path to the fasttext model.
    :param clues: Path to the file containing the clues.
    :param board:  Path to the file containing the board.
    :param alpha:  The alpha value for the predictions.  High alpha values will give low accuracy but take longer.
    :return: None
    """
    start = time.time()
    down, across, board, location_dict, answer = parse_them(fp)

    model = Model(model_path)

    precedence = model.get_precedence(across, down)

    board = complete_the_puzzle(model, [(1, board)], location_dict, alpha, precedence)
    end = time.time()
    num_dots = np.count_nonzero(board == ".")
    number_of_equal_elements = np.sum(board == answer)
    total_elements = np.multiply(board.shape[0], board.shape[1])
    percentage = number_of_equal_elements / total_elements
    print(f"Correct: {percentage}")
    print(f"Time: {end - start}")

def complete_the_puzzle(model, branches, location_dict, alpha, precedence):
    """
    Solves the board iteratively whilst dropping the threshold. Then fills in blanks. Combines other methods
    :param show: Whether it will print at every step. Default is False.
    :return:
    """
    if '.' not in branches[0][1] or not precedence:
        ret = branches[0][1]
        return ret
    print(f"Branches: {len(branches)}")
    print(branches[0][1])
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
    lim = leafs[0][0]
    leafs = [leaf for leaf in leafs if leaf[0] >= alpha * lim]
    precedence.pop(0)
    return complete_the_puzzle(model, leafs, location_dict, alpha, precedence)

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
    pct, words = model.clue_to_list_of_words(clue, regex)
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
    args = my_parser.parse_args()
    main(model_path=args.model, fp=args.xd_path, alpha= args.alpha)

