
"""A module of functions for scanning a string, that is,
   splitting the string into its constituent words (tokens)
"""

###### data structures:

nextword = ""  # the word or operator in process of assembly
answer = []    # the answer list of operators and words

# functions that maintain the two data structures:
def init() :
    """init  resets the data structures"""
    global nextword, answer
    nextword = ""
    answer = []

def emitword() :
    """emitword  moves the current assembled word to  answer"""
    global nextword
    if nextword != "" :
        answer.append(nextword)
        nextword = ""

def addletter(letter):
    """addletter  appends  letter  to the end of  nextword"""
    global nextword
    nextword = nextword + letter


####### the scan function:

def scan(text) :
    """scan splits apart the symbols in  text  into a list.

       pre:  text  is a string holding words and
             one- and two-symbol operators
       post: answer  is a list of the words and operators
             within  text; spaces and newlines are removed
       returns  answer
    """
    OPERATOR_SYMBOLS = ("(", ")", "+", "-", ";", ":", "=", "!", "[", "]", ".", ",")
    TWO_SYM_OPS = ("==", "!=")
    SPACES = (" ", "\n", "\r", "\t")   # space, newline, return, tab
    init()
    for letter in text:
        # invariant:  answer + nextword + letter  equals
        #   all the words/symbols read so far
        #   from  text  with  SPACES  removed
        if letter in SPACES :
            emitword()

        elif letter in OPERATOR_SYMBOLS :
            if nextword + letter in TWO_SYM_OPS :
                addletter(letter)
                emitword()
            else :
                emitword()
                addletter(letter)

        else :  # a letter that is part of a word/number :
            if nextword in OPERATOR_SYMBOLS :
                emitword()
            addletter(letter)

    # loop finished; all words assembled.
    emitword()   # in case there is a last word

    return answer

