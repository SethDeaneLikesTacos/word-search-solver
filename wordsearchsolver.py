import imagerecognition as imgrec
# taco

width,height = 5,5
matrix = [['t', 'o', 'a', 's', 't'],
          ['a', 'f', 'f', 'f', 'f'],
          ['c', 'f', 'p', 'f', 'm'],
          ['o', 'f', 'f', 'u', 'f'],
          ['f', 'f', 'g', 'f', 'g']]
listOfWords = ["toast", "taco", "ocat", "mug", "pug", "gup", "gum"]


def printmatrix():
    """
    Prints the matrix to the terminal for testing purposes.
    :return:
    """
    for row in range(height):
        print(matrix[row])


def findword():
    """
    Loops through each in the word search to see if it matches the first letter of
    the word being searched for. If first letter in the matrix matches the first
    letter being searched for, then findneighbors() is called.
    :return: None
    """
    for word in range(len(listOfWords)):
        w = listOfWords[word]
        print("We are looking for the word: " + w)
        
        for row in range(height):
            for let in range(width):
                
                if w[0] == matrix[row][let]:
                    print("Found matching first letter: " + matrix[row][let])

                    findneighbors(w, let, row)


def findneighbors(w, let, row):
    """
    Search every direction around the matched letter. If the next letter in the matrix
    matches the next letter in the word to find, then continue to search for the rest
    of the word in that direction.
    :param w: Current word being searched for.
    :param let: Column of the matched letter.
    :param row: Row of the matched letter.
    :return: None
    """
    n = 1  # character we are checking

    # North
    if row-n > 0 and matrix[row-n][let] == w[n]:
        for q in range(len(w)):
            if row-n > 0 and matrix[row-q][let] == w[q]:
                print(str(q) + ": " + matrix[row-q][let] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # North East
    elif row-n > 0 and let+n < width and matrix[row-n][let+n] == w[n]:
        for q in range(len(w)):
            if row-q > 0 and let+q < width and matrix[row-q][let+q] == w[q]:
                print(str(q) + ": " + matrix[row-q][let+q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # East
    elif let+n < width and matrix[row][let+n] == w[n]:
        for q in range(len(w)):
            if let+q < width and matrix[row][let+q] == w[q]:
                print(str(q) + ": " + matrix[row][let+q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # South East
    elif row+n < height and let+n < width and matrix[row+n][let+n] == w[n]:
        for q in range(len(w)):
            if row+n < height and let+q < width and matrix[row+q][let+q] == w[q]:
                print(str(q) + ": " + matrix[row+q][let+q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # South
    elif row+n < height and matrix[row+n][let] == w[n]:
        for q in range(len(w)):
            if row+q < height and matrix[row+q][let] == w[q]:
                print(str(q) + ": " + matrix[row+q][let] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # South West
    elif row+n < height and let-n > 0 and matrix[row+n][let-n] == w[n]:
        for q in range(len(w)):
            if row+q < height and let-q > 0 and matrix[row+q][let-q] == w[q]:
                print(str(q) + ": " + matrix[row+q][let-q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # West
    elif let-n > 0 and matrix[row][let-n] == w[n]:
        for q in range(len(w)):
            if let-q > 0 and matrix[row][let-q] == w[q]:
                print(str(q) + ": " + matrix[row][let-q] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    # North West
    elif row-n > 0 and let-n > 0 and matrix[row-n][let-n] == w[n]:
        for q in range(len(w)):
            if row-q > 0 and let-q > 0 and matrix[row-q][let-q] == w[q]:
                print(str(q) + ": " + matrix[row-q][let] + "|" + w[q])
                if q == len(w)-1:
                    print("FOUND: " + w)

    else:
        print("No matching neighbors were found!")


def main():
    """
    Main function of the word search solver program.
    :return:
    """
    printmatrix()
    findword()
    #createReferencesLetters()
    #imgrec.whatLetAmI("images/letters/b.png")


main()
