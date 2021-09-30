
"""A module of functions that reformat an input program into an
   operator tree.   Call  parse()  to run the parser.

PROGRAM ::= BLOCK
BLOCK ::=  DECLIST COMMANDLIST 
DECLIST ::=  DECLARATION ; DECLIST  |  (nothing)
DECLARATION ::=  int VAR  |  proc VAR : BLOCK end
COMMANDLIST ::=  COMMAND  |  COMMAND ; COMMANDLIST
COMMAND ::=  VAR = EXPRESSSION
             |  print EXPRESSION
             |  while EXPRESSION : COMMANDLIST end
             |  if EXPRESSION : COMMANDLIST else COMMANDLIST end
             |  call VAR
EXPRESSION ::= NUMERAL  |  VAR  |  ( EXPRESSION OPERATOR EXPRESSION )
OPERATOR is  +  or  -
NUMERAL  is a sequence of digits from the set, {0,1,2,...,9}
VAR  is a string of lower-case letters, not a keyword


The output operator trees are nested lists:

PTREE ::= BTREE
BTREE ::=  [ DLIST, CLIST ]
DLIST ::=  [ DTREE* ]
           where  DTREE*  means zero or more DTREEs
DTREE ::=  ["int", VAR]  |  ["proc", VAR, BTREE]
CLIST ::=  [ CTREE+ ]
           where  CTREE+  means one or more CTREEs
CTREE ::=  ["=", VAR, ETREE]  |  ["print", ETREE]  |  ["while", ETREE, CLIST]
        |  ["if", ETREE, CTREE, CTREE]  |  ["call", VAR]
ETREE ::=  NUMERAL  |  VAR  |  [OP, ETREE, ETREE]
           where  OP  is either "+" or "-"
"""

### data structures for parser:
wordlist = []  # holds the remaining unread words
nextword = ""  # holds the first unread word
# global invariant:  nextword + wordlist == all remaining unread words
EOF = "!"      # a word that marks the end of the input words

def getNextword() :
    """moves the front word in  wordlist  to  nextword.
       If wordlist is empty, sets  nextword = EOF
    """
    global nextword, wordlist
    if wordlist == [] :
        nextword = EOF
    else :
        nextword = wordlist[0]
        wordlist = wordlist[1:]

#####

def error(message) :
    """prints an error message and halts the parse"""
    global nextword, wordlist
    print("parse error: " + message)
    print(nextword, wordlist)
    raise Exception


def isVar(word) :
    """checks whether  word  is a legal variable name"""
    KEYWORDS = ("declare", "in", "end", "int", "proc", "print", "while", "if", "else", "call")
    ans = ( word.isalpha()  and  not(word in KEYWORDS) )
    return ans


def parseEXPR() :
    """builds an ETREE from the words in  nextword + wordlist,
          where  EXPR ::=  NUMERAL  |  VAR  |  ( EXPR OP EXPR )
                 OP is "+" or "-"
          and    ETREE ::=  NUMERAL  |  VAR  |  [OP, ETREE, ETREE]
      Also, maintains the global invariant (on wordlist and nextword)
    """
    if  nextword.isdigit() :   # a NUMERAL ?
        ans = nextword        
        getNextword()
    elif  isVar(nextword) :    # a VARIABLE ?
        ans = nextword
        getNextword()
    elif nextword == "(" :     # ( EXPR op EXPR ) ?
        getNextword()
        tree1 = parseEXPR()
        op = nextword
        if op == "+"  or  op == "-" :
            getNextword()
            tree2 = parseEXPR()
            if nextword == ")" :
                ans = [op, tree1, tree2]
                getNextword()
            else :
                error("missing )")
        else :
            error("missing operator")
    else :
        error("illegal symbol to start an expression")

    return ans

def parseCOMMAND() :
    """builds a CTREE from the words in  nextword + wordlist,
       where  COMMAND ::=  VAR = EXPRESSSION
                        |  print VAR
                        |  while EXPRESSION : COMMANDLIST end
                        |  if EXPRESSION : COMMANDLIST else COMMANDLIST end
                        |  call VAR
       and  CTREE ::=  ["=", VAR, ETREE]  |  ["print", VAR] 
                    |  ["while", ETREE, CLIST]
                    |  ["if", ETREE, CTREE, CTREE]  |  ["call", VAR]
      Also, maintains the global invariant (on wordlist and nextword)
    """
    if isVar(nextword) :       # VARIABLE = EXPRESSION ?
        v = nextword
        getNextword()
        if nextword == "=" :
            getNextword()
            exprtree = parseEXPR()
            ans = ["=", v, exprtree]
        else :
            error("missing =")
    elif nextword == "print" :      # print VARIABLE ?
        getNextword()
        exprtree = parseEXPR()
        ans = ["print", exprtree]
    elif nextword == "while" :    # while EXPRESSION : COMMANDLIST end ?
        getNextword()
        exprtree = parseEXPR()
        if nextword == ":" :
            getNextword()
        else :
            error("missing :")
        cmdlisttree = parseCMDLIST()
        if nextword == "end" :
            ans = ["while", exprtree, cmdlisttree]
            getNextword()
        else :
            error("missing end")
    elif nextword == "if" :    # if EXPRESSION : COMMANDLIST else COMMANDLIST end
        getNextword()
        exprtree = parseEXPR()
        if nextword == ":" :
            getNextword()
        else :
            error("missing :")
        clist1 = parseCMDLIST()
        if nextword == "else" :
            getNextword()
        else :
            error("missing else")
        clist2 = parseCMDLIST()
        if nextword == "end" :
            ans = ["if", exprtree, clist1, clist2]
            getNextword()
        else :
            error("missing end")
    elif nextword == "call" :
        getNextword()
        if isVar(nextword) :
            ans = ["call", nextword]
            getNextword()
        else :
            error("expected name of called proc")

    else :                       # error -- bad command
        error("bad word to start a command")
    return ans


def parseDECLARATION():
    """builds a DTREE from  nextword + wordlist,
       where  DECLARATION ::=  int VAR  |  proc VAR : COMMANDLIST end
       and    DTREE ::=  ["int", VAR]  |  ["proc", VAR, CLIST]
    """
    if nextword == "int" :   # int VAR
        getNextword()
        if isVar(nextword):
            ans = ["int", nextword]
            getNextword()
        else :
            error("missing name of declared variable")
    elif nextword == "proc" :   # proc I : CMDLIST  end
        getNextword()
        if isVar(nextword):
            pname = nextword
            getNextword()
            if nextword == ":" :
                getNextword()
                body = parseBLOCK()
                if nextword == "end" :
                    getNextword()
                    ans = ["proc", pname, body]
                else :
                    error("missing end")
            else :
                error("missing : in proc decl")
        else :
            error("missing proc name")
    else :
        error("bad word to start a declaration")

    return ans 


def parseDECLIST():
    """builds a DLIST from  nextword + wordlist, 
       where  DECLIST ::=  DECLARATION ; DECLIST  |  (nothing)
       and    DLIST ::=  [ DTREE* ]
              where  DTREE*  means zero or more DTREEs
    """
    ans = []
    while nextword in ("int", "proc") :
        ans.append(parseDECLARATION())
        if nextword == ";" :
            getNextword()
        else : error("missing ;")
    return ans
       

def parseCMDLIST() :
    """builds a CLIST from the words in  nextword + wordlist,
       where  COMMANDLIST ::=  COMMAND  |  COMMAND ; COMMANDLIST
       and    CLIST ::=  [ CTREE+ ]
       Also, maintains the global invariant (on wordlist and nextword)
    """
    ans = [ parseCOMMAND() ]   # parse first command
    while nextword == ";" :    # collect any other COMMANDS
        getNextword()
        ans.append( parseCOMMAND() )
    return ans


def parseBLOCK():
    """builds a BTREE from  nextword + wordlist,
       where  BLOCK ::=  declare DECLIST in COMMANDLIST end
       and    PTREE ::=  [ DLIST, CLIST ]
    """
    decls = parseDECLIST()
    cmds = parseCMDLIST()
    ans = [decls, cmds]
    return ans
    
def parsePROGRAM():
    """builds a PTREE from  nextword + wordlist,
       where  PROGRAM ::= BLOCK
       and    PTREE ::=  BTREE
    """
    return parseBLOCK()


def parse(words) :
    """reads the input program, initializes the  nextword and wordlist,
       and builds an operator tree

       precondition:  words is a list of strings, the words in the program
       postcondition: returns an operator tree for  wordlist
    """
    global wordlist  # we will reset this global variable
    wordlist = words
    getNextword()
    # assert: global invariant for nextword and wordlist holds true here
    tree = parsePROGRAM()
    # assert: tree holds the entire operator tree for  text
    #print "The parsed program is:"
    #print tree
    #print
    if nextword != EOF :
       error("there are extra words")
    return tree
