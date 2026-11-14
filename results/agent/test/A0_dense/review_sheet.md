# Review sheet (grade manually; gold shown for the reviewer only)

## n01 — answerable — status: answered
**Q:** What does Python's or operator return?  
**Expected:** It takes two condition operands and returns True if either condition is true (False only when both are false).  
**Queries:** ['or operator']  
**Answer:** Python's `or` operator takes two condition operands and returns `True` if either condition is true. If both conditions are false, it returns `False`. This is illustrated in the truth table for `p or q`, where the result is `True` for all cases except when both `p` and `q` are `False` [p0105:c02].  
> [p0105:c02] p.105: if (x < 10) and (y > 20): z = 5 else: z = 0 a. 0 b. 5 Logical operator: or Sometimes a decision only requires one condition to be true. Ex: If a student is in the band or choir, they will perform in the spring concert. The or operator takes two condition operands and returns True if either condition is true. p q p or q True True True True False True False True True False False False Table 4.2 Truth table: p or q.

## n02 — answerable — status: answered
**Q:** How many logical operators does Python have, and which are they?  
**Expected:** Three: and, or, and not.  
**Queries:** ['logical operators']  
**Answer:** Python has three logical operators: and, or, and not. These operators take condition operands and produce True or False results based on the evaluation of those conditions. For example, the 'and' operator returns True only if both conditions are true, while 'or' returns True if at least one condition is true, and 'not' negates the truth value of a condition. [p0104:c03] [p0121:c00] [p0108:c02]  
> [p0104:c03] p.104: Logical operator: and Decisions are often based on multiple conditions. Ex: A program printing if a business is open may check that hour >= 9 and hour < 17. A logical operator takes condition operand(s) and produces True or False. Python has three logical operators: and, or, and not. The and operator takes two condition operands and returns True if both conditions are true.
> [p0121:c00] p.121: 4.8 Chapter summary Highlights from this chapter include: • Booleans represent a value of True or False. • Comparison operators compare values and produce True or False. • Logical operators take condition operand(s) and produce True or False. • Operators are evaluated in order according to precedence and associativity. • Conditions are expressions that evaluate to True or False. • Decision statements allow different paths of execution (branches) through code based on conditions. • Decision state
> [p0108:c02] p.108: Operator Meaning () Parentheses ** Exponentiation (right associative) *, /, //, % Multiplication, division, floor division, modulo +, - Addition, subtraction <, <=, >, >=, ==, != Comparison operators not Logical not operator and Logical and operator or Logical or operator Table 4.4 Operator precedence from highest to lowest.

## n03 — answerable — status: answered
**Q:** In the miles-per-gallon example, what does the function return when gallons is 0, and why that value?  
**Expected:** It returns -1 (after printing "Gallons can't be 0"), a value often used to indicate a problem, to avoid division by zero.  
**Queries:** ['miles-per-gallon example', 'calc_mpg gallons 0']  
**Answer:** When gallons is 0, the function `calc_mpg` returns -1. This value is used to indicate a problem, specifically to avoid division by zero, as the function checks if gallons is greater than 0 before performing the division. If gallons is 0, it prints "Gallons can't be 0" and then returns -1 instead of attempting the division, which would result in an error. This behavior is illustrated in the example where `car_2_mpg = calc_mpg(300, 0)` results in -1 being returned and the message being printed [p0166:c01][p0166:c00].  
> [p0166:c01] p.166: def calc_mpg(miles, gallons): if gallons > 0: mpg = miles/gallons return mpg else: print("Gallons can't be 0") return -1 car_1_mpg = calc_mpg(448, 16) print("Car 1's mpg is", car_1_mpg) car_2_mpg = calc_mpg(300, 0)
> [p0166:c00] p.166: function and return control flow to the calling code. In the table below, calc_mpg() takes in miles driven and gallons of gas used and calculates a car's miles per gallon. calc_mpg() checks if gallons is 0 (to avoid division by 0), and if so, returns -1, a value often used to indicate a problem.

## n04 — answerable — status: answered
**Q:** What is the difference between a function argument and a function parameter?  
**Expected:** An argument is a value passed as input during a function call; a parameter is the variable representing that input in the function definition.  
**Queries:** ['function argument parameter']  
**Answer:** A function argument is a value passed as input during a function call, while a function parameter is a variable that represents the input in the function definition. Although the terms "argument" and "parameter" are sometimes used interchangeably, they have distinct meanings in programming contexts. [p0160:c02]  
> [p0160:c02] p.160: Arguments and parameters What if a programmer wants to write a function that prints the contents of a list? Good practice is to pass values directly to a function rather than relying on global variables. A function argument is a value passed as input during a function call. A function parameter is a variable representing the input in the function definition. Note: The terms "argument" and "parameter" are sometimes used interchangeably in conversation and documentation.

## n05 — answerable — status: answered
**Q:** When a function that was called by another function finishes, where does control flow go?  
**Expected:** Control flow returns to the calling function.  
**Queries:** ['function control flow']  
**Answer:** When a function that was called by another function finishes, control flow moves back to where the function was called and continues the sequence of execution from that point onward. This means that after executing the function statements, the program returns to the original calling location to resume execution. [p0151:c04]  
> [p0151:c04] p.151: Control flow and functions Control flow is the sequence of program execution. A program's control flow begins at the main program but rarely follows a strict sequence. Ex: Control flow skips over lines when a conditional statement isn't executed. When execution reaches a function call, control flow moves to where the function is defined and executes the function statements. Then, control flow moves back to where the function was called and continues the sequence. CHECKPOINT Calling a brunch menu

## n06 — answerable — status: answered
**Q:** Why not simply make every variable global to avoid scope errors?  
**Expected:** Making every variable global makes a program messy: if the whole program can modify a variable, a bug could be anywhere; limiting scope makes programs easier to debug/maintain.  
**Queries:** ['global variables scope errors']  
**Answer:** Making every variable global can lead to a messy program, making debugging difficult. If a variable can be modified anywhere in the program, it becomes challenging to identify where a bug originates. Limiting a variable's scope to only what is necessary helps in making the program easier to debug, maintain, and update [p0159:c00].  
> [p0159:c00] p.159: is_dst = True hour = int(input("Enter hour: ")) update_hour() print("New hour:", new_hour) a. New hour: 9 b. New hour: 10 c. Error BENEFITS OF LIMITING SCOPE A programmer might ask, "Why not just make all variables global variables to avoid access errors?" Making every variable global can make a program messy. Ex: A programmer debugging a large program discovers a variable has the wrong value. If the whole program can modify the variable, then the bug could be anywhere in the large program. Limi

## u04 — UNANSWERABLE — status: abstain
**Q:** What does the yield keyword do inside a generator function?  
**Expected:** No 'yield' or 'generator' token in the corpus.  
**Queries:** ['yield keyword generator function', 'generator function yield']  
**Answer:** The passages do not cover the function of the yield keyword inside a generator function.  

## u05 — UNANSWERABLE — status: abstain
**Q:** How do *args and **kwargs let a function accept a variable number of arguments?  
**Expected:** No '*args', 'kwargs', 'variable number' or 'arbitrary' in the corpus; section 6.6 covers keyword/default arguments only.  
**Queries:** ['*args **kwargs variable number of arguments', '*args **kwargs']  
**Answer:** The textbook does not provide specific information on how *args and **kwargs allow a function to accept a variable number of arguments. Therefore, I cannot provide an answer based on the passages available.  
