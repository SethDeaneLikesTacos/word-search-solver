import numpy as np
from PIL import Image as PILImage


def determineletter(puzzle_file):
    """
    Determines the letter of the image passed into the function.
    :param letter_file: The filepath of a picture to check the letter of.
    :return: char of the letter that was found
    """
    # for the time being, pick one letter to read into a list
    letter_png_list = ["Resources/letters/a.png",
                       "Resources/letters/b.png",
                       "Resources/letters/c.png",
                       "Resources/letters/d.png",
                       "Resources/letters/e.png",
                       "Resources/letters/f.png",
                       "Resources/letters/g.png",
                       "Resources/letters/h.png",
                       "Resources/letters/i.png",
                       "Resources/letters/j.png",
                       "Resources/letters/k.png",
                       "Resources/letters/l.png",
                       "Resources/letters/m.png",
                       "Resources/letters/n.png",
                       "Resources/letters/o.png",
                       "Resources/letters/p.png",
                       "Resources/letters/q.png",
                       "Resources/letters/r.png",
                       "Resources/letters/s.png",
                       "Resources/letters/t.png",
                       "Resources/letters/u.png",
                       "Resources/letters/v.png",
                       "Resources/letters/w.png",
                       "Resources/letters/x.png",
                       "Resources/letters/y.png",
                       "Resources/letters/z.png"]

    # read puzzle into a list
    i = PILImage.open(puzzle_file)
    puzzle = np.array(i)
    puzzle_rows = len(puzzle)           # number of rows in puzzle png
    puzzle_cols = len(puzzle[0])        # number of cols in puzzle png

    # loop through every letter in the alphabet
    for i in range(26):
        print(i)

        letimg = PILImage.open(letter_png_list[i])
        letter = np.array(letimg)
        letter_rows = len(letter)            # number of rows in letter png
        letter_cols = len(letter[0])         # number of cols in letter png

        # loop through every pixel in the puzzle
        for row_puz in range(puzzle_rows - letter_rows - 1):
            for col_puz in range(puzzle_cols - letter_cols - 1):

                puzbox = puzzle[row_puz : row_puz+letter_rows , col_puz : col_puz+letter_cols]

                if np.array_equal(letter, puzbox):
                # if np.sum(puzbox) == np.sum(letter):
                    print("taco")


    return
