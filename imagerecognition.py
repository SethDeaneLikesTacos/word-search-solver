import numpy as np
from PIL import Image

grid_start_row = 58
grid_start_col = 18
grid_end_row = 455
grid_end_col = 547

def parseimage(puzzle_file):
    """
    Determines the letter of the image passed into the function.
    :param letter_file: The filepath of a picture to check the letter of.
    :return: char of the letter that was found
    """

    # for the time being, pick one letter to read into a list
    letter_png_list = ["Resources/testletters/a.png",
                       "Resources/testletters/b.png",
                       "Resources/testletters/c.png",
                       "Resources/testletters/d.png",
                       "Resources/testletters/e.png",
                       "Resources/testletters/f.png",
                       "Resources/testletters/g.png",
                       "Resources/testletters/h.png",
                       "Resources/testletters/i.png",
                       "Resources/testletters/j.png",
                       "Resources/testletters/k.png",
                       "Resources/testletters/l.png",
                       "Resources/testletters/m.png",
                       "Resources/testletters/n.png",
                       "Resources/testletters/o.png",
                       "Resources/testletters/p.png",
                       "Resources/testletters/q.png",
                       "Resources/testletters/r.png",
                       "Resources/testletters/s.png",
                       "Resources/testletters/t.png",
                       "Resources/testletters/u.png",
                       "Resources/testletters/v.png",
                       "Resources/testletters/w.png",
                       "Resources/testletters/x.png",
                       "Resources/testletters/y.png",
                       "Resources/testletters/z.png"]

    # read image into array
    puzzle = readimage(puzzle_file)

    # loop through every letter in the alphabet
    # for i in range(4,5):
    for i in range(12,13):
    #for i in range(26):
        print("Searching for: " + letter_png_list[i][-5])

        letter = readimage(letter_png_list[i])

        # Determine value for the dimensions of the letter to look for
        letter_rows = len(letter)            # number of rows in letter png
        letter_cols = len(letter[0])         # number of cols in letter png

        # the list of starting rows where the top of the letters are found
        row_nums = [67, 100, 133, 167, 201, 234, 267, 301, 335, 368, 401, 435, 469, 502]

        # starting pixels
        for row_puz in row_nums:
            for col_puz in range(grid_start_col, grid_end_col):

                # grab a cross section of the puzzle to compare to our letter
                puzbox = puzzle[row_puz : row_puz+letter_rows , col_puz : col_puz+letter_cols]

                # mse
                factor = ((letter ^ puzbox) ** 2).mean(axis=None)

                # If the percentage of the matched pixels is above a threshold, we can say the letter was found
                if factor < .06:
                    grid_col, grid_row = togrid(row_puz, col_puz)
                    print("Found: " + letter_png_list[i][-5] + \
                          " @ " + str(grid_col) + " " + str(grid_row)+ \
                          " with " + str(factor) + " precision")
    return


def readimage(image_file):
    """
    read puzzle into a list and convert to black and which image
    :param image_file: the image file that will be converted
    :return: array of booleans, True if white pixel, False if black pixel
    """
    img = Image.open(image_file)
    i1 = img.convert('L')
    i2 = i1.point(lambda x: 0 if x < 254 else 255, '1')
    puzzle = np.array(i2)
    return puzzle


def togrid(row, col):
    grid_col = (col - grid_start_col + 10) // 32
    grid_row = (row - grid_start_row) // 34
    return grid_col, grid_row

