# Review sheet (grade manually; gold shown for the reviewer only)

## n01 — answerable — status: answered
**Q:** What does Python's or operator return?  
**Expected:** It takes two condition operands and returns True if either condition is true (False only when both are false).  
**Queries:** ['or operator']  
**Answer:** Python's or operator takes two condition operands and returns True if either condition is true. For example, in a situation where a student is in the band or choir, the or operator would evaluate to True if at least one of those conditions is met. The truth table for the or operator shows that it returns True in three out of four possible combinations of truth values for its operands: True or True is True, True or False is True, and False or True is True; only False or False is False [p0105:c02].  
> [p0105:c02] p.105: if (x < 10) and (y > 20): z = 5 else: z = 0 a. 0 b. 5 Logical operator: or Sometimes a decision only requires one condition to be true. Ex: If a student is in the band or choir, they will perform in the spring concert. The or operator takes two condition operands and returns True if either condition is true. p q p or q True True True True False True False True True False False False Table 4.2 Truth table: p or q.

## n02 — answerable — status: answered
**Q:** How many logical operators does Python have, and which are they?  
**Expected:** Three: and, or, and not.  
**Queries:** ['logical operators']  
**Answer:** Python has three logical operators: and, or, and not. These operators take condition operands and produce True or False [p0104:c03].  
> [p0104:c03] p.104: Logical operator: and Decisions are often based on multiple conditions. Ex: A program printing if a business is open may check that hour >= 9 and hour < 17. A logical operator takes condition operand(s) and produces True or False. Python has three logical operators: and, or, and not. The and operator takes two condition operands and returns True if both conditions are true.

## n03 — answerable — status: answered
**Q:** In the miles-per-gallon example, what does the function return when gallons is 0, and why that value?  
**Expected:** It returns -1 (after printing "Gallons can't be 0"), a value often used to indicate a problem, to avoid division by zero.  
**Queries:** ['miles-per-gallon example gallons is 0']  
**Answer:** In the miles-per-gallon example, when gallons is 0, the function returns -1. This value is returned to indicate a problem, specifically to avoid division by zero, which would occur if the function attempted to calculate miles per gallon with a denominator of zero. The function checks if gallons is greater than 0 before performing the calculation, and if not, it prints "Gallons can't be 0" and returns -1 instead [p0166:c01][p0166:c00].  
> [p0166:c01] p.166: def calc_mpg(miles, gallons): if gallons > 0: mpg = miles/gallons return mpg else: print("Gallons can't be 0") return -1 car_1_mpg = calc_mpg(448, 16) print("Car 1's mpg is", car_1_mpg) car_2_mpg = calc_mpg(300, 0)
> [p0166:c00] p.166: function and return control flow to the calling code. In the table below, calc_mpg() takes in miles driven and gallons of gas used and calculates a car's miles per gallon. calc_mpg() checks if gallons is 0 (to avoid division by 0), and if so, returns -1, a value often used to indicate a problem.

## n04 — answerable — status: answered
**Q:** What is the difference between a function argument and a function parameter?  
**Expected:** An argument is a value passed as input during a function call; a parameter is the variable representing that input in the function definition.  
**Queries:** ['function argument parameter']  
**Answer:** A function argument is a value passed as input during a function call, while a function parameter is a variable representing the input in the function definition. The terms "argument" and "parameter" are sometimes used interchangeably in conversation and documentation [p0160:c02].  
> [p0160:c02] p.160: Arguments and parameters What if a programmer wants to write a function that prints the contents of a list? Good practice is to pass values directly to a function rather than relying on global variables. A function argument is a value passed as input during a function call. A function parameter is a variable representing the input in the function definition. Note: The terms "argument" and "parameter" are sometimes used interchangeably in conversation and documentation.

## n05 — answerable — status: answered
**Q:** When a function that was called by another function finishes, where does control flow go?  
**Expected:** Control flow returns to the calling function.  
**Queries:** ['function control flow']  
**Answer:** When a function that was called by another function finishes, control flow moves back to where the function was called and continues the sequence of execution from that point. This means that after executing the function statements, the program returns to the original calling location to resume execution [p0151:c04].  
> [p0151:c04] p.151: Control flow and functions Control flow is the sequence of program execution. A program's control flow begins at the main program but rarely follows a strict sequence. Ex: Control flow skips over lines when a conditional statement isn't executed. When execution reaches a function call, control flow moves to where the function is defined and executes the function statements. Then, control flow moves back to where the function was called and continues the sequence. CHECKPOINT Calling a brunch menu

## n06 — answerable — status: abstain
**Q:** Why not simply make every variable global to avoid scope errors?  
**Expected:** Making every variable global makes a program messy: if the whole program can modify a variable, a bug could be anywhere; limiting scope makes programs easier to debug/maintain.  
**Queries:** ['global variables scope errors', 'global variables disadvantages']  
**Answer:** The textbook does not specifically address the disadvantages of using global variables or the reasons against making every variable global to avoid scope errors. Therefore, I cannot provide a definitive answer based on the available passages.  

## u04 — UNANSWERABLE — status: abstain
**Q:** What does the yield keyword do inside a generator function?  
**Expected:** No 'yield' or 'generator' token in the corpus.  
**Queries:** ['yield keyword generator function', 'generator function yield']  
**Answer:** The passages do not cover the function of the yield keyword inside a generator function.  

## u05 — UNANSWERABLE — status: abstain
**Q:** How do *args and **kwargs let a function accept a variable number of arguments?  
**Expected:** No '*args', 'kwargs', 'variable number' or 'arbitrary' in the corpus; section 6.6 covers keyword/default arguments only.  
**Queries:** ['*args **kwargs variable number of arguments', '*args **kwargs']  
**Answer:** The textbook does not provide specific information about how *args and **kwargs allow a function to accept a variable number of arguments. Therefore, I cannot provide an answer based on the passages available.  
