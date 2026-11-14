# Review sheet (grade manually; gold shown for the reviewer only)

## m01 — answerable — status: answered
**Q:** What does the not operator return?  
**Expected:** It takes one condition operand and returns True when the operand is false and False when the operand is true.  
**Queries:** ['not operator']  
**Answer:** The not operator takes one condition operand and returns True when the operand is false and returns False when the operand is true. It is useful for making conditions more readable and can toggle a Boolean's value. For example, if a variable is_on is True, using not is_on would return False, and vice versa [p0106:c02].  
> [p0106:c02] p.106: 7 . Given a = 9 and b = 10, does the test pass? if (a%2 == 0 and b%2 == 1) or (a%2 == 1 and b%2 == 0): # Test passed else: # Test failed a. yes b. no Logical operator: not If the computer is not on, press the power button. The not operator takes one condition operand and returns True when the operand is false and returns False when the operand is true. not is a useful operator that can make a condition more readable and can be used to toggle a Boolean's value. Ex: is_on = not is_on.

## m02 — answerable — status: answered
**Q:** Can for loops and while loops be combined inside one nested loop?  
**Expected:** Yes. The for and while constructs can be mixed in a nested loop construct (e.g. an outer for loop over a list with an inner while loop).  
**Queries:** ['nested loops']  
**Answer:** Yes, for loops and while loops can be combined inside one nested loop. This is referred to as mixed loops, where the outer loop can be a for loop and the inner loop can be a while loop, or vice versa. An example provided is using a for loop to iterate over a list while the inner while loop iterates over all even numbers less than a given number from that list [p0136:c00].  
> [p0136:c00] p.136: b. for i in range(1, 4): for j in range(4): print(i * j) c. for i in range(1, 4): for j in range(4): print(i * j, end = ' ') print() MIXED LOOPS The two for and while loop constructs can also be mixed in a nested loop construct. Ex: Printing even numbers less than a given number in a list. The outer loop can be implemented using a for loop iterating over the provided list, and the inner loop iterates over all even numbers less than a given number from the list using a while loop.

## m03 — answerable — status: answered
**Q:** What happens when a function finishes executing?  
**Expected:** The function returns and provides a result to the calling code.  
**Queries:** ['function finishes executing']  
**Answer:** When a function finishes executing, it can specify a value to return to the function's caller. If there is no return statement, it implicitly returns None, indicating no value. Additionally, when a function called from another function finishes execution, control flow returns to the calling function, allowing the program to continue from where it left off in the caller function's execution context. [p0165:c00][p0153:c00]  
> [p0165:c00] p.165: finishes the function execution and can specify a value to return to the function's caller. Functions introduced so far have not had a return statement, which is the same as returning None, representing no value.
> [p0153:c00] p.153: b. 8 c. 12 4 . What is the output? def park_greet(): """Output greeting.""" print("Welcome to the park") print("Open sunrise to sunset") park_greet() a. Welcome to the park b. Welcome to the park Open sunrise to sunset c. Open sunrise to sunset Welcome to the park Functions calling functions Functions frequently call other functions to keep the modularity of each function performing one task. Ex: A function that calculates an order total may call a function that calculates sales tax. When a func

## m04 — answerable — status: abstain
**Q:** For printing every multiple of 5 below 50, how does a for loop with range() compare with an equivalent while loop?  
**Expected:** The for loop with range(0, 50, 5) is more compact than the while loop implementation (which needs initialization and an explicit increment).  
**Queries:** ['for loop range', 'while loop']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** A for loop using the `range()` function is generally more concise and easier to read for counting iterations, such as printing multiples of 5 below 50. The `range()` function generates a sequence of integers, making it straightforward to specify the start, stop, and step values for the loop. For example, `for i in range(0, 50, 5): print(i)` directly iterates through the multiples of 5.

In contrast, a while loop requires manual initialization and updating of the loop variable, which can lead to more verbose code. For instance, you would need to initialize a variable (e.g., `i = 0`), check the condition (`while i < 50:`), and increment it within the loop (`i += 5`). This can introduce potential errors if the increment is forgotten or incorrectly implemented. Thus, while both loops can achieve the same result, the for loop with `range()` is often preferred for its simplicity and clarity in counting scenarios [p0130:c00][p0125:c01].  

## m05 — answerable — status: answered
**Q:** In the loop-else example that searches a list for the number 10, what happens if 10 is not in the list?  
**Expected:** The loop terminates after evaluating all integers, so the else statement runs and prints "10 is not in the list."  
**Queries:** ['loop else example searches list for number 10']  
**Answer:** If the number 10 is not in the list, the loop will terminate after evaluating all integers in the list, and the else statement will execute, printing "10 is not in the list." Alternatively, a Boolean variable can be used to track whether the number 10 was found, and if it remains false after the loop, it will also print "10 is not in the list." [p0141:c00]  
> [p0141:c00] p.141: statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement. Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If 10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else statement will run and print "10 i

## m06 — answerable — status: answered
**Q:** How does the textbook define a function?  
**Expected:** A function is a named, reusable block of code that performs a task when called.  
**Queries:** ['define a function', 'what is a function']  
**Answer:** A function is defined as a named, reusable block of code that performs a task when called. Functions allow programmers to write a block of code once, name it, and use it multiple times by calling it by name. They can also read in values and return values to perform tasks, including complex calculations, thus making programs more organized and optimized [p0148:c00][p0171:c02].  
> [p0148:c00] p.148: Calling a function Throughout the book, functions have been called to perform tasks. Ex: print() prints values, and sqrt() calculates the square root. A function is a named, reusable block of code that performs a task when called.
> [p0171:c02] p.171: 6.7 Chapter summary Highlights from this chapter include: • Functions are named blocks of code that perform tasks when called and make programs more organized and optimized. • Control flow is the sequence of program execution. Control flow moves between calling code and function code when a function is called.

## v01 — UNANSWERABLE — status: abstain
**Q:** How do I write a dictionary comprehension in Python?  
**Expected:** No 'comprehension' or 'dictionary' token in chapters 4-6.  
**Queries:** ['dictionary comprehension', 'dictionary comprehension']  
**Answer:** The passages do not cover how to write a dictionary comprehension in Python.  

## v02 — UNANSWERABLE — status: abstain
**Q:** How can the walrus operator := be used in a while loop condition?  
**Expected:** No ':=' or 'walrus' in the corpus.  
**Queries:** ['walrus operator := while loop', 'walrus operator']  
**Answer:** The passages do not cover the use of the walrus operator := in a while loop condition specifically. Therefore, I cannot provide an answer based on the textbook content.  
