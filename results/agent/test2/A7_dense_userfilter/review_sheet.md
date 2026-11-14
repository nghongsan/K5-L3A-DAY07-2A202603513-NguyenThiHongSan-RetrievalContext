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
**Queries:** ['nested loops for while', 'combining for loops and while loops']  
**Answer:** Yes, for loops and while loops can be combined inside one nested loop. The two constructs can be mixed, where, for example, the outer loop can be a for loop iterating over a list, and the inner loop can be a while loop iterating over a range of values. This allows for flexibility in how iterations are handled within the nested structure [p0136:c00].  
> [p0136:c00] p.136: b. for i in range(1, 4): for j in range(4): print(i * j) c. for i in range(1, 4): for j in range(4): print(i * j, end = ' ') print() MIXED LOOPS The two for and while loop constructs can also be mixed in a nested loop construct. Ex: Printing even numbers less than a given number in a list. The outer loop can be implemented using a for loop iterating over the provided list, and the inner loop iterates over all even numbers less than a given number from the list using a while loop.

## m03 — answerable — status: answered
**Q:** What happens when a function finishes executing?  
**Expected:** The function returns and provides a result to the calling code.  
**Queries:** ['function finishes executing']  
**Answer:** When a function finishes executing, it can specify a value to return to the function's caller using a return statement. If there is no return statement, the function returns None, indicating no value. Additionally, when a function called from another function finishes execution, control flow returns to the calling function [p0165:c00].  
> [p0165:c00] p.165: finishes the function execution and can specify a value to return to the function's caller. Functions introduced so far have not had a return statement, which is the same as returning None, representing no value.

## m04 — answerable — status: answered
**Q:** For printing every multiple of 5 below 50, how does a for loop with range() compare with an equivalent while loop?  
**Expected:** The for loop with range(0, 50, 5) is more compact than the while loop implementation (which needs initialization and an explicit increment).  
**Queries:** ['for loop range printing multiples of 5', 'while loop printing multiples of 5']  
**Answer:** A for loop using the `range()` function is more compact and straightforward for printing multiples of 5 below 50 compared to a while loop. The for loop can be written as:

```python
for i in range(0, 50, 5):
    print(i)
```

This approach directly specifies the start, stop, and step values in the `range()` function, making it concise [p0131:c00].

In contrast, the equivalent while loop requires more lines of code for initialization and incrementing the counter:

```python
i = 0
while i < 50:
    print(i)
    i += 5
```

This implementation is longer and involves manual management of the loop variable [p0131:c01]. Thus, the for loop is generally preferred for such tasks due to its simplicity and clarity.  
> [p0131:c00] p.131: EXAMPLE 5.2 Two programs printing all integer multiples of 5 less than 50 (Notice the compactness of the for construction compared to the while) # For loop condition using # range() function to print # all multiples of 5 less than 50 for i in range(0, 50, 5):
> [p0131:c01] p.131: print(i) # While loop implementation of printing # multiples of 5 less than 50 # Initialization i = 0 # Limiting the range to be less than 50 while i < 50: print(i) i+=5 Table 5.2 CONCEPTS IN PRACTICE For loop using a range() function 4 . What are the arguments to the range() function for the increasing sequence of every 3rd integer from 10 to 22 (inclusive of both ends)?

## m05 — answerable — status: answered
**Q:** In the loop-else example that searches a list for the number 10, what happens if 10 is not in the list?  
**Expected:** The loop terminates after evaluating all integers, so the else statement runs and prints "10 is not in the list."  
**Queries:** ['loop-else example searches list for number 10']  
**Answer:** If the number 10 is not in the list, the loop will terminate after evaluating all integers in the list, and the else statement will execute, printing "10 is not in the list." Alternatively, a Boolean variable can be used to track whether the number 10 was found, and if it remains false after the loop, it will also print "10 is not in the list." [p0141:c01].  
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
**Answer:** The passages retrieved do not contain information on how to write a dictionary comprehension in Python.  

## v02 — UNANSWERABLE — status: abstain
**Q:** How can the walrus operator := be used in a while loop condition?  
**Expected:** No ':=' or 'walrus' in the corpus.  
**Queries:** ['walrus operator := while loop', 'walrus operator']  
**Answer:** The passages do not cover the use of the walrus operator := in a while loop condition.  
