# Review sheet (grade manually; gold shown for the reviewer only)

## q01 — answerable — status: answered
**Q:** Which values does bool() convert to False?  
**Expected:** 0 and the empty string (any non-zero number or non-empty string becomes True).  
**Queries:** ['bool() convert to False']  
**Answer:** The values that bool() converts to False are 0 and an empty string. Specifically, 0 represents zero in numeric types, and an empty string is a string with no characters [p0097:c01].  
> [p0097:c01] p.97: bool() converts a value to a Boolean value, True or False. • True: any non-zero number, any non-empty string • False: 0, empty string CHECKPOINT Converting integers, floats, and strings using bool() Converting integers, floats, and strings using bool(); ch 4, video 2 (https://www.openstax.org/r/converting- using-bool)

## q02 — answerable — status: answered
**Q:** What goes wrong if I write is_zero = num=0 when I meant to test whether num is zero?  
**Expected:** It assigns 0 to both is_zero and num regardless of num's original value; = is assignment, == is comparison.  
**Queries:** ['is_zero = num=0']  
**Answer:** If you write `is_zero = num=0`, it will always assign both `is_zero` and `num` with 0, regardless of the original value of `num`. This is because the `=` operator performs assignment, while the `==` operator is used for comparison and does not modify the variable. Therefore, the intended test to check if `num` is zero will not occur, leading to incorrect logic in your program [p0099:c01].  
> [p0099:c01] p.99: compare_result = (z == "coriander") a. True b. False 20 . a = "dog" compare_result = (a < "cat") a. True b. False = VS == A common mistake is using = for comparison instead of ==. Ex: is_zero = num=0 will always assign is_zero and num with 0, regardless of num's original value. The = operator performs assignment and will modify the variable. The == operator performs comparison, does not modify the variable, and produces True or False. EXPLORING FURTHER • Unicode Basic Latin Chart (https://openst

## q03 — answerable — status: answered
**Q:** How many spaces per indentation level does the PEP 8 style guide recommend?  
**Expected:** Four spaces per indentation level.  
**Queries:** ['PEP 8 indentation', 'PEP 8 indentation spaces']  
**Answer:** The PEP 8 style guide recommends four spaces per indentation level [p0100:c05].  
> [p0100:c05] p.100: The if statement's body must be grouped together and have one level of indentation. The PEP 8 style guide recommends four spaces per indentation level. The Python interpreter will produce an error if the body is empty.

## q04 — answerable — status: answered
**Q:** When an if-else statement runs, can both the if body and the else body execute?  
**Expected:** No. One and only one of the branches is taken.  
**Queries:** ['if-else statement execution']  
**Answer:** When an if-else statement is executed, one and only one of the branches is taken. That is, the body of the if or the body of the else is executed, but not both [p0102:c02].  
> [p0102:c02] p.102: An else statement is used with an if statement and contains a body of statements that is executed when the if statement's condition is false. When an if-else statement is executed, one and only one of the branches is taken. That is, the body of the if or the body of the else is executed. Note: The else statement is at the same level of indentation as the if statement, and the body is indented.

## q05 — answerable — status: answered
**Q:** Which operator is the main exception to left associativity, and how is 2 ** 3 ** 4 evaluated?  
**Expected:** Exponentiation is right associative, so 2 ** 3 ** 4 is evaluated as 2 ** (3**4).  
**Queries:** ['operator exception to left associativity', '2 ** 3 ** 4 evaluation']  
**Answer:** The main exception to left associativity is the exponentiation operator (**), which is right associative. This means that expressions involving exponentiation are evaluated from right to left. For example, the expression 2 ** 3 ** 4 is evaluated as 2 ** (3 ** 4) rather than (2 ** 3) ** 4 [p0109:c00].  
> [p0109:c00] p.109: 1 . x ** 2 + 6 / 3 a. 6 / 3 b. x ** 2 c. 2 + 6 2 . not 3 * 5 > 10 a. 3 * 5 b. not 3 c. 5 > 10 3 . z == 5 and x / 8 < 100 a. 5 and x b. x / 8 c. 8 < 100 Associativity What if operators beside each other have the same level of precedence? Associativity determines the order of operations when precedence is the same. Ex: 8 / 4 * 3 is evaluated as (8/4) * 3 rather than 8 / (4*3) because multiplication and division are left associative. Most operators are left associative and are evaluated from left t

## q06 — answerable — status: answered
**Q:** How does Python evaluate a chained comparison such as 10 < x <= 20?  
**Expected:** As 10 < x and x <= 20, evaluated from left to right.  
**Queries:** ['chained comparison']  
**Answer:** Python evaluates a chained comparison such as 10 < x <= 20 by converting it into two separate comparisons: 10 < x and x <= 20. This evaluation is done from left to right, meaning both conditions must be true for the entire expression to be true [p0109:c01].  
> [p0109:c01] p.109: When comparison operators are chained, the expression is converted into the equivalent combination of comparisons and evaluated from left to right. Ex. 10 < x <= 20 is evaluated as 10 < x and x <= 20.

## q07 — answerable — status: answered
**Q:** Why can two separate if statements give a student a double grade curve, and what fixes it?  
**Expected:** Separate if statements do not guarantee only one branch is taken, so both can execute; chaining with elif fixes it.  
**Queries:** ['two separate if statements double grade curve', 'fix double grade curve']  
**Answer:** Two separate if statements can lead to a double grade curve because they do not guarantee that only one branch is executed. This means that if both conditions are true, both branches can be executed, resulting in an unintended cumulative effect on the student's score. For example, if a student's score is 60, both if statements might be executed, incorrectly raising the score to 75 [p0111:c02].

To fix this issue, the use of chained decision statements with `elif` is recommended. This structure ensures that once a condition is met, the subsequent conditions are not evaluated, preventing multiple branches from being executed. By using `elif`, the program can check for multiple conditions in a controlled manner, ensuring that only one adjustment to the score is made [p0111:c03]. 

Thus, replacing separate if statements with an if-elif structure can effectively resolve the problem of double grading.  
> [p0111:c02] p.111: elif Sometimes, a complicated decision is based on more than a single condition. Ex: A travel planning site reviews the layovers on an itinerary. If a layover is greater than 24 hours, the site should suggest accommodations. Else if the layover is less than one hour, the site should alert for a possible missed connection. Two separate if statements do not guarantee that only one branch is taken and might result in both branches being taken. Ex: The program below attempts to add a curve based on 
> [p0111:c03] p.111: score = int(input()) if score < 70: score += 10 # Wrong: if 70 <= score < 85: score += 5 Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short for else if) statement checks a condition when the prior decision statement's condition is false. An elif statement is part of a chain and must follow an if (or elif) statement. if-elif statement template: # Statements before if condition: # Body elif condition: # Body # Statements after

## q08 — answerable — status: answered
**Q:** What precedence do conditional expressions have compared with other Python operations?  
**Expected:** The lowest precedence of all Python operations.  
**Queries:** ['conditional expressions precedence']  
**Answer:** Conditional expressions have the lowest precedence of all Python operations. This means that when an expression contains multiple operators, conditional expressions will be evaluated last, after all other operators have been processed [p0119:c02].  
> [p0119:c02] p.119: Conditional expression template: expression_if_true if condition else expression_if_false A conditional expression is evaluated by first checking the condition. If condition is true, expression_if_true is evaluated, and the result is the resulting value of the conditional expression. Else, expression_if_false is evaluated, and the result is the resulting value of the conditional expression. A variable can be assigned with a conditional expression. Ex: Finding the max of two numbers can be calcul

## q09 — answerable — status: answered
**Q:** In a counting while loop, what happens when the step size is negative?  
**Expected:** The counter counts in descending order (positive step counts ascending).  
**Queries:** ['counting while loop negative step size']  
**Answer:** In a counting while loop, if the step size is negative, the counter counts in descending order. This means that the loop will decrease the counter's value with each iteration, allowing it to iterate through a sequence of values in reverse. Conversely, if the step size is positive, the counter counts in ascending order [p0127:c00].  
> [p0127:c00] p.127: determine the number of iterations executed. Ex: A programmer may want to print all even numbers between 1 and 20. The task can be done by using a counter initialized with 1. In each iteration, the counter's value is increased by one, and a condition can check whether the counter's value is an even number or not. The change in the counter's value in each iteration is called the step size. The step size can be any positive or negative value. If the step size is a positive number, the counter coun

## q10 — answerable — status: answered
**Q:** Is the end value included in the sequence produced by range()?  
**Expected:** No. The sequence is inclusive of the start and exclusive of the end.  
**Queries:** ['range() end value']  
**Answer:** The end value is exclusive in the sequence produced by the range() function. It generates a sequence of integers that includes the start value but excludes the end value [p0130:c00].  
> [p0130:c00] p.130: a. A string* b. A*s*t*r*i*n*g* c. A* *s*t*r*i*n*g* Range() function in for loop A for loop can be used for iteration and counting. The range() function is a common approach for implementing counting in a for loop. A range() function generates a sequence of integers between the two numbers given a step size. This integer sequence is inclusive of the start and exclusive of the end of the sequence. The range() function can take up to three input values. Examples are provided in the table below. Ran

## q11 — answerable — status: answered
**Q:** When should I prefer a for loop over a while loop, including in nested loops?  
**Expected:** When counting with range() or iterating over a container object, including nested situations.  
**Queries:** ['for loop vs while loop', 'when to use for loop']  
**Answer:** You should prefer a for loop over a while loop when you need to iterate over elements of a container object or when counting using a range function. For loops are particularly useful in nested situations, such as iterating over multiple lists or collections, where the outer loop iterates over one collection and the inner loop iterates over another. This makes for loops more concise and easier to read in such contexts [p0135:c00].

In contrast, while loops are better suited for situations where the number of iterations is not predetermined and depends on a condition that may change during execution. They run a set of statements while a given condition is true [p0125:c03]. 

Thus, for loops are generally preferred for counting and iterating over known collections, while while loops are used for conditions that may vary [p0144:c00]. 

In summary, use:
- **For loops**: when iterating over containers or counting with a range.
- **While loops**: when the number of iterations is not known beforehand and depends on a condition.  
> [p0135:c00] p.135: j += 1 i += 1 Nested for loops A nested for loop can be implemented and used in the same way as a nested while loop. A for loop is a preferable option in cases where a loop is used for counting purposes using a range() function, or when iterating over a container object, including nested situations. Ex: Iterating over multiple course rosters. The outer loop iterates over different courses, and the inner loop iterates over the names in each course roster.
> [p0125:c03] p.125: 5.1 While loop Learning objectives By the end of this section you should be able to • Explain the loop construct in Python. • Use a while loop to implement repeating tasks. While loop A while loop is a code construct that runs a set of statements, known as the loop body, while a given condition, known as the loop expression, is true. At each iteration, once the loop statement is executed, the
> [p0144:c00] p.144: Function Description Loop constructs Description while loop # initialization while expression: # loop body # statements after the loop for loop # initialization for loop_variable in container: # loop body # statements after the loop Nested while loop while outer_loop_expression:

## q12 — answerable — status: answered
**Q:** What is a loop without a termination condition called, and what statement is essential to leave it?  
**Expected:** An infinite loop; a break statement is essential to exit it.  
**Queries:** ['loop without a termination condition']  
**Answer:** A loop without a termination condition is called an infinite loop. A break statement is essential to leave it [p0138:c00].  
> [p0138:c00] p.138: INFINITE LOOP A break statement is an essential part of a loop that does not have a termination condition. A loop without a termination condition is known as an infinite loop. Ex: An infinite loop that counts up starting from 1 and prints the counter's value while the counter's value is less than 10. A break condition is triggered when the counter's value is equal to 10, and hence the program execution exits.

## q13 — answerable — status: answered
**Q:** What does a continue statement do inside a loop?  
**Expected:** It skips the remainder of the current loop iteration without exiting the loop entirely.  
**Queries:** ['continue statement loop']  
**Answer:** A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. After the continue statement's execution, the loop expression will be evaluated again, and the loop will continue from the loop's expression. This facilitates the loop's control and readability [p0139:c00][p0143:c02].  
> [p0139:c00] p.139: i = 1 count = 0 while True: if i%2 == 0 or i%3 == 0: count += 1 if count >= 5: print(i) break i += 1 a. 5 b. 8 c. 30 Continue A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. A continue statement can be used in a for or a while loop. After the continue statement's execution, the loop expression will be evaluated again and the loop will continue from the loop's expression. A continue statement facilitates the loop's control and
> [p0143:c02] p.143: • A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. • A loop else statement runs after the loop's execution is completed without being interrupted by a break statement.

## q14 — answerable — status: answered
**Q:** Why do functions make code reusable?  
**Expected:** The function body can be executed repeatedly with multiple function calls.  
**Queries:** ['functions reusable']  
**Answer:** Functions make code reusable because they promote modularity by grouping related code statements into a single unit. This allows the body of a function to be executed multiple times through function calls, enabling the same block of code to be used repeatedly without rewriting it. Consequently, modular and reusable code is easier to modify and share among programmers, which helps avoid redundancy in coding efforts [p0149:c03]. Additionally, functions allow programmers to write a block of code once, name it, and call it as needed, which enhances efficiency and organization in programming [p0147:c01].  
> [p0149:c03] p.149: a. print_pc_specs b. print_pc_specs() c. print_pc_specs(): 7 . Which is an appropriate name for a function that calculates a user's taxes? a. calc_tax b. calculate user tax c. c_t Benefits of functions A function promotes modularity by putting code statements related to a single task in a separate group. The body of a function can be executed repeatedly with multiple function calls, so a function promotes reusability. Modular, reusable code is easier to modify and is shareable among programmers 
> [p0147:c01] p.147: 6.7 Chapter summary Introduction Functions are the next step toward creating optimized code as a software developer. If the same block of code is reused repeatedly, a function allows the programmer to write the block of code once, name the block, and use the code as many times as needed by calling the block by name. Functions can read in values and return values to perform tasks, including complex calculations.

## q15 — answerable — status: answered
**Q:** Can a variable created inside a function be used after the function finishes?  
**Expected:** No. It has local scope, only exists within the function, and no longer exists after the function finishes executing.  
**Queries:** ['variable scope function']  
**Answer:** A variable created inside a function has local scope and only exists within that function. Therefore, it cannot be accessed after the function finishes executing, as the local variables no longer exist after the function completes [p0156:c01].  
> [p0156:c01] p.156: Local scope A variable created within a function has local scope and only exists within the function. A local variable cannot be accessed outside of the function in which the variable was created. After a function finishes executing, the function's local variables no longer exist.

## q16 — answerable — status: answered
**Q:** What must a function do before it can edit a global variable?  
**Expected:** Declare the variable with the global keyword.  
**Queries:** ['function edit global variable']  
**Answer:** Before a function can edit a global variable, the variable must be declared with the global keyword. This is necessary because, by default, a function treats any variable it edits as a local variable unless specified otherwise [p0157:c02].  
> [p0157:c02] p.157: b. print_time() c. print_greeting() and print_time() Using local and global variables together Python allows global and local variables to have the same name, which can lead to unexpected program behavior. A function treats a variable edited within the function as a local variable unless told otherwise. To edit a global variable inside a function, the variable must be declared with the global keyword. CHECKPOINT Editing global variables in a program with a function Editing global variables in a 

## q17 — answerable — status: answered
**Q:** What does PEP 8 recommend about spaces around the = sign?  
**Expected:** No spaces around = when indicating keyword arguments and default parameter values.  
**Queries:** ['PEP 8 spaces around = sign']  
**Answer:** PEP 8 recommends no spaces around the = sign when indicating keyword arguments and default parameter values [p0171:c00].  
> [p0171:c00] p.171: PEP 8 RECOMMENDATIONS: SPACING The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default parameter values. Stream donations Write a function, donate(), that lets an online viewer send a donation to a streamer. donate() has three parameters:

## q18 — answerable — status: answered
**Q:** What is a branch?  
**Expected:** A group of statements that execute based on a condition.  
**Queries:** ['branch']  
**Answer:** A branch is a group of statements that execute based on a condition. The Python interpreter follows a single path of execution when executing a program, but a branch allows for multiple possible paths based on conditions defined by the programmer [p0095:c01].  
> [p0095:c01] p.95: 4.6 Nested decisions 4.7 Conditional expressions 4.8 Chapter summary Introduction The Python interpreter follows a single path of execution when executing a program. What if a programmer wants to define multiple possible paths? Ex: Instead of always taking the left path, a program uses the path width to decide which path to take. If the left path is wider, take the right path. Else, take the left path. A branch is a group of statements that execute based on a condition. The Expressions chapter i

## q19 — answerable — status: answered
**Q:** In a nested loop, what does the outer loop control?  
**Expected:** The number of the inner loop's full executions.  
**Queries:** ['nested loop outer loop control']  
**Answer:** In a nested loop, the outer loop controls the number of times the inner loop is fully executed. This means that for each iteration of the outer loop, the inner loop will run completely before the outer loop proceeds to its next iteration [p0132:c03].  
> [p0132:c03] p.132: 5.3 Nested loops Learning objectives By the end of this section you should be able to • Implement nested while loops. • Implement nested for loops. Nested loops A nested loop has one or more loops within the body of another loop. The two loops are referred to as outer loop and inner loop. The outer loop controls the number of the inner loop's full execution. More than one inner loop can exist in a nested loop.

## t01 — answerable — status: answered
**Q:** What value does a function return if it has no return statement?  
**Expected:** None, representing no value.  
**Queries:** ['function return value no return statement']  
**Answer:** If a function has no return statement, it returns None, which represents no value [p0165:c00].  
> [p0165:c00] p.165: finishes the function execution and can specify a value to return to the function's caller. Functions introduced so far have not had a return statement, which is the same as returning None, representing no value.

## t02 — answerable — status: answered
**Q:** Why shouldn't a list be used as a default parameter value?  
**Expected:** Default values are defined only once for the function, so mutable objects such as lists should not be used.  
**Queries:** ['list default parameter value']  
**Answer:** A list should not be used as a default parameter value because default parameter values are only defined once when the function is defined. This means that if a mutable object like a list is used as a default value, any modifications to that list will persist across subsequent calls to the function, leading to unexpected behavior. This is why mutable objects should be avoided as default parameter values [p0170:c00].  
> [p0170:c00] p.170: a. greeting("Morning", "Morgan", count=3) b. greeting(count=1,"Hi", "Bea") c. greeting("Cheers", "Colleagues", 10) Default parameter values Functions can define default parameter values to use if a positional or keyword argument is not provided for the parameter. Ex: def season(m, d, hemi="N"): defines a default value of "N" for the hemi parameter. Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as lists) should not be used as default val

## t03 — answerable — status: answered
**Q:** If a function changes a list argument, does the caller see the change? What about a string argument?  
**Expected:** Yes for a list (mutable: changes appear outside the function); no for a string (immutable: the function changes a local copy).  
**Queries:** ['function changes list argument', 'function changes string argument']  
**Answer:** If a function changes a list argument, the caller sees the change because lists are mutable objects in Python. This means that modifications to the list within the function will reflect outside the function as well. On the other hand, if a function changes a string argument, the caller does not see the change because strings are immutable. Therefore, any modifications made to a string within the function do not affect the original string outside the function [p0162:c02][p0163:c01].  
> [p0162:c02] p.162: a. 2 b. 4 c. 3 d. 6 e. Error Modifying arguments and mutability In Python, a variable is a name that refers to an object stored in memory, aka an object reference, so Python uses a pass-by-object-reference system. If an argument is changed in a function, the changes are kept or lost depending on the object's mutability. A mutable object can be modified after creation. A function's changes to the object then appear outside the function. An immutable object cannot be modified after creation. So a 
> [p0163:c01] p.163: for temp in wknd_temps: print(f"{temp:.2f}{deg_sign}{metric}", end=" ") The output is 9.44°F 10.56°F 6.67°F. type was changed to "C" in the function but didn't keep the change outside of the function. Why is the list argument change kept and not the string argument change? (Hint: A list is mutable. A string is immutable.)

## t04 — answerable — status: answered
**Q:** When does the else block run?  
**Expected:** (Loops chapter) A loop else runs after the loop completes without being interrupted by a break statement.  
**Queries:** ['else block']  
**Answer:** The else block runs after the loop's execution is completed without being interrupted by a break statement. If the loop is terminated normally (i.e., it completes all iterations without hitting a break), the else block will execute. For example, if a loop is searching for a value and does not find it, the else block will run to indicate that the value was not found [p0141:c00][p0143:c02].  
> [p0141:c00] p.141: statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement. Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If 10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else statement will run and print "10 i
> [p0143:c02] p.143: • A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. • A loop else statement runs after the loop's execution is completed without being interrupted by a break statement.

## t05 — answerable — status: answered
**Q:** When a call mixes positional and keyword arguments, which must come first?  
**Expected:** Positional arguments, in the correct order, before any keyword arguments.  
**Queries:** ['positional and keyword arguments']  
**Answer:** When mixing positional and keyword arguments in a function call, positional arguments must come first, before any keyword arguments [p0169:c01].  
> [p0169:c01] p.169: Keyword arguments So far, functions have been called using positional arguments, which are arguments that are assigned to parameters in order. Python also allows keyword arguments, which are arguments that use parameter names to assign values rather than order. When mixing positional and keyword arguments, positional arguments must come first in the correct order, before any keyword arguments.

## t06 — answerable — status: answered
**Q:** What does elif stand for and where must it be placed?  
**Expected:** Else if; it is part of a chain and must follow an if (or elif) statement.  
**Queries:** ['elif']  
**Answer:** Elif stands for 'else if' and is used to check a condition when the prior decision statement's condition is false. An elif statement must follow an if (or another elif) statement in a chain of decision statements [p0111:c03].  
> [p0111:c03] p.111: score = int(input()) if score < 70: score += 10 # Wrong: if 70 <= score < 85: score += 5 Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short for else if) statement checks a condition when the prior decision statement's condition is false. An elif statement is part of a chain and must follow an if (or elif) statement. if-elif statement template: # Statements before if condition: # Body elif condition: # Body # Statements after

## u01 — UNANSWERABLE — status: abstain
**Q:** How do I write a lambda (anonymous) function in Python?  
**Expected:** Corpus = chapters 4-6 only; 'lambda' never occurs. 'anonymous' only occurs as a string default value "Anonymous" (p.170).  
**Queries:** ['lambda function', 'anonymous function']  
**Answer:** The passages do not cover how to write a lambda (anonymous) function in Python.  

## u02 — UNANSWERABLE — status: abstain
**Q:** How does a try/except block handle a ZeroDivisionError?  
**Expected:** No 'try', 'except' or 'ZeroDivision' token in the corpus; calc_mpg avoids division by zero with an if, not exceptions.  
**Queries:** ['try except ZeroDivisionError', 'try except']  
**Answer:** The passages do not cover how a try/except block handles a ZeroDivisionError.  

## u03 — UNANSWERABLE — status: abstain
**Q:** What is the base case of a recursive function?  
**Expected:** No 'recursion'/'recursive'/'base case' in chapters 4-6 (recursion is a later chapter, not indexed).  
**Queries:** ['base case recursive function', 'recursive function base case']  
**Answer:** The passages do not cover the concept of a base case in a recursive function.  
