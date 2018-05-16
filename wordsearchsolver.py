import numpy as np
from PIL import Image, ImageDraw
import pytesseract
import re

# path to tesseract (necessary for tesseract)
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

# dimensions of the puzzle to be solved
width, height = 14, 14

RGB_VAL = "RGB"

# boundaries of the letter grid
grid_start_row = 89
grid_start_col = 30
grid_end_row = 666
grid_end_col = 610


def image_to_array(path):

    # read image into array
    img = Image.open(path)
    puzzle = np.array(img)

    # grab a cross section of the puzzle to identify and convert to image
    puzbox = puzzle[grid_start_row : grid_end_row , grid_start_col : grid_end_col]
    puzbox_img = Image.fromarray(puzbox, RGB_VAL)
    puzbox_img.save("temp_puzzle.png")

    # identify the letter of the cross section
    text = pytesseract.image_to_string(puzbox_img, config="--psm 6", lang='eng')

    # generate list
    text = text.split("\n")

    # remove any random newline elements
    for i in text:
        if len(i) < 1:
            text.remove(i)

    # remove any non alphanumeric characters
    for i in range(len(text)):
        text[i] = text[i].replace('0', 'O')
        text[i] = text[i].replace('5', 'S')
        text[i] = re.sub('\W', '', text[i])
        text[i] = text[i].upper()

    # convert to a nice numpy array
    matrix = np.empty([14, 14], dtype = str)
    for i in range(width):
        for j in range(height):
            matrix[i][j] = text[i][j]
    print(matrix)
    return matrix


def search_words(path):
    """
    creates a list of the words that will be found in the puzzle.
    :param path: path of the puzzle to be solved
    :return:
    """
    # dimensions
    fw_x1, fw_y1 = 620, 80
    fw_x2, fw_y2 = 803, 669

    # read image into array
    img = Image.open(path)
    puzzle = np.array(img)

    # grab a cross section of the puzzle to identify and convert to image
    wordbox = puzzle[ fw_y1: fw_y2, fw_x1: fw_x2]
    wordbox_img = Image.fromarray(wordbox, RGB_VAL)
    wordbox_img.save("temp_words.png")

    # translate picture to text
    text = pytesseract.image_to_string(wordbox_img, config="--psm 1", lang='eng')

    # generate list
    text = text.split("\n")

    # remove any random newline elements
    for i in text:
        if len(i) < 1:
            text.remove(i)

    for i in range(len(text)):
        text[i] = re.sub('\W', '', text[i])
        text[i] = text[i].replace('0', 'O')
        text[i] = text[i].replace('5', 'S')
        text[i] = text[i].upper()

    return text


def print_matrix(matrix):
    """
    Prints the matrix to the terminal for testing purposes.
    :return: None
    """
    for p in matrix:
        for l in p:
            print(str(l) + ' ', end='')
        print()


def findword(matrix, words_to_find, path):
    """
    Loops through each in the word search to see if it matches the first letter of
    the word being searched for. If first letter in the matrix matches the first
    letter being searched for, then findneighbors() is called.
    :return: None
    """
    im = Image.open(path)
    draw = ImageDraw.Draw(im)

    for word in range(len(words_to_find)):
        word = words_to_find[word]
        print("We are looking for the word: " + word)
        found = 0

        for y in range(height):
            for x in range(width):

                ww = ''.join([''.join(row) for row in matrix[y:y+1, x:x + len(word)]])[::-1]
                if ww == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1
                    x2 = x1 + len(word) - 1

                ee = ''.join([''.join(row) for row in matrix[y:y+1, x:x + len(word)]])
                if ee == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1
                    x2 = x1 + len(word) - 1

                nn = ''.join([''.join(row) for row in matrix[y:y + len(word), x:x+1]])[::-1]
                if nn == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1 + len(word) - 1
                    x2 = x1

                ss = ''.join([''.join(row) for row in matrix[y:y + len(word), x:x+1]])
                if ss == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1 + len(word) - 1
                    x2 = x1

                sw = ''.join(np.diagonal(np.rot90(matrix[y:y + len(word), x - len(word):x])))
                if sw == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1 + len(word) - 1
                    x2 = x1 - len(word)
                    x1 -= 1

                ne = ''.join(np.diagonal(np.rot90(matrix[y:y + len(word), x - len(word):x])))[::-1]
                if ne == word:
                    found = 1
                    y1 = y
                    x1 = x - 1
                    y2 = y1 + len(word) - 1
                    x2 = x1 - len(word) + 1

                se = ''.join(np.diagonal(matrix[y:y + len(word), x:x + len(word)]))
                if se == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1 + len(word) - 1
                    x2 = x1 + len(word) - 1

                nw = ''.join(np.diagonal(matrix[y:y + len(word), x:x + len(word)]))[::-1]
                if nw == word:
                    found = 1
                    y1 = y
                    x1 = x
                    y2 = y1 - len(word) - 1
                    x2 = x1 - len(word) - 1

        if found:
            print("FOUND: [" + word + "] (" + str(x1) + "," + str(y1) + ") | (" + str(x2) + ", " + str(y2) + ")")
            draw_line(draw, x1, x2, y1, y2)

        if found == 0:
            print("!! WORD NOT FOUND !!")

    im.save("out.png")
    return


def draw_line(draw, x1, x2, y1, y2):
    # list of starting rows and columns for each letter
    row_nums = [89, 131, 172, 214, 255, 295, 337, 379, 419, 460, 503, 543, 584, 626]
    col_nums = [30, 71, 113, 155, 196, 237, 279, 321, 361, 403, 445, 487, 528, 570]

    # draw lines highlighting the words found
    draw.line(
        (col_nums[x1] + 20, row_nums[y1] + 20,
         col_nums[x2] + 20, row_nums[y2] + 20)
        , fill=(255, 0, 0, 255), width=2)
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
                # print(str(q) + ": " + matrix[row-q][let] + "|" + w[q])
                if q == len(w)-1:
                    x = x
                    y -= q
                    found = 1
                    return x, y, found

    # North East
    elif row-n > 0 and let+n < width and matrix[row-n][let+n] == w[n]:
        for q in range(len(w)):
            if row-q > 0 and let+q < width and matrix[row-q][let+q] == w[q]:
                # print(str(q) + ": " + matrix[row-q][let+q] + "|" + w[q])
                if q == len(w)-1:
                    x += q
                    y -= q
                    found = 1
                    return x, y, found

    # East
    elif let+n < width and matrix[row][let+n] == w[n]:
        for q in range(len(w)):
            if let+q < width and matrix[row][let+q] == w[q]:
                # print(str(q) + ": " + matrix[row][let+q] + "|" + w[q])
                if q == len(w)-1:
                    x += q
                    y = y
                    found = 1
                    return x, y, found
    # South East
    elif row+n < height and let+n < width and matrix[row+n][let+n] == w[n]:
        for q in range(len(w)):
            if row+q < height and let+q < width and matrix[row+q][let+q] == w[q]:
                # print(str(q) + ": " + matrix[row+q][let+q] + "|" + w[q])
                if q == len(w)-1:
                    x += q
                    y += q
                    found = 1
                    return x, y, found

    # South
    elif row+n < height and matrix[row+n][let] == w[n]:
        for q in range(len(w)):
            if row+q < height and matrix[row+q][let] == w[q]:
                # print(str(q) + ": " + matrix[row+q][let] + "|" + w[q])
                if q == len(w)-1:
                    x = x
                    y += q
                    found = 1
                    return x, y, found

    # South West
    elif row+n < height and let-n > 0 and matrix[row+n][let-n] == w[n]:
        for q in range(len(w)):
            if row+q < height and let-q > 0 and matrix[row+q][let-q] == w[q]:
                # print(str(q) + ": " + matrix[row+q][let-q] + "|" + w[q])
                if q == len(w)-1:
                    x -= q
                    y += q
                    found = 1
                    return x, y, found

    # West
    elif let-n > 0 and matrix[row][let-n] == w[n]:
        for q in range(len(w)):
            if let-q > 0 and matrix[row][let-q] == w[q]:
                # print(str(q) + ": " + matrix[row][let-q] + "|" + w[q])
                if q == len(w)-1:
                    x -= q
                    y = y
                    found = 1
                    return x, y, found

    # North West
    elif row-n > 0 and let-n > 0 and matrix[row-n][let-n] == w[n]:
        for q in range(len(w)):
            if row-q > 0 and let-q > 0 and matrix[row-q][let-q] == w[q]:
                # print(str(q) + ": " + matrix[row-q][let] + "|" + w[q])
                if q == len(w)-1:
                    x -= q
                    y -= q
                    found = 1
                    return x, y, found

    # print("No matching neighbors were found!")
    return 0, 0, found




def main():
    """
    Main function of the word search solver program.
    :return:
    """
    # path to the puzzle
    puz_path = "wordsearches\\ws4.png"


    array = image_to_array(puz_path)
    words_to_find = search_words(puz_path)
    for i in words_to_find:
        print(i)
    print_matrix(array)
    findword(array, words_to_find, puz_path)


main()
