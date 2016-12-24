# AUTHOR: RAHUL VERMA
# Seawolf-Language-Parser

RUNNING THE SEAWOLF-LANGUAGE PROGRAM:
- To run this program you must have TPG. Please visit http://cdsoft.fr/tpg/ to see how to run programs that use TPG.
- You must save your seawolf program as a .txt file.
- Let's for example call our program userprogram.txt. On the command line you can run this program as follows:
	python3 seawolfParse.py userprogram.txt


The seawolf language provides the user with variables, operations between variables, conditional statements, loops, functions and a built-in print function.

VARIABLES:

- To declare a variable we use the following recipe : NAMEofVARIABLE '=' VARIABLEVALUE ';'
	ex. height = 51;
- A variable in the seawolf language can have many different types. These types are integers, floats, and strings. As for boolean values, 0 equates to FALSE, and any number greater than 0  equates to TRUE.




OPERATIONS:

- In the seawolf language we have two types of operations that can occur between two variables, arithmetic operations and logical operations.


CONDITIONALS:
- The language supports the usual conditionals:
	if(condition){
		//if condition body	
	}else{
		//else condition body
	}

LOOPS:
- The seawolf language supports while loops only. Here is an example:

	while(condition){
		//while loop body
	}


FUNCTIONS:

- Functions are declared as follows:
	name(paramater1, paramater2, ...., parametern){
		//body
	}
  
  The seawolf language also supports recursive functions.

BUILT-IN FUNCTIONS:
- The seawolf language has a built in print() function that allows the user to print out variables. Here is an example:
	
	a = 5;
	print(a);

This would print 5 to the screen.

- You can also make function calls inside of the print() function. 

IMPORTANT NOTES ABOUT THE LANGUAGE:

- All functions calls must be contained inside the body of curly brakets.
- Please see the EXAMPLE PROGRAMS for a better understanding of how the language works. Also, please play around with the example programs.

################################################################################
#################################EXAMPLE PROGRAMS###############################
################################################################################


#################################PROGRAM 1######################################

gcd(a,b){

    t = b;

    b = a % b;

    if(b == 0){

        return t;

    } else {

        return gcd(t,b);

    }

}

{

    print(gcd(32,18));

}

################################################################################

#################################PROGRAM 2######################################

ackermann(m,n){

    if(m == 0){

        return n+1;

    } else {

        if(n == 0){

            return ackermann(m-1,1);

        } else {

            return ackermann(m-1,ackermann(m,n-1));

        }

    }

}

{

    print(ackermann(1,2));

}

###############################################################################


