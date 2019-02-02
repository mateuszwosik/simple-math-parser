import sys
import re

#For each class token:
#   Generating binary tree for expression
#   varible lbp - (left binding power) controls operator precedence;
#       the higher the value, the tihgter a token binds to  the token that follow
#   function nud - (for null denotation) used when a token appears at the beginning of language constructor
#       returns value of token
#   function led - (left denotation) used when a token appears inside the construct (to the left of the rest of the construct)
#       calls expressionParser with token binding power (this causes the expressionParser to treat everything with a higher power as subexpression) and returns result value of expressionParser
#       returns result of applied function (operator)
#   commented returning value

class number_token:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        #self.value = int(value)
    def nud(self):
        return self
        #return self.value
    def __repr__(self):
        return "Node(%s)" % self.value

class variable_token:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
    def nud(self):
        return self
    def __repr__(self):
        return "Node(%s)" % self.value

class operator_add_token:
    lbp = 10 #operator binding power
    def __init__(self):
        self.value = "+"
        self.left = None
        self.right = None
    def nud(self):
        self.left = expressionParser(100)
        self.right = None
        return self
        #return expressionParser(100)
    def led(self,left):
        self.left = left
        self.right = expressionParser(10)
        return self
        #right = expressionParser(10)
        #return left + right
    def __repr__(self):
        return "Node(\"%s\", %s, %s)" % (self.value, self.left, self.right)

class operator_sub_token:
    lbp = 10 #operator binding power
    def __init__(self):
        self.value = "-"
        self.left = None
        self.right = None
    def nud(self):
        self.left = expressionParser(100)
        self.right = None
        return self
        #return -expressionParser(100)
    def led(self,left):
        self.left = left
        self.right = expressionParser(10)
        return self
        #right = expressionParser(10)
        #return left - right
    def __repr__(self):
        return "Node(\"%s\", %s, %s)" % (self.value, self.left, self.right)

class operator_mul_token:
    lbp = 20 #operator binding power
    def __init__(self):
        self.value = "*"
        self.left = None
        self.right = None
    def led(self,left):
        self.left = left
        self.right = expressionParser(20)
        return self
        #right = expressionParser(20)
        #return left * right
    def __repr__(self):
        return "Node(\"%s\", %s, %s)" % (self.value, self.left, self.right)

class operator_div_token:
    lbp = 20 #operator binding power
    def __init__(self):
        self.value = "/"
        self.left = None
        self.right = None
    def led(self,left):
        self.left = left
        self.right = expressionParser(20)
        return self
        #right = expressionParser(20)
        #return left / right
    def __repr__(self):
        return "Node(\"%s\", %s, %s)" % (self.value, self.left, self.right)

class operator_pow_token:
    lbp = 30 #operator binding power
    def __init__(self):
        self.value = "^"
        self.left = None
        self.right = None
    def led(self,left):
        self.left = left
        self.right = expressionParser(30-1)
        return self
    def __repr__(self):
        return "Node(\"%s\", %s, %s)" % (self.value, self.left, self.right)

#NOT WORKING CORRECTLY
class operator_lpar_token:
    lbp = 2 #operator binding power
    def __init__(self):
        self.value = "("
        self.left = None
        self.right = None
    def nud(self):
        self.left = expressionParser(2)
        self.right = None
        return self
    def led(self,left):
        self.left = left
        self.right = expressionParser(2)
        return self
    def __repr__(self):
        return "Node(\"%s\", %s , %s)" % (self.value, self.left, self.right)

class operator_rpar_token:
    lbp = 2 #operator binding power
    def __init__(self):
        self.value = ")"
        self.left = None
        self.right = None
    def led(self,left):
        return left

#Special token ending parsing
#lowest binding power to ensure that the expressionParser stops when reaches the end of expression)
class end_token:
    lbp = 0 #operator binding power

#Functions executing instructions
#Pop two numbers from stack and perform operations on them and append result to the stack

def operator_add(stack):
    if len(stack) == 1: #sign of number
        a = stack.pop()
        if isinstance(a,str):
            stack.append(str(a))
        else:
            stack.append(0 + a)
    else:
        b = stack.pop()
        a = stack.pop()
        if isinstance(a,str) or isinstance(b,str):
            stack.append(''.join([str(a),'+',str(b)]))
        else:
            stack.append(a + b)

def operator_sub(stack):
    if len(stack) == 1: #sign of number
        a = stack.pop()
        if isinstance(a,str):
            stack.append(''.join(['-',str(a)]))
        else:
            stack.append(0-a)
    else:
        b = stack.pop()
        a = stack.pop()
        if isinstance(a,str) or isinstance(b,str):
            stack.append(''.join([str(a),'-',str(b)]))
        else:
            stack.append(a - b)

def operator_mul(stack):
    b = stack.pop()
    a = stack.pop()
    if isinstance(a,str) or isinstance(b,str):
        stack.append(''.join([str(a),'*',str(b)]))
    else:
        stack.append(a * b)

def operator_div(stack):
    b = stack.pop()
    a = stack.pop()
    if isinstance(a,str) or isinstance(b,str):
        stack.append(''.join([str(a),'/',str(b)]))
    else:
        stack.append(a / b)

def operator_pow(stack):
    b = stack.pop()
    a = stack.pop()
    if isinstance(a,str) or isinstance(b,str):
        stack.append(''.join([str(a),'^',str(b)]))
    else:
        stack.append(a ** b)

def put_number(stack,value):
    stack.append(value)

def put_variable(stack,variable):
    stack.append(variable)
    
#Operator available in runtime environment
operators = {
    '+': operator_add,
    '-': operator_sub,
    '*': operator_mul,
    '/': operator_div,
    '^': operator_pow,
    }

#Reading binary tree in postfix order and returning orders for runtime environment
def codeGenerator(node):
    s = ""
    if node == None:
        return s
    if node.left != None:
        s += codeGenerator(node.left)
        #s = ''.join([s,str(codeGenerator(node.left))])
    if node.right != None:
        s += codeGenerator(node.right)
        #s = ''.join([s,str(codeGenerator(node.right))])
    return ' '.join([s,str(node.value)])

#Execute orders using stack
#Returning table of performed actions
#Cell in last row and last column is the result of expression
def execute(expression):
    stack = [] #stack
    table = ["TOKEN,ACTION,STACK".split(',')] #table with performed actions
    for token, variable in re.findall("\s*(?:(\d+|[\+|\-|\*|\/|\^])|(\w+))",expression):
        if token in operators:
            action = "Apply operator to top of stack"
            operators[token](stack) #performing operation
            table.append( (token, action, ' '.join(str(s) for s in stack)) ) #adding operation to table (token - operator, action name, stack)
        elif token:
            action = "Push number onto top of stack"
            put_number(stack,int(token)) #put number onto top of stack
            table.append( (token, action, ' '.join(str(s) for s in stack)) ) #adding operation to table (token - number, action name, stack)
        elif variable:
            action = "Push variable onto top of stack"
            put_variable(stack,variable) #put variable onto top of stack
            table.append( (variable, action, ' '.join(str(s) for s in stack)) ) #adding operation to table (token - variable, action name, stack)
    return table

#tokenize - Python generator (PARSER)
#generate right kind of token objects for given expression (end token at the end)
#getting tokens from regular expression (SKANER)
#   \s* - zero or more occurences of whitespace
#   (?:(\d+)|(.)) - groups regular expressions (one or more occurances of digit or any character) without remembering matched text
#   findall() - returns list of groups (tuples)
#number - list of number tokens
#operator - list of operator tokens
def tokenize(expression):
    for number, variable, operator in re.findall("\s*(?:(\d+)|(\w+)|(.))\s*",expression):
        if number:
            yield number_token(number)
        elif variable:
            yield variable_token(variable)
        elif operator == "+":
            yield operator_add_token()
        elif operator == "-":
            yield operator_sub_token()
        elif operator == "*":
            yield operator_mul_token()
        elif operator == "/":
            yield operator_div_token()
        elif operator == "^":
            yield operator_pow_token()
        elif operator == "(":
            yield operator_lpar_token()
        elif operator == ")":
            yield operator_rpar_token()
        else:
            raise SyntaxError("unknown operator") #rise error when unknown operator
    yield end_token() #add ending token

#expressionParser
#   rbp - right binding power (given binding power)
#expression parser from Pratt's algorithm
def expressionParser(rbp = 0):
    global token, root #global variable containing current token, global token containing root element of binary tree
    t = token #rembember current token (integer token)
    if root == None: #for '-' and '+' indicating the sing of number
        root = token
    token = next() #get next token (operator token)
    left = t.nud() #get token value (integer token)
    while rbp < token.lbp: #check if the binding power of the next token is at least as large as the given binding power
        t = token #remember current token (operator token)
        token = next() #get next token (integer token)
        left = t.led(left) #pass left result to token (operator) led function and return result to left
        root = t #remember root element of the binary tree
    if root == None: #if none operators in expression
        root = left
    return left #return result of expression

#Main function parsing expression
def parse(expression):
    global token, next, root #current token, helper that fetches the next token, root element of binary tree
    next = tokenize(expression).next #get generator
    token = next() #get next token
    root = None #set root element to None
    print "Expression: %s" % expression #print given expression
    print "Parser tree: %s" % expressionParser() #calculate and print binary tree
    print "Code generator: %s" % codeGenerator(root) #calculate orders for runtime environment and print them
    result = execute(codeGenerator(root)) #perform runtime orders
    #Printing runtime environment actions
    row = result[0] #get first row from result table (headers)
    maxcolwidths = [max(len(y) for y in x) for x in zip(*result)] #calculate maximum columns widths
    print( ' '.join('{cell:^{width}}'.format(width=width, cell=cell) for (width, cell) in zip(maxcolwidths, row))) #print first row (headers) on center (takes into account the width of a column)
    for row in result[1:]: #for rest of the result table
        print( ' '.join('{cell:<{width}}'.format(width=width, cell=cell) for (width, cell) in zip(maxcolwidths, row))) #print the result (takes into account the width of a column)
    #
    print "The result value is: %r \n" % result[-1][2] #print final result

#parse("1 /2- 3*4+ 12+   100") #100
#parse("2^3+1") #9
#parse("+1-2+4") #3
#parse("1") #1
#parse("--1") #1
#parse("7+1+2+a") #10+a
#parse("7+3+b-10*5 /   25") #10+b-2
#parse("1*5+5-5+Zmienna1 -4/2") #5+Zmienna1-2
#parse("2*(5+5)-1*4") #16
parse("1+2    ")
