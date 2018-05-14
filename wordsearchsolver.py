import numpy as np
from PIL import Image, ImageDraw
import pytesseract
import re

# path to tesseract (necessary for tesseract)
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

# path to the puzzle
puz_path = "Resources\\wordsearches\\ws2.png"

# dimensions of the puzzle to be solved
width, height = 14, 14

# list of starting rows and columns for each letter
row_nums = [89, 131, 172, 214, 255, 295, 337, 379, 419, 460, 503, 543, 584, 626]
col_nums = [30, 71, 113, 155, 196, 237, 279, 321, 361, 403, 445, 487, 528, 570]

# boundaries of the letter grid
grid_start_row = 89
grid_start_col = 30
grid_end_row = 666
grid_end_col = 610

# Determine value for the dimensions of the letter to look for
letter_rows = 40  # number of rows in letter png
letter_cols = 40  # number of cols in letter png


def image_to_array(path):


    # create array
    puzzlear = [[0 for x in range(width)] for y in range(height)]

    # read image into array
    img = Image.open(path)
    puzzle = np.array(img)

    # starting pixels
    for row_puz in row_nums:
        for col_puz in col_nums:

            # get column and row numbers for indexing locations
            col = col_nums.index(col_puz)
            row = row_nums.index(row_puz)

            # grab a cross section of the puzzle to identify and convert to image
            puzbox = puzzle[row_puz : row_puz+letter_rows , col_puz : col_puz+letter_cols]
            puzbox_img = Image.fromarray(puzbox, "RGBA")
            puzbox_img.save("temp.png")

            # identify the letter of the cross section
            text = pytesseract.image_to_string(puzbox_img, config="--psm 10", lang='eng')

            # friendly print statement
            # print("Found: " + text + " @ " + str(col) + " " + str(row))

            # correct 0 to O
            if text[0] == "0":
                insert = text[0].replace('0', 'O')
            else:
                insert = text[0].upper()

            puzzlear[row][col] = insert

    return puzzlear


def print_matrix(matrix):
    """
    Prints the matrix to the terminal for testing purposes.
    :return: None
    """
    for p in matrix:
        for l in p:
            print(str(l) + ' ', end='')
        print()


def findword(matrix, words_to_find):
    """
    Loops through each in the word search to see if it matches the first letter of
    the word being searched for. If first letter in the matrix matches the first
    letter being searched for, then findneighbors() is called.
    :return: None
    """
    im = Image.open(puz_path)
    draw = ImageDraw.Draw(im)

    for word in range(len(words_to_find)):
        w = words_to_find[word]
        print("We are looking for the word: " + w)
        
        for y1 in range(height):
            for x1 in range(width):
                
                if w[0] == matrix[y1][x1]:
                    print("Found matching first letter: " + matrix[y1][x1])

                    x2, y2, found = find_neighbors(w, x1, y1, matrix)
                    if found:
                        print("orig: " + str(x1) + ", " + str(y1))
                        print(" new: " + str(x2) + ", " + str(y2))

                        draw.line(
                            (col_nums[x1] + (letter_cols / 2), row_nums[y1] + (letter_rows / 2),
                             col_nums[x2] + (letter_cols / 2), row_nums[y2] + (letter_rows / 2))
                            ,fill=(255,0,0,255), width=2)
    im.save("out.png")
    return


def find_neighbors(w, let, row, matrix):
    """
    Search every direction around the matched letter. If the next letter in the matrix
    matches the next letter in the word to find, then continue to search for the rest
    of the word in that direction.
    :param w: Current word being searched for.
    :param let: Column of the matched letter.
    :param row: Row of the matched letter.
    :return: final x, y pair and whether or not the word was found
    """
    x, y = let, row
    n = 1  # character we are checking
    found = 0

    # North
    if row-n > 0 and matrix[row-n][let] == w[n]:
        for q in range(len(w)):
            if row-n > 0 and matrix[row-q][let] == w[q]:
                print(str(q) + ": " + matrix[row-q][let] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x = x
                    y -= q
                    found = 1
                    return x, y, found

    # North East
    elif row-n > 0 and let+n < width and matrix[row-n][let+n] == w[n]:
        for q in range(len(w)):
            if row-q > 0 and let+q < width and matrix[row-q][let+q] == w[q]:
                print(str(q) + ": " + matrix[row-q][let+q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x += q
                    y -= q
                    found = 1
                    return x, y, found

    # East
    elif let+n < width and matrix[row][let+n] == w[n]:
        for q in range(len(w)):
            if let+q < width and matrix[row][let+q] == w[q]:
                print(str(q) + ": " + matrix[row][let+q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x += q
                    y = y
                    found = 1
                    return x, y, found
    # South East
    elif row+n < height and let+n < width and matrix[row+n][let+n] == w[n]:
        for q in range(len(w)):
            if row+q < height and let+q < width and matrix[row+q][let+q] == w[q]:
                print(str(q) + ": " + matrix[row+q][let+q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x += q
                    y += q
                    found = 1
                    return x, y, found

    # South
    elif row+n < height and matrix[row+n][let] == w[n]:
        for q in range(len(w)):
            if row+q < height and matrix[row+q][let] == w[q]:
                print(str(q) + ": " + matrix[row+q][let] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x = x
                    y += q
                    found = 1
                    return x, y, found

    # South West
    elif row+n < height and let-n > 0 and matrix[row+n][let-n] == w[n]:
        for q in range(len(w)):
            if row+q < height and let-q > 0 and matrix[row+q][let-q] == w[q]:
                print(str(q) + ": " + matrix[row+q][let-q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x -= q
                    y += q
                    found = 1
                    return x, y, found

    # West
    elif let-n > 0 and matrix[row][let-n] == w[n]:
        for q in range(len(w)):
            if let-q > 0 and matrix[row][let-q] == w[q]:
                print(str(q) + ": " + matrix[row][let-q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x -= q
                    y = y
                    found = 1
                    return x, y, found

    # North West
    elif row-n > 0 and let-n > 0 and matrix[row-n][let-n] == w[n]:
        for q in range(len(w)):
            if row-q > 0 and let-q > 0 and matrix[row-q][let-q] == w[q]:
                print(str(q) + ": " + matrix[row-q][let] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)
                    x -= q
                    y -= q
                    found = 1
                    return x, y, found

    print("No matching neighbors were found!")
    return 0, 0, found


fw_x1, fw_y1 = 620, 80
fw_x2, fw_y2 = 803, 669
def search_words(path):

    # read image into array
    img = Image.open(path)
    puzzle = np.array(img)

    # grab a cross section of the puzzle to identify and convert to image
    wordbox = puzzle[ fw_y1: fw_y2, fw_x1: fw_x2]
    wordbox_img = Image.fromarray(wordbox, "RGBA")
    wordbox_img.save("temp.png")

    # translate picture to text
    text = pytesseract.image_to_string(wordbox_img, config="--psm 6", lang='eng')

    # generate list
    text = text.split("\n")

    # remove any random newline elements
    for i in text:
        if len(i) < 1:
            text.remove(i)

    for i in range(len(text)):
        text[i] = re.sub('\W', '', text[i])

    return text




def main():
    """
    Main function of the word search solver program.
    :return:
    """
    array = image_to_array(puz_path)
    words_to_find = search_words(puz_path)
    print_matrix(array)
    findword(array, words_to_find)


main()
