import numpy as np
from PIL import Image as PILImage
from wand.image import Image as wandImage
from wand.image import Color as wandColor


def convert_pdf(filename, output_path):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    with wandImage(filename=filename, resolution=1000000) as img:
        with wandImage(width=img.width, height=img.height, background=wandColor("white")) as bg:
            bg.composite(img, 0, 0)
            bg.save(filename=output_path)


def searchpuzzle(puzzle_path):
    """

    :param puzzle_path: The raw pdf file take from the word search site.
    :return:
    """
    outpath = "Resources/wordsearches/wordsearch1.pdf"
    convert_pdf(puzzle_path, outpath)



def determineletter(letter_file):
    """
    Determines the letter of the image passed into the function.
    :param letter_file: The filepath of a picture to check the letter of.
    :return: char of the letter that was found
    """
    ref_file = open("letArRef.txt","r").read()
    ref_lst = ref_file.split("\n")
    # ref_lst is now a list of strings containing the rgb values of each letter.

    i = PILImage.open(letter_file)
    letter = str(np.array(i).tolist())
    # letter is now a string containing the rgb values of the letter to check.

    # For each word in the reference word list
    for ref in ref_lst:

        # Split reference list to get letter and rgb values
        split_ref = ref.split("::")
        ref_name = split_ref[0]
        ref_data = split_ref[1]

        # find the maximum number of iterations that we can check
        if len(letter) >= len(ref_data):
            max_it = len(ref_data)
        else:
            max_it = len(letter)

        # Iterate through each character in the letter and the reference letter
        count = 0
        for x in range(0, max_it):
            if letter[x] == ref_data[x]:
                count += 1

        if (count == len(letter)):
            print(ref_name)
            return ref_name


# TODO: Adds a line to the end of the file which throws things off unless removed
# TODO: Appends to the end of the file every time. Should rewrite the file.
def createreferencefile():
    """
    Create file containing bitmaps of reference images.
    """
    letterArrayReferences = open("letArRef.txt", "a")
    lettersWeHave = range(0,26)
    letAr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z']

    # create reference file for each number in "numbers"
    for let in lettersWeHave:
        imgFilePath = "Resources/letters/" + letAr[let] + ".png"
        refImage = Image.open(imgFilePath)
        refImageAr = np.array(refImage)
        refImageAr1 = str(refImageAr.tolist())

        lineToWrite = letAr[let] + "::" + refImageAr1 + "\n"
        letterArrayReferences.write(lineToWrite)
