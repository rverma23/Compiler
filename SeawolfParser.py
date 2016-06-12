#!/usr/bin/env python
""" AUTHOR: RAHUL VERMA """
import math
import operator
import string
import sys
import tpg
import traceback
import copy
d = {}
v = {}
fd = {}
functions = []
funccounter=-1
stackcount = -1
stack = []
class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error
    occurs.
    """
    
# These are the nodes of our abstract syntax tree.
class Node(object):
    """
    A base class for nodes. Might come in handy in the future.
    """
    def evaluate(self):
        """
        Called on children of Node to evaluate that child.
        """
        raise Exception("Not implemented.")


class ListLit(Node):
    """
    A node representing List literals.
    """
    def __init__(self):
        self.value = []
    def evaluate(self):
        return self.value    
    def ap(self,v):
        if ((type(v) is not str) and (type(v) is not Variable)):
            m = v.evaluate()
            self.value.append(m)
        else:
            self.value.append(v)  


class StringLiteral(Node):
    """
    A node representing String literals.
    """
    def __init__(self):
        self.value = ""    
    def evaluate(self):
        return self.value 
    def ap(self,v):
        if type(v) is not str:
            self.value = self.value + str(v.evaluate())
        else:
            self.value = self.value + v
               

class FloatLiteral(Node):
    """
    A node representing Float literals.
    """

    def __init__(self, value):
        self.value = float(value)
    def evaluate(self):
        return self.value

class IntLiteral(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value

class Add(Node):
    """
    A node representing addition.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        if type(self.left) is not str:
            left = self.left.evaluate()
        else:
            left = self.left    
        if type(self.right) is not str:    
            right = self.right.evaluate()
        else:
            right = self.right
        if isinstance(left,int) or isinstance(left, float):
            if isinstance(right,int) or isinstance(right,float):
                return left + right
            raise SemanticError()
        if isinstance(left,str) and isinstance (right, str):
            return left + right
        if isinstance(left,list) and isinstance (right, list):
            return left + right
        raise SemanticError()        
class Sub(Node):
    """
    A node representing subtraction.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        p=(str,int,list,float)
        while not isinstance(left, p):
            left = left.evaluate()
        while not isinstance(right, p):
            right = right.evaluate()
        if not isinstance(left, int):
            if not isinstance(left,float):
                raise SemanticError()
        if not isinstance(right, int):
            if not isinstance(right,float):
                raise SemanticError()
        return left - right
    
class Multiply(Node):
    """
    A node representing multiplication.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            if not isinstance(left,float):
                raise SemanticError()
        if not isinstance(right, int):
            if not isinstance(right,float):
                raise SemanticError()
        return left * right

class POW(Node):
    """
    A node representing multiplication.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            if not isinstance(left,float):
                raise SemanticError()
        if not isinstance(right, int):
            if not isinstance(right,float):
                raise SemanticError()
        return math.pow(left,right)

class Divide(Node):
    """
    A node representing division.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            if not isinstance(left,float):
                raise SemanticError()
        if not isinstance(right, int):
            if not isinstance(right,float):
                raise SemanticError()
        if right == 0:
            raise SemanticError()
        return left / right

class FloorDivide(Node):
    """
    A node representing division.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            if not isinstance(left,float):
                raise SemanticError()
        if not isinstance(right, int):
            if not isinstance(right,float):
                raise SemanticError()
        if right == 0:
            raise SemanticError()
        return left//right 

class Modulus(Node):
    """
    A node representing division.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            if not isinstance(left,float):
                raise SemanticError()
        if not isinstance(right, int):
            if not isinstance(right,float):
                raise SemanticError()
        if right == 0:
            raise SemanticError()
        return left%right
class Find(Node):
    """
    A node representing array indexing.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if len(right)==1:
            right1 = right[0]
            if type(right1) is Variable:
                right1 = right1.evaluate() 
            if not isinstance(right1, int):
                raise SemanticError()
        else:
            raise SemanticError()
        try:
            answer = left[right1]
            return answer
        except IndexError:
            raise SemanticError()
        except TypeError:
            raise SemanticError()  
class NOT(Node):
    """
    A node representing boolean not.
    """

    def __init__(self, left):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
    def evaluate(self):
        if type(self.left.evaluate()) is not int:
            raise SemanticError()
        left = self.left.evaluate()
        if left == 0:
            return 1
        else: 
            return 0

class GT(Node):
    """
    A node representing greater than function.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if left > right:
                    return 1
               else:
                    return 0
        raise SemanticError()

class LT(Node):
    """
    A node representing less than function.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if left < right:
                    return 1
               else:
                    return 0
        raise SemanticError()

class GTE(Node):
    """
    A node representing greater than or equal to.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if left >= right:
                    return 1
               else:
                    return 0
        raise SemanticError()                      

class LTE(Node):
    """
    A node representing less than or equal to.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if left <= right:
                    return 1
               else:
                    return 0
        raise SemanticError()                                       

class ET(Node):
    """
    A node representing equal to.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):

        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if left == right:
                    return 1
               else:
                    return 0
        raise SemanticError()

class NOTE(Node):
    """
    A node representing equal to.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if left == right:
                    return 0
               else:
                    return 1
        raise SemanticError()        

class AND(Node):
    """
    A node representing the and function.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if (left and right) > 0:
                    return 1
               else:
                    return 0
        raise SemanticError()

class OR(Node):
    """
    A node representing the or unction.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right
    def evaluate(self):
        if type(self.left.evaluate()) is int:
            if type(self.right.evaluate()) is int:
               left = self.left.evaluate()
               right = self.right.evaluate()  
               if (left or right) > 0:
                    return 1
               else:
                    return 0
        raise SemanticError()
    
class PrintNode(Node):

    def __init__(self):
        self.value = ""
    def add(self, s):
        self.value = s
    def evaluate(self):
        x = self.value.evaluate()
        p=(str,int,list,float)
        if isinstance(x, p):
            print(x)
        elif x == None:
            print(x)
        else:
            print(self.value.evaluate().evaluate())

class VariableAssignState(Node):
    def __init__(self, a=None, e=None,c=None):
        self.name = a
        self.value = e
        self.ind = c
    def evaluate(self):
        global d
        global funccounter 
        global stackcount
        global stack
        if self.ind != None:
            d[self.name][self.value.evaluate()] = self.ind.evaluate()
        else:
            if funccounter == -1:
                d[self.name]=self.value.evaluate()
            else:
                if stackcount == -1:
                    fd[functions[funccounter]].variables[self.name]=self.value
                else:
                    stack[stackcount].variables[self.name]=self.value.evaluate()


class Variable(Node):
    def __init__(self, a=None,h=-1):
        self.name = a
        self.h=h
    def evaluate(self):
        global d
        global funccounter
        global stackcount
        global stack
        if funccounter == -1:
            return d[self.name]
        else:
            if stackcount == -1:
                return fd[functions[funccounter]].variables[self.name]
            else:
                return stack[stackcount].variables[self.name]
        raise SemanticError


class WhileNode(Node):
    def __init__(self, c=0):
        self.condition = c
        self.statements = []
    def addstatements(self,a):
        self.statements.append(a)
    def evaluate(self):
        global d
        global v
        while(self.condition.evaluate()):
            for x in self.statements:
                x.evaluate()

class IfNode(Node):
    def __init__(self, c=0):
        self.condition = c
        self.statements = []
        self.elsestate = []
    def addstatements(self,a):
        self.statements.append(a)
    def addelsestate(self,a):
        self.elsestate.append(a)
    def evaluate(self):
        if(self.condition.evaluate()):
            for x in self.statements:
                if type(x) is Return:
                    return x.evaluate()
                else:
                    v=x.evaluate()
                    if type(v) is not type(None):
                        return v
        else:
            if [] != self.elsestate:
                for x in self.elsestate:
                    if type(x) is Return:
                        return x.evaluate()
                    else:
                        v=x.evaluate()
                        if type(v) is not type(None):
                            return v

class FuncNode(Node):
    def __init__(self, a, fcount=0):
        self.name = a
        self.argu=[]
        self.statements=[]
        self.argcounter=0
        self.variables={}
        self.fcount = fcount
    def addargs(self,a):
        self.argu.append(a)
        self.variables[a.name]=a
    def setargs(self,o):
        if self.argcounter>=len(self.argu):
            raise SemanticError
        else:
            self.variables[self.argu[self.argcounter].name]=o
            self.argcounter+=1
    def addstatements(self,a):
        self.statements.append(a)
    def evaluate(self):
        global funccounter
        for x in self.statements:
            funccounter = self.fcount
            if type(x) is Return:
                return x.evaluate()
            else:
                v=x.evaluate()
                if type(v) is not type(None):
                    return v
                
class FuncCall(Node):
    def __init__(self,n):
        global fd
        self.n = n
        self.f = object()
        self.args = []
    def setargsf(self,a):
        self.args.append(a)
    def setargs(self):
        h = self.f
        for x in self.args:
            h.variables[h.argu[h.argcounter].name]=x.evaluate()
            h.argcounter+=1
    def launch(self):
        self.f = copy.deepcopy(fd[self.n])
        self.setargs()
        print(self.f)        
    def evaluate(self):
        self.f = copy.deepcopy(fd[self.n])
        self.setargs()
        global stackcount
        global stack
        stackcount+=1
        stack.append(self.f)
        v=self.f.evaluate()
        if type(v) is not type(None):
            return v        
        
class Return(Node):
    def __init__(self):
        self.link = Node()
        self.statement = Node()
    def setlinl(self,l):
        self.link = l
    def addstatement(self,s):
        self.statement = s
    def evaluate(self):
        global stack
        global stackcount
        v=self.statement.evaluate()
        stack.pop()
        stackcount-=1
        return v
        

class BodyNode(Node):
    def __init__(self):
        self.statements = []
    def addstatements(self,a):
        self.statements.append(a)
    def evaluate(self):
        global funccounter
        for x in self.statements:
            funccounter = -1
            x.evaluate()


# This is the TPG Parser that is responsible for turning our language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    r"""
    separator spaces: '\s+';
    token real: '\d*\.\d+'  FloatLiteral;
    token number: "\d+" IntLiteral;
    token word: '[a-zA-z][a-zA-Z0-9_!@#$:]*';
    Pick/a -> 
        word/a | number/a | real/a | '[\\]["]' $ a = "\""$;
    String/s ->
        '\"'                    $s= StringLiteral()  
        (Pick/a                 $s.ap(a+" ")
        )*
        '\"'
        ;
    Pick2/a ->
        String/a | number/a | real/a;    
    other/s ->    
        number/a                  $ s = a
        '\]'                      $ 
        ;
    START/a ->  ((func/a)*(Body/a)+)* ;
    expression/a ->  If/a | While/a | printstate/a  | Vari/a | VariList/a | funCall/a | addsub/a |ret/a;
    fexpression/a -> If/a | While/a | printstate/a  | Vari/a | VariList/a | funCall/a | addsub/a |ret/a;
    addsub/a -> muldivbool/a ("\+" muldivbool/b $ a = Add(a, b) $| "\-"  parens/b $ a = Sub(a, b) $)* ;
    muldivbool/a -> parens/a( "\*\*" parens/b $ a = POW(a,b) $|
                "\*" parens/b $ a = Multiply(a, b) $|
                "\/\/"  parens/b $ a = FloorDivide(a, b) $| 
                "\/"  parens/b $ a = Divide(a, b) $| 
                "\%"  parens/b $ a = Modulus(a, b) $|
                      parens/b $ a = Find(a,b) $|
                "[&][&]"  parens/b $ a = AND(a,b) $|
                "[o][r]"  parens/b $ a = OR(a,b) $|
                "[>][=]"  parens/b $ a = GTE(a,b) $|
                "[<][=]"  parens/b $ a = LTE(a,b) $|
                "[<][>]"  parens/b $ a = NOTE(a,b) $|
                "[=][=]"  parens/b $ a = ET(a,b) $|
                "[>]"  parens/b $ a = GT(a,b) $|
                "[<]"  parens/b $ a = LT(a,b) $)* ;
    parens/a -> "\(" expression/a "\)" | literal/a | "[n][o][t]" expression/b $ a = NOT(b) $;
    literal/a ->  String/a  | List/a | number/a | real/a |funCall/a | Varl/a;

    List/l ->
        '\['                      $ l = ListLit()
        expression/a              $ l.ap(a)
        ( ',' expression/a        $ l.ap(a)
        )* 
        '\]'
        ;

    Body/a->
        '\{'                          $a=BodyNode()
                                      $self.resetfunc()
        (expression/b                 $a.addstatements(b)
         )*
         '\}'                       $a.evaluate()
                                  $print("\n")
        ;

    printstate/a ->
        'print\s*\('               $a = PrintNode()
        expression/b               $a.add(b)
        '\)'
        '\;'                    
        ;
    
    While/a ->
        'while\s*\('                  
        expression/b               $a=WhileNode(b)
        '\)'
        '\{'                       
        (expression/c              $a.addstatements(c)
        )*
        '\}'                                                       
        ;

    If/a ->
        'if\s*\('                     
        expression/b              $a=IfNode(b)
        '\)'
        '\{'
        (expression/c             $a.addstatements(c)
        )*
        '\}'
        ('else\s*\{'
        (expression/c             $a.addelsestate(c)
        )*       
        '\}'
        )?                                                                    
        ;

    funCall/a ->
        word/d'\('                $a = FuncCall(d)
        expression/b?             $a.setargsf(copy.deepcopy(b))
        ( ',' expression/b        $a.setargsf(copy.deepcopy(b))
        )*
        '\)'                      
        ;

    ret/a ->
        'return'                $a=Return()
        expression/c?           $a.addstatement(c)
        '\;'
        ;

    func/a ->
     word/d'\('                   $a=FuncNode(d)
                                  $self.getfd()[a.name]=a
                                  $self.getfunctions().append(a.name)
    VarId/b?                      $a.addargs(b)
     ( ',' VarId/b                 $a.addargs(b)
     )*
     '\)'
     '\{'                         $self.funcinc()
                                  $global funccounter
                                  $a.fcount=funccounter
     (fexpression/c              $a.addstatements(c)$|
      ret/c                      $a.addstatements(c)
     )*     
     '\}'
                                  $self.getfd()[a.name]=a

     ;

    Vari/a -> VarId/v '\=' expression/e '\;' $a = VariableAssignState(v.name,e)
                                             $self.getv()[v.name]=v
                                       ;
    VariList/a -> Varl/v '\[' expression/x '\]' '\=' expression/e '\;'$ a = VariableAssignState(v.name,x,e)
                                       ;
    VarId/v ->  
            String2/x   $global funccounter
                        $v = Variable(x,funccounter)
            ;
    String2/s ->
                        $a=StringLiteral()
         (word/t        $a.ap(t)
         )+
                        $s=a.evaluate()   
        ;



    Varl/x -> String2/v $if v in self.getv():
                        $   x=self.getv()[v]
                        $else:
                        $   x=""
        ;
    """
    def getv(self):
        global v
        global funccounter
        global fd
        global functions
        if funccounter == -1:
            return v
        else:
            return fd[functions[funccounter]].variables
    def getfd(self):
        global fd
        return fd 
    def resetfunc(self):
        global funccounter
        funccounter=-1
    def funcinc(self):
        global funccounter
        funccounter+=1
    def getfunctions(self):
        global functions
        return functions
    verbose = 2

# Make an instance of the parser. This acts like a function.
parse = Parser()

# This is the driver code, that reads in lines, deals with errors, and
# prints the output if no error occurs.

# Open the file containing the input.
parse = Parser()
try:
    f = open(sys.argv[1], "r")
except(IndexError, IOError):
    print("No file found.")
    sys.exit(0)
# For each line in f
try:
        # Try to parse the expression.
    print("HW (HW test)")
    node = parse(f.read())
        # If an exception is thrown, print the appropriate error.
except tpg.Error:
    print("SYNTAX ERROR")
            # Uncomment the next line to re-raise the syntax error,
            # displaying where it occurs. Comment it for submission.
            # raise
        
except SemanticError:
    print("SEMANTIC ERROR")
    print(traceback.format_exc())
            # Uncomment the next line to re-raise the semantic error,
            # displaying where it occurs. Comment it for submission.
            # raise
f.close()
