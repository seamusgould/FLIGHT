# FLIGHT

A lightweight implementation of Dr. Fill (**Fill light**). 

## ✈️ Description

FLIGHT is a crossword puzzle solver that is loosely based on the record breaking algorithm Dr. Fill.  To learn more about
Dr. Fill, you can read the [original paper here](https://arxiv.org/abs/1401.4597).


# Implementation

To learn more about the implementation, look at the attached read this [presentation](https://github.com/seamusgould/FLIGHT/blob/master/CMPU366_Final_Presentation.pdf)
or read the [paper](https://github.com/seamusgould/FLIGHT/blob/master/CMPU366CrossWords.pdf).

The statistics on crossword solvers can be found in the document titled Crosswords.html.

# Setup

## Requirements
In order to run the program, you must have the following installed:
- time
- tqdm
- numpy
- argparse
- copy
- fastText

## Run the program

 - The data is in data/crossword in xd format.
 - One excellent source to gretrieve puzzles is from this library:[xword-dl](https://github.com/thisisparker/xword-dl).
To learn more about xd formats, visit the following repository [Crossword Format](https://github.com/century-arcade/xd)
which allows users to convert .puz files into .xd files.
 - In order to run the program, you must first add a fasttext model to the data/fasttext folder.  To learn more about fasttext, visit [FastText](https://fasttext.cc/).
Alternitavely, you can download our pretrained fasttext model, visit the following link: [Download](https://drive.google.com/file/d/1AZeDvWbBzC6mvLbcC-Kz9_y2jjULsv-A/view?usp=sharing)

Here is one example of the program running:

    $ python3 CheckFoundPuzzle -m ../<model location> -xd ../<board_location> -a .1

# Example

This is an example of the program running the United States Today crossword puzzle from January 1, 2017.

The puzzle will be solved with the correct accuracy being printed out 
![grab-landing-page](https://github.com/seamusgould/FLIGHT/blob/master/example.gif?raw=true)

