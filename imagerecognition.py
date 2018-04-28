import numpy as np
from PIL import Image as PILImage

grid_start_row = 58
grid_start_col = 18
grid_end_row = 455
grid_end_col = 547

def determineletter(puzzle_file):
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

    # read puzzle into a list
    i = PILImage.open(puzzle_file)
    puzzle = np.array(i)
    puzzle = threshold(puzzle)

    # loop through every letter in the alphabet
    for i in range(12,13):
    #for i in range(26):
        print("Searching for: " + letter_png_list[i][-5])

        # Read letter into a list
        letimg = PILImage.open(letter_png_list[i])
        letter = np.array(letimg)
        letter = threshold(letter)

        # Determine value for the dimensions of the letter to look for
        letter_rows = len(letter)            # number of rows in letter png
        letter_cols = len(letter[0])         # number of cols in letter png
        num_pix = letter_rows * letter_cols

        # starting pixels
        for row_puz in range(grid_start_row, grid_end_row):
            for col_puz in range(grid_start_col, grid_end_col):

                # grab a cross section of the puzzle to compare to our letter
                puzbox = puzzle[row_puz : row_puz+letter_rows , col_puz : col_puz+letter_cols]

                count = 0
                for r in range(letter_rows):
                    for c in range(letter_cols):
                        if puzbox[r][c] == letter[r][c]:
                            count += 1


                # If the percentage of the matched pixels is above a threshold, we can say the letter was found
                if count / num_pix > .95:
                    grid_col, grid_row = togrid(row_puz, col_puz)
                    print("Found: " + letter_png_list[i][-5] + \
                          " @ " + str(grid_row) + " " + str(grid_col) + \
                          " with " + str(count / num_pix) + " precision")
    return


def threshold(array):
    """

    :param array: the array
    :return:
    """
    rr = len(array)  # number of rows in letter png
    cc = len(array[0])  # number of cols in letter png

    new_array = np.empty([rr, cc])

    for r in range(rr):
        for c in range(cc):

            # if the pixel is pure white
            if array[r][c][0] == 255:
                new_array[r][c] = 0

            # if the pixel has any pigmentation whatsoever
            else:
                new_array[r][c] = 1

            #print(str(c) + " " + str(r) + " " + str(new_array[r][c]) + " " + str(array[r][c][0]))

    return new_array

def togrid(row, col):
    grid_col = (col - grid_start_col) % 32
    grid_row = (row - grid_start_row) % 34
    return grid_col, grid_row

