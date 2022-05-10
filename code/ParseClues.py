import numpy as np
import re
import argparse
from copy import deepcopy

def parse_them(fp):
    across_clues = {}
    down_clues = {}
    fp = open(fp, 'r')
    board = []
    for i in fp:
        if i == "\n":
            continue
        # check if it is all uppercase, or if it has a number that does not contain "., or that it has "#"
        if "." not in i and i.replace("#", "").isupper():
            row = np.array(list(i))
            board.append(row[:-1])
            continue
        if not board:
            continue
        answers = np.vstack(board)
        # replace all the "#" with "*"
        answers[answers == "#"] = "*"
        clear_board = deepcopy(answers)
        # Iterate across array and replace all characters that are not # with .
        clear_board[clear_board != "*"] = "."
        # Check to see if the string has A, number, then .
        pattern = re.compile("^A[0-9]+\..*")
        if pattern.match(i):
            # Split the string into a list
            clue = i.split(". ", 1)
            # Get the number of the clue
            clue_number = clue[0][1:]
            # Get the clue
            clue_text = clue[1].split(" ~")[0]
            # Add the clue to the dictionary
            across_clues[clue_number] = clue_text
            continue
        # Check to see if the string has D, number, then .
        pattern = re.compile("^D[0-9]+\..*")
        if pattern.match(i):
            # Split the string into a list
            clue = i.split(". ", 1)
            # Get the number of the clue
            clue_number = clue[0][1:]
            # Get the clue
            clue_text = clue[1].split(" ~")[0]
            # Add the clue to the dictionary
            down_clues[clue_number] = clue_text
            continue
        fp.close()
    location_dict = get_locations(clear_board)
    return down_clues, across_clues, clear_board, location_dict, answers

def get_locations(clear_board):
    location_dict = {}
    j = 0
    k = 1
    # Iterate across the board
    for i in range(clear_board.shape[0]):
        # Iterate across the row
        for j in range(clear_board.shape[1]):
            # If the character is a number, add it to the dictionary
            if (i == 0 and clear_board[i][j] == '.') or (j == 0 and clear_board[i][j] == '.'):
                location_dict[str(k)] = (i, j)
                k += 1
                continue
            if ((clear_board[i-1][j] == '*' and clear_board[i][j] == ".") or (clear_board[i][j-1] == '*' and clear_board[i][j] == ".")):
                location_dict[str(k)] = (i, j)
                k += 1
                continue
    return location_dict

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Scrape the data from the website.')
    my_parser.add_argument('-xd','--xdfile', help='The path to the xd file.', required=True)
    # Convert namespace to string
    main(my_parser.parse_args().xdfile)
