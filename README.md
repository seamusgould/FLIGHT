# FLIGHT

## ✈️ Description

FLIGHT is a crossword puzzle solver that is loosely based on the record breaking algorithm Dr. Fill.  To learn more about
Dr. Fill, visit [The algorithm that won against human competitors](https://arxiv.org/abs/1401.4597).  This is a test.


# Implementation

To learn more about the implementation, look at the attached read this [presentation](https://github.com/seamusgould/FLIGHT/blob/master/CMPU366_Final_Presentation.pdf)
or read the [paper](https://github.com/seamusgould/FLIGHT/blob/master/CMPU366CrossWords.pdf).

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

 - In order to run the program, you must have the data/crossword in xd format.
 - In order to get crosswords online, xl-word has an excellent library to accomplish this: [xword-dl](https://github.com/thisisparker/xword-dl).
To learn more about xd formats, visit the following repository [Crossword Format](https://github.com/century-arcade/xd)
which allows users to convert .puz files into .xd files.
 - In order to run the program, you must first add a fasttext model to the data/fasttext folder.  To learn more about fasttext, visit [FastText](https://fasttext.cc/).
To download our pretrained fasttext model, visit the following link: [Download](https://drive.google.com/file/d/1AZeDvWbBzC6mvLbcC-Kz9_y2jjULsv-A/view?usp=sharing)

Here is one example of the program running:

    $ python3 CheckFoundPuzzle -m ../<model location> -xd ../<board_location> -a .1

# Example

This is an example of the program running the United States Today crossword puzzle from january first, 2017.

The puzzle will be solved with the correct accuracy being printed out 
![grab-landing-page](https://github.com/seamusgould/FLIGHT/blob/master/example.gif?raw=true)

