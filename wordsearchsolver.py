import numpy as np
from PIL import Image, ImageDraw
import pytesseract
import re
import pdf2image

# path to tesseract (necessary for tesseract)
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

# color type used by pytesseract
RGB_VAL = "RGB"

# dimensions of the puzzle to be solved
width, height = 14, 14

# boundaries of the letter grid
grid_start_row = 244
grid_start_col = 95
grid_end_row = 1424
grid_end_col = 1211


def image_to_array(puz_image):
    """
    creates a numpy matrix of the puzzle
    :param puz_image: the image object of entire puzzle
    :return: numpy matrix of the word search
    """
    # read image into array
    puzzle = np.array(puz_image)

    # grab a cross section of the puzzle to identify and convert to image
    puzbox = puzzle[grid_start_row : grid_end_row , grid_start_col : grid_end_col]
    puzbox_img = Image.fromarray(puzbox, RGB_VAL)

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
    return matrix


def search_words(puz_image):
    """
    creates a list of the words that will be found in the puzzle.
    :param puz_image: image object of entire puzzle
    :return: list of words to find in the puzzle
    """
    # dimensions where words to search for are
    fw_x1, fw_y1 = 1227, 244
    fw_x2, fw_y2 = 1637, 1424

    # read image into array
    puzzle = np.array(puz_image)

    # grab a cross section of the puzzle to identify and convert to image
    wordbox = puzzle[ fw_y1: fw_y2, fw_x1: fw_x2]
    wordbox_img = Image.fromarray(wordbox, RGB_VAL)

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


def findword(matrix, words_to_find, puz_image):
    """
    locates and highlights the words found in the puzzle
    :param matrix: numpy matrix of the puzzle letters
    :param words_to_find: list of the words to be found in the puzzle
    :param puz_image: image object of entire puzzle
    :return: image object with highlighted words
    """
    draw = ImageDraw.Draw(puz_image)

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

    return puz_image


def draw_line(draw, x1, x2, y1, y2):
    """
    draw lines highlighting the words that were found
    :param draw: the image to draw on
    :param x1: starting x location
    :param x2: ending x location
    :param y1: starting y location
    :param y2: ending y location
    :return:
    """
    draw.line(
        (grid_start_col + x1 * 80 + 40, grid_start_row + y1 * 86 + 20,
         grid_start_col + x2 * 80 + 40, grid_start_row + y2 * 86 + 20)
        , fill=(255, 0, 0, 255), width=2)
    return


def main():
    """
    Main function of the word search solver program.
    :return:
    """
    puz_image = pdf2image.convert_from_path('wordsearches\\ws1.pdf')
    array = image_to_array(puz_image[0])
    words_to_find = search_words(puz_image[0])
    for i in words_to_find:
        print(i)
    print_matrix(array)
    solved_image = findword(array, words_to_find, puz_image[0])
    solved_image.save("out.png")


main()
