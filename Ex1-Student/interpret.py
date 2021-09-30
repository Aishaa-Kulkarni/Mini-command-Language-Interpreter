
"""Interpreter for a mini-language with variables,loops and if-commands, declarations, and procedure.

   Operator trees that are interpreted are defined as

PTREE ::= BTREE
BTREE ::=  [ DLIST, CLIST ]
DLIST ::=  [ DTREE* ]
           where  DTREE*  means zero or more DTREEs
DTREE ::=  ["int", VAR]  |  ["proc", VAR, BTREE]
CLIST ::=  [ CTREE+ ]
           where  CTREE+  means one or more CTREEs
CTREE ::=  ["=", VAR, ETREE]  |  ["print", ETREE]  |  ["while", ETREE, CLIST]
        |  ["if", ETREE, CLIST, CLIST]  |  ["call", VAR]
ETREE ::=  NUMERAL  |  VAR  |  [OP, ETREE, ETREE]
           where  OP  is either "+" or "-"         
           
           
There is one crucial data structure:

  ns is a namespace --- it holds the program's variables
  and their values.  It's a dictionary now for the mini-language in Lecture Note 1.

  With adding procedure call, you can change ns to be a list of Python hash table (dictionary). 
  For example, 
     ns = [{'x': 2,
           'p': [['int', y], ['=' 'y', ['+', 'x', '1']], ['print', 'y']]
           },
           {'y': 0}] 
  holds global namespace for vars  x, p, and another procedure namespace of p for  y,  where int x has value 2, and y initially value 0;
  proc p has the command list for int y; y=x+1; print y  as its value,
  and int y has value 0.
"""
ns = {}

def interpretPTREE(p):
    """pre: p  is a program represented as a  PTREE ::=  BTREE
       post:  ns  holds all the global updates commanded by program  p
    """
    global ns #  ns  is a global variable that we will modify
    ns = {}   #  reset  ns  to empty
    interpretBTREE(p)
    for i in ns.keys():
        if type(ns[i])==list:
            if len(ns[i][0])==0:
                ns[i]=ns[i][1]
    print("final namespace. =", ns)

def interpretBTREE(b):
    """pre: b  is a program represented as a  BTREE ::=  [ DLIST, CLIST ]
       post:  ns  holds all the global updates commanded by block  b
    """
    global ns   #  ns  is a global variable that we will modify
    # Modify ns so that global and local variable will be stored properly
    # WRITE YOUR CODE HERE
    

    # YOUR CODE END HERE
    #print('here is the btree[0] item',b[0])
    #print('here is the btree[1] item',b[1])
    if(len(b[0])!=0):
        interpretDLIST(b[0])   # interpret the declariations, initial int variabal to 0, and store proc contents
    interpretCLIST(b[1])   # extract the commands and execute them
    



def interpretDLIST(dlist):
    """pre: dlist is a list of declaration trees: DLIST ::=  [ DTREE* ]
       post: ns holds all the updates of declarations
    """
    # WRITE YOUR CODE HERE
    # similar to CLIST, for each DTREE, call interpretDTREE,

    
    for argument in dlist:
        #print('each argument which goes to interpretDTREE',argument)
        if len(argument)!=0:
            interpretDTREE(argument)


    # YOUR CODE END HERE

def interpretDTREE(dtree):
    """pre: dtree is a variable or proc declaration represented as a DTREE:
         DTREE ::=["int", VAR] | ["proc", VAR, BTREE]
       post: ns  holds the updates declared by dtree
    """
    ## WRITE YOUR CODE HERE
    # type, var = dtree[:2] 
    ## find the local or global namespace to store variable value, 
    ## for example, "x": 0 for ["int", "x"]
    # 
    # if type == 'int': #["int", VAR]
    # 
    #  
    #   
    ## for ["proc", "p", [....]] procedure declaration, store dtree[2] (a list) as value of p
    ## for example 'p': dtree[2]
    # elif type == 'proc': # ["proc", VAR, BTREE]
    global ns
    
    var=dtree[1]
    if dtree[0]=='int':
        if var not in ns:
            ns[var]=0
    elif dtree[0]=='proc':
        if var not in ns:
            ns[var]=dtree[2]
            
    #print('first assigning values in ns',ns)
        
            

    # YOUR CODE END HERE

def interpretCLIST(clist):
    """pre: clist  is a list of command trees:  CLIST ::=  [ CTREE+ ]
       post:  ns  holds all the updates commanded by   clist
    """
    
    for command in clist :
        interpretCTREE(command)


def interpretCTREE(c) :
    """pre: c  is a command represented as a CTREE:
         CTREE ::=  ["=", VAR, ETREE]  |  ["print", VAR] |  ["while", ETREE, CLIST]
                    |  ["if", ETREE, CLIST, CLIST]  |  ["call", VAR]
       post:  ns  holds the updates commanded by  c
    """
    # 1. Make sure global namespace and local namespace is specified
    # WRITE YOUR CODE HERE
    global ns
    operator = c[0]
    if operator == "=" :   # assignment command, ["=", VAR, ETREE]
        # 2. MODIFY THE FOLLOWING THREE LINES OF CODES TO CONSIDER VAR SCOPE CHECKING
        # YOUR CODE START HERE
        
        var = c[1]   # get left-hand side
        exprval = interpretETREE(c[2])  # evaluate the right-hand side
        ns[var] = exprval  # do the assignment
        #print('here comes the equal to keyword, now the name space becomes',ns)        


        # YOUR CODE END HERE

    elif operator == "print" :   # print command,  ["print", VAR]
        exp = c[1]   
        print("Print:", interpretETREE(exp) )
        

    elif operator == "while" :   # while command,  ["while", ETREE, CLIST]
        expr = c[1]
        body = c[2]
        if interpretETREE(expr)!= 0:
            interpretCLIST(body) 
            interpretCTREE(c)  # repeat
        else :     # exit loop
            pass   # do nothing
    elif operator == "if" :   # ["if", ETREE, CLIST, CLIST] 
        # WRITE YOUR CODE HERE
        expr=c[1]
        body1=c[2]
        body2=c[3]
        if interpretETREE(expr)!=0:
            interpretCLIST(body1)
        else:
            interpretCLIST(body2)

        # YOUR CODE END HERE

    elif operator == "call":   # call command, ["call",VAR]
        # WRITE YOUR CODE HERE
        #if the operator is call we need to traverse back
        var=c[1]
        #print(var)
        if var in ns:
            interpretBTREE(ns[var])
            
            #print('responsible for infinite loop',ns[var])
            #print('bksa')
        


        # YOUR CODE END HERE
    
    else :   # error:
        crash("invalid command")


def interpretETREE(e) :
    """pre: e  is an expression represented as an ETREE:
           ETREE ::=  NUMERAL  |  VAR  |  [OP, ETREE, ETREE]
                      where OP is either "+" or "-"
      post:  ans  holds the numerical value of  e
      returns:   ans
    """
    # 1. Make sure global namespace and local namespace is specified
    # WRITE YOUR CODE HERE


    if isinstance(e, str) and  e.isdigit() :   # a numeral
        ans = int(e)
    elif isinstance(e, str) and len(e) > 0  and  e[0].isalpha() :  # var name
        # 2. MODIFY THE FOLLOWING FOUR LINES OF CODE TO CONSIDER GLOBAL AND LOCAL NAMESPACE
        # YOUR CODE START HERE
        if e in ns:   # is var name  e  assigned a value in the namespace ?
            ans = ns[e]  # look up its value
        else :
            crash("variable name not a declared int")

        # YOUR CODE END HERE
    else :   #  [op, e1, e2]
        op = e[0]
        ans1 = interpretETREE(e[1])
        ans2 = interpretETREE(e[2])
        if op == "+" : 
            ans = ans1 + ans2
        elif op == "-" : 
            ans = ans1 - ans2
        else :
            crash("illegal arithmetic operator")
    return ans


def crash(message) :
    """pre: message is a string
       post: message is printed and interpreter stopped
    """
    print(message + "! crash! core dump:", ns)
    raise Exception   # stops the interpreter





