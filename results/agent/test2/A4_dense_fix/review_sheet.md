# Review sheet (grade manually; gold shown for the reviewer only)

## m01 — answerable — status: answered
**Q:** What does the not operator return?  
**Expected:** It takes one condition operand and returns True when the operand is false and False when the operand is true.  
**Queries:** ['not operator']  
**Answer:** The not operator takes one condition operand and returns True when the operand is false and returns False when the operand is true. It is useful for making conditions more readable and can toggle a Boolean's value [p0106:c02].  
> [p0106:c02] p.106: 7 . Given a = 9 and b = 10, does the test pass? if (a%2 == 0 and b%2 == 1) or (a%2 == 1 and b%2 == 0): # Test passed else: # Test failed a. yes b. no Logical operator: not If the computer is not on, press the power button. The not operator takes one condition operand and returns True when the operand is false and returns False when the operand is true. not is a useful operator that can make a condition more readable and can be used to toggle a Boolean's value. Ex: is_on = not is_on.

## m02 — answerable — status: answered
**Q:** Can for loops and while loops be combined inside one nested loop?  
**Expected:** Yes. The for and while constructs can be mixed in a nested loop construct (e.g. an outer for loop over a list with an inner while loop).  
**Queries:** ['nested loops']  
**Answer:** Yes, for loops and while loops can be combined inside one nested loop. The two loop constructs can be mixed in a nested loop construct, where, for example, the outer loop can be a for loop and the inner loop can be a while loop. An example provided is printing even numbers less than a given number in a list, where the outer loop iterates over the list and the inner loop iterates over all even numbers using a while loop [p0136:c00].  
> [p0136:c00] p.136: b. for i in range(1, 4): for j in range(4): print(i * j) c. for i in range(1, 4): for j in range(4): print(i * j, end = ' ') print() MIXED LOOPS The two for and while loop constructs can also be mixed in a nested loop construct. Ex: Printing even numbers less than a given number in a list. The outer loop can be implemented using a for loop iterating over the provided list, and the inner loop iterates over all even numbers less than a given number from the list using a while loop.

## m03 — answerable — status: answered
**Q:** What happens when a function finishes executing?  
**Expected:** The function returns and provides a result to the calling code.  
**Queries:** ['function finishes executing', 'what happens when a function finishes executing']  
**Answer:** When a function finishes executing, control flow returns to the function's caller. If the function has a return statement, it can specify a value to return; if there is no return statement, it implicitly returns None, indicating no value is returned. Control flow then continues from the point where the function was called [p0165:c00][p0151:c04]. Thus, the execution sequence is organized such that the program can move back and forth between the calling code and the function code as needed [p0171:c02].  
> [p0165:c00] p.165: finishes the function execution and can specify a value to return to the function's caller. Functions introduced so far have not had a return statement, which is the same as returning None, representing no value.
> [p0151:c04] p.151: Control flow and functions Control flow is the sequence of program execution. A program's control flow begins at the main program but rarely follows a strict sequence. Ex: Control flow skips over lines when a conditional statement isn't executed. When execution reaches a function call, control flow moves to where the function is defined and executes the function statements. Then, control flow moves back to where the function was called and continues the sequence. CHECKPOINT Calling a brunch menu
> [p0171:c02] p.171: 6.7 Chapter summary Highlights from this chapter include: • Functions are named blocks of code that perform tasks when called and make programs more organized and optimized. • Control flow is the sequence of program execution. Control flow moves between calling code and function code when a function is called.

## m04 — answerable — status: answered
**Q:** For printing every multiple of 5 below 50, how does a for loop with range() compare with an equivalent while loop?  
**Expected:** The for loop with range(0, 50, 5) is more compact than the while loop implementation (which needs initialization and an explicit increment).  
**Queries:** ['for loop range', 'while loop']  
**Answer:** A for loop using the range() function is generally more concise and preferable for counting iterations, such as printing multiples of 5 below 50. The range() function generates a sequence of integers, making it straightforward to specify the start, end, and step size [p0130:c00]. In contrast, a while loop requires manual initialization and updating of the loop variable, which can lead to more complex code and potential errors if the loop condition is not managed correctly [p0125:c03]. Therefore, for counting tasks, a for loop is often the better choice due to its simplicity and clarity.  
> [p0130:c00] p.130: a. A string* b. A*s*t*r*i*n*g* c. A* *s*t*r*i*n*g* Range() function in for loop A for loop can be used for iteration and counting. The range() function is a common approach for implementing counting in a for loop. A range() function generates a sequence of integers between the two numbers given a step size. This integer sequence is inclusive of the start and exclusive of the end of the sequence. The range() function can take up to three input values. Examples are provided in the table below. Ran
> [p0125:c03] p.125: 5.1 While loop Learning objectives By the end of this section you should be able to • Explain the loop construct in Python. • Use a while loop to implement repeating tasks. While loop A while loop is a code construct that runs a set of statements, known as the loop body, while a given condition, known as the loop expression, is true. At each iteration, once the loop statement is executed, the

## m05 — answerable — status: answered
**Q:** In the loop-else example that searches a list for the number 10, what happens if 10 is not in the list?  
**Expected:** The loop terminates after evaluating all integers, so the else statement runs and prints "10 is not in the list."  
**Queries:** ['loop else example searches list for number 10']  
**Answer:** If the number 10 is not in the list, the loop will terminate after evaluating all integers in the list, and the else statement will execute, printing "10 is not in the list." Alternatively, a Boolean variable can be used to track whether the number 10 was found, and if it remains false after the loop, it will also print "10 is not in the list." [p0141:c00][p0141:c01].  
> [p0141:c00] p.141: statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement. Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If 10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else statement will run and print "10 i
> [p0141:c01] p.141: EXAMPLE 5.4 Finding the number 10 in a list In the code examples below, the code on the left prints "Found 10!" if the variable i's value is 10. If the value 10 is not in the list, the code prints "10 is not in the list.". The code on the right uses the seen Boolean variable to track if the value 10 is in the list. After loop's execution, if seen's value is still false, the code prints "10 is not in the list.".

## m06 — answerable — status: answered
**Q:** How does the textbook define a function?  
**Expected:** A function is a named, reusable block of code that performs a task when called.  
**Queries:** ['define a function']  
**Answer:** A function is defined as a named, reusable block of code that performs a task when called. It allows the programmer to write a block of code once, name it, and use it multiple times by calling it by name. Functions can also read in values and return values to perform tasks, including complex calculations. [p0148:c00]  
> [p0148:c00] p.148: Calling a function Throughout the book, functions have been called to perform tasks. Ex: print() prints values, and sqrt() calculates the square root. A function is a named, reusable block of code that performs a task when called.

## v01 — UNANSWERABLE — status: abstain
**Q:** How do I write a dictionary comprehension in Python?  
**Expected:** No 'comprehension' or 'dictionary' token in chapters 4-6.  
**Queries:** ['dictionary comprehension', 'comprehension']  
**Answer:** The passages do not cover how to write a dictionary comprehension in Python.  

## v02 — UNANSWERABLE — status: abstain
**Q:** How can the walrus operator := be used in a while loop condition?  
**Expected:** No ':=' or 'walrus' in the corpus.  
**Queries:** ['walrus operator := while loop', 'walrus operator']  
**Answer:** The passages do not cover the use of the walrus operator := in a while loop condition.  
