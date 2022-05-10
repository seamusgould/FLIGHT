# FLITE

## Description

FLITE is a crossword puzzle solver that is loosely based on the record breaking algorithm Dr. Fill.  To learn more about
Dr. Fill, visit [The algorithm that won against human competitors](https://arxiv.org/abs/1401.4597).  This is a test.


# Implementation

- Line 79 contains all of the needed code to run the program.
- This is how it works:
- 1. The method takes in all the arguments from the command line.
- 2. If the puzzle is done, it will print out the solution and quit the program.
- 3. If the puzzle is not done, it will print out the current state of the puzzle along
with the threshold, number of branches, and delta values.
- 4. For each branch, it will add a word and parse the branches that are unlikely to be
the solution. 
- 5. Iterate across thresholds and adds to branches new possibilities.

# Problems

1. Ideally, each branch should write a different word to a different clue, but as of right
now, it writes different words to different clues.  There should be a way to control this, no?
2. The program is slow.  Too many branches.  There should be a way to control this, no?
3. There is a lot of repetition in the code.  When this occurs, we can make a new method.
4. It would be nice to have a way display the numpy array as a gui, though this is not essential.
