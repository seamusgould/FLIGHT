from CheckFoundPuzzle import puzzle_complete
import argparse
import os
import random
from tqdm import tqdm
from Readftmodel import Model

def main(model_path, fp):
    file_path = open('solver_10.txt', 'w')
    file_path.write("file, alpha, accuracy, time\n")
    model = Model(model_path)
    for subdir, dirs, files in os.walk(fp):
        for file in tqdm(files):
            i = .1
            file = os.path.join(subdir, file)
            accuracy, puz_time = puzzle_complete(model, file, i)
            if accuracy:
                file_path.write(f"{file}, {i}, {accuracy}, {puz_time}\n")
            else:
                break
            if i <= 0:
                break
        file_path.close()

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Tune the parameters.')
    my_parser.add_argument('-m','--model', help='The path to the fasttext model.', required=True)
    my_parser.add_argument('-xd', '--xd_path', help='Path to save the clues file', required=True)
    args = my_parser.parse_args()
    main(model_path=args.model, fp=args.xd_path)
