# Author: Silviu Velica
# Date: August 2016
# Description: 
#	This is a program that draws the truth table for a propositional logic
#	formula given by the user. It translates the pretty standard syntax 
#	in which the user writes the formula to the syntax of python functions,
#	then executes the new formula and draws its truth table. It also tells
#	whether the formula is valid, contingent, or contradictory.


from sys import exit

answer = None
top_line = ' '
ord_keys = None
ord_props = []
run_num = 0
valid = []
dictionary = {}
R = []
index_r = 0

# the list of propositional variables that can be used
props = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# list of accepted logical connectives...
connectives = ["and", "or", "xdis", "implies", "nicod", "equivalent", "sheffer", "not"]

# ...and their translation to functions defined later on
operator_dict = {"and": "conjunction", "not": "negation", "implies": "implies", "or": "disjunction",
"xdis": "edisjunction", "nicod": "nicod", "equivalent": "equivalent", "sheffer": "sheffer"}


print """
\tThis program draws the truth table for a propositional logic formula.

\tAcceptable propositional variables: A, B, C, D, E, F, G, H, I, J
\tAcceptable logical operators: not, and, or, implies, xdis, equivalent, nicod, sheffer

\tTo display the syntactic rules, write "syntax".

\tTo display the definitions for the logical operators, write "operators".

\tTo display both syntax and definitions, write "both".

\tIf you don't need to see the syntax or definitions, write your formula directly.

\tTo exit the program now, write "quit".
"""

operator_def = """
"not" - true if argument is false, false if argument is true;

"and" - conjunction; true if BOTH arguments are true; false otherwise;

"or" - disjunction; false if BOTH arguments are false; true otherwise;

"xdis" - exclusive disjunction; true if ONLY ONE argument is true; false otherwise;

"implies" - implication; false if antecedent is true and consequent, false; true otherwise;

"equivalent" - equivalence/biconditional; true when BOTH arguments have the same value; false otherwise;

"nicod" - Nicod's operator/NOR; true when BOTH arguments are false; false otherwise;

"sheffer" - Sheffer's stroke/NAND; false when BOTH arguments are true; true otherwise.
"""

syntax = """
1. Square brackets '[]' and curly brackets '{}' are not accepted.
\tCORRECT: A and (B and (C and D))
\tINCORRECT: {A and [B and (C and D)]}

2. You can't have more than 10 propositional variables in the formula.

3. The accepted propositional variables are the letters from 'A' to 'J' (10 in total).

4. Always put each operator and its arguments in parentheses, including negation.
\tCORRECT: A and (not B)
\tINCORRECT: A and not B

5. Always leave a space [' '] between the operator and its arguments.
\tCORRECT: A and (not B)
\tINCORRECT: A and(notB)

6. All operators except 'not' are strictly binary.
\tCORRECT: A and (B and C)
\tINCORRECT: A and B and C

7. The formula may contain only logical operators, propositional variables, spaces [' '], and parentheses.
"""

def dead(a):
	print a
	exit(0)

# displaying the rules on each run of the program would have been annoying...
while answer != "quit":
	answer = raw_input("\t--> ")

	if answer == "syntax":
		print syntax

	elif answer == "operators":
		print operator_def
	
	elif answer == "both":
		print syntax
		print operator_def

	elif answer == "quit":
		dead("Goodbye!")
	
	else:
		formula = answer
		break
		
formula = "(" + formula + ")"

# formula is stored in two variables, one to translate, the other to use later		
new_formula = formula

# testing if the formula was spelled correctly by the user
def syntax_check():
	
	if formula.count('(') <> formula.count (')'):
		dead("\nInvalid Syntax: check parentheses!")
	
	if len(formula) <= 3:
		dead("\nInvalid Syntax: formula too short!")

	operator_no = 0
	prop_no = 0

	# checking whether there is at least one connective in the formula
	for connective in connectives:
		if connective in formula:
			operator_no += 1
	
	if operator_no == 0:
		dead("\nInvalid Syntax: need at least one operator!")
	
	# checking whether there is at least one propositional variable in the formula
	for prop in props:
		if prop in formula:
			prop_no += 1
			
	if prop_no == 0:
		dead("\nInvalid Syntax: need at least one propositional variable!")

	test_formula = formula.split('(')
	test_formula = ' '.join(test_formula)
	test_formula = test_formula.split(')')
	test_formula = ' '.join(test_formula)
	test_formula = test_formula.split(' ')
	
	# making sure the formula is only made up of propositional variables and operators
	for term in test_formula:
		if (not term in connectives and not term in props) and term != '':
			dead("\nInvalid Syntax: unknown variable or connective!")

	# checking whether operators and their arguments have been combined correctly
	for value in dictionary.values():
		
		if len(value.split(' ')) > 3:
			dead("\nInvalid Syntax: too many objects in a pair of parentheses!")
		
		for key in dictionary.keys():
			for connective in connectives:
				if (connective == "not" and connective in value) and key in value:
					if value != connective + ' ' + key:
						dead("\nInvalid Syntax: a negation is spelled wrong!")
						
				elif (connective == "not" and connective in value) and "R" in value:
					if not connective + ' R' in value:
						dead("\nInvalid Syntax: a negation is spelled wrong!")
				
				elif connective != "not" and connective in value:
					for connective2 in connectives:
						if (connective in value and connective2 in value) and connective != connective2:
							dead("\nInvalid Syntax: can't have more than one connective in a pair of parentheses!")
						elif connective == connective2 and value.count(connective) > 1:
							dead("\nInvalid Syntax: a connective is repeated!")
						
					for key2 in dictionary.keys():
						if (key in value and key2 in value) and key != key2:
							if value != key + ' ' + connective + ' ' + key2 and value != key2 + ' ' + connective + ' ' + key:
								dead("\nInvalid Syntax: binary operation spelled wrong!")
							
					if "] " in value and " R" in value:
						if not '] ' + connective + ' R' in value:
							dead("\nInvalid Syntax: binary operator spelled wrong!")
								
					if key in value and 'R' in value:
						if not '] ' + connective + ' ' + key and not key + ' ' + connective + ' R':
							dead("\nInvalid Syntax: binary operator spelled wrong!")
		

# replacing the propositional letters in the formula with names of values in a list ("R[n]")
# this will be used when writing the truth table
for index, item in enumerate(props):
	if item in formula:
		exec("cr = \"R[%d]\"" % index_r)
		new_formula = new_formula.replace(props[index], cr)
		R.append(None)
		index_r += 1


# reading the formula written by the user
# each iteration eliminates a pair of parentheses
while len(new_formula) > 3:
	
	run_num += 1
	# each pair of parentheses is separated then stored in a dictionary
	# I use exec to generate as many variables as needed
	slice = new_formula.split(')')
	exec("slice%d = slice[0].split('(')" % run_num)
		
	exec("dictionary['P%d'] = slice%d[-1]" % (run_num, run_num))
	ord_keys = dictionary.keys()
	ord_keys = sorted(ord_keys)
	
	# each pair of parentheses is now replaced with a variable
	exec("new_formula = new_formula.replace('(' + slice%d[-1] + ')', ord_keys[%d - 1])" % (run_num, run_num))


syntax_check()


if ord_keys != None:
	ord_keys = sorted(ord_keys, reverse = True)
else:
	pass

# starting the translation into python's functional syntax
for key, value in dictionary.items():
	for operator in operator_dict.keys():
		if operator in value:
			elem = value.split(' ')
			# translating the operators and rearranging their arguments
			if len(elem) > 2:
				dictionary[key] = operator_dict[operator] + "(" + elem[0] + ", " + elem[2] + ")"
			elif len(elem) == 2:
				dictionary[key] = operator_dict[operator] + "(" + elem[1] + ")"

# finally, putting together the new formula
for key in ord_keys:
	new_formula = new_formula.replace(key, dictionary[key])

# this check is not really needed here, but useful if you want to use it elsewhere
def check_boolean(a, b):
	if not a in [True, False] or not b in [True, False]:
		dead("Operators only work with truth values!")

# defining functions for each logical operator
def implies(a, b):
	check_boolean(a, b)
	if a == True and b == False:
		return False
	else:
		return True

def conjunction(a, b):
	check_boolean(a, b)
	return a and b
	
		
def disjunction(a, b):
	check_boolean(a, b)
	return a or b
	
def edisjunction(a, b):
	check_boolean(a, b)
	if a == b:
		return False
	else:
		return True

def equivalent(a, b):
	check_boolean(a, b)
	if a == b:
		return True
	else:
		return False

def negation(a):
	check_boolean(a, True)
	return not a

def nicod(a, b):
	check_boolean(a, b)
	if a == False and b == False:
		return True
	else:
		return False

def sheffer(a, b):
	check_boolean(a, b)
	if a == True and b == True:
		return False
	else:
		return True

# generating the table's header
for prop in props:
	if prop in formula:
		top_line += prop + "\t"
	else:
		pass

print "\n", top_line, formula, "\n"		

# ...and the rows of the table
def num_tabs(i, R, stuff):
	for index in range(i):
		print R[index], "\t",
	print "\t", stuff	

def calc(i):

	for R[i] in [True, False]:
		if i == len(R) - 1:
			exec("stuff = %s" % new_formula)
			num_tabs(i + 1, R, stuff)
			valid.append(stuff)
		else:
			calc(i + 1)
			
calc(0)

# this bit is to tell us what type of formula we have
if False in valid and True in valid:
	print "\n\tThe formula is contingent.\n"
elif not (True in valid):
	print "\n\tThe formula is a contradiction.\n"
else:
	print "\n\tThe formula is valid.\n"
