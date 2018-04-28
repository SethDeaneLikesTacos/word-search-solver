import numpy as np
from PIL import Image as PILImage


def determineletter(puzzle_file):
    """
    Determines the letter of the image passed into the function.
    :param letter_file: The filepath of a picture to check the letter of.
    :return: char of the letter that was found
    """
    grid_start_row = 58
    grid_start_col = 18
    grid_end_row = 455
    grid_end_col = 547

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

    # loop through every letter in the alphabet
    for i in range(4,5):
    #for i in range(26):
        print(i)
        letimg = PILImage.open(letter_png_list[i])
        letter = np.array(letimg)
        letter_rows = len(letter)            # number of rows in letter png
        letter_cols = len(letter[0])         # number of cols in letter png
        num_pix = letter_rows * letter_cols


        letter = threshold(letter, letter_rows, letter_cols)


        # loop through every pixel in the puzzle
        for row_puz in range(grid_start_row, grid_end_row, 30):
            for col_puz in range(grid_start_col, grid_end_col, 32):

                puzbox = puzzle[row_puz : row_puz+letter_rows , col_puz : col_puz+letter_cols]
                puzbox = threshold(puzbox, letter_rows, letter_cols)

                count = 0
                for r in range(letter_rows):
                    for c in range(letter_cols):
                        if puzbox[r][c] == letter[r][c]:
                            count += 1
                print(count / num_pix)

                #print(puzbox)

                #if ((row_puz * col_puz) % 10132 == 0):
                #    print(np.mean(letter == puzbox))

                #if np.mean(letter == puzbox) > .71:
                #    print("Found: " + letter_png_list[i][-5])
                    

                if count / num_pix > .9:
                    print("Found: " + letter_png_list[i][-5] + " @ " + str(col_puz) + " " + str(row_puz))
                #if np.array_equal(letter, puzbox):
                #    print("Found: " + letter_png_list[i][-5] + " @ " + str(col_puz) + " " + str(row_puz))

    return


def threshold(array, rr, cc):

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

