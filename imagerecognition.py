import numpy as np
from PIL import Image
from collections import Counter


def determineletter(filePath):
    """

    :param filePath: The filepath of a
    :return:
    """
    matchedAr = []  # Keeps track of the
    loadRefs = open("letArRef.txt","r").read()
    loadRefs = loadRefs.split("\n")

    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()

    inQuestion = str(iarl)

    for ref in loadRefs:
        if len(ref) > 3: # to ignore the last line
            splitRef = ref.split("::")
            currentNum = splitRef[0]
            currentAr = splitRef[1]

            eachPixRef = currentAr.split("],")
            eachPixInQ = inQuestion.split("],")

            x = 0
            while x < len(eachPixRef):
                print(str(eachPixRef[x]) + " : " + str(eachPixInQ[x]))
                if eachPixRef[x] == eachPixInQ[x]:
                    matchedAr.append(currentNum)

                x += 1

    print(matchedAr)
    x = Counter(matchedAr)
    print(x)


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
        imgFilePath = "images/letters/" + letAr[let] + ".png"
        refImage = Image.open(imgFilePath)
        refImageAr = np.array(refImage)
        refImageAr1 = str(refImageAr.tolist())

        lineToWrite = letAr[let] + "::" + refImageAr1 + "\n"
        letterArrayReferences.write(lineToWrite)


def threshold(imageAr):
    """
    Turn colored image into black-and-white image.
    :param imageAr:
    :return:
    """
    balanceAr = []
    newAr = imageArle

    for row in imageAr:
        for pix in row:
            avgRGB = reduce(lambda x, y: x + y, pix[:3]) / len(pix[:3])
            balanceAr.append(avgRGB)

    balance = reduce(lambda x, y: x + y, balanceAr) / len(balanceAr)

    for row in newAr:
        for pix in row:
            if reduce(lambda x, y: x + y, pix[:3]) / len(pix[:3]) > balance:
                pix[0] = 255
                pix[1] = 255
                pix[2] = 255
                pix[3] = 255
            else:
                pix[0] = 0
                pix[1] = 0
                pix[2] = 0
                pix[3] = 255

    return newAr