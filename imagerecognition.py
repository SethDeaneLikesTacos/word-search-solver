import numpy as np
from PIL import Image


def determineletter(filePath):
    """
    Determines the letter of the image passed into the function.
    :param filePath: The filepath of a picture to check the letter of.
    :return: char of the letter that was found
    """
    ref_file = open("letArRef.txt","r").read()
    ref_lst = ref_file.split("\n")
    # ref_lst is now a list of strings containing the rgb values of each letter.

    i = Image.open(filePath)
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
