# Review sheet (grade manually; gold shown for the reviewer only)

## q01 — answerable — status: abstain
**Q:** Which values does bool() convert to False?  
**Expected:** 0 and the empty string (any non-zero number or non-empty string becomes True).  
**Queries:** ['bool() convert to False', 'boolean values that evaluate to False', 'values that evaluate to False']  
**Answer:** The values that bool() converts to False include: 0 (zero), empty sequences (like '', [], or ()), and None. These are considered "falsy" values in Python, meaning they evaluate to False in a Boolean context. However, the textbook passages do not explicitly list these values.  

## q02 — answerable — status: abstain
**Q:** What goes wrong if I write is_zero = num=0 when I meant to test whether num is zero?  
**Expected:** It assigns 0 to both is_zero and num regardless of num's original value; = is assignment, == is comparison.  
**Queries:** ['is_zero = num=0']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** If you write `is_zero = num=0`, it will always assign both `is_zero` and `num` the value of 0, regardless of what `num` was originally. This is because the `=` operator is used for assignment, not comparison. To test whether `num` is zero, you should use `is_zero = (num == 0)`, which uses the `==` operator for comparison and will correctly evaluate to `True` or `False` without modifying `num`'s value. This common mistake can lead to unintended behavior in your code.  

## q03 — answerable — status: abstain
**Q:** How many spaces per indentation level does the PEP 8 style guide recommend?  
**Expected:** Four spaces per indentation level.  
**Queries:** ['PEP 8 indentation spaces']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** The PEP 8 style guide recommends four spaces per indentation level.  

## q04 — answerable — status: abstain
**Q:** When an if-else statement runs, can both the if body and the else body execute?  
**Expected:** No. One and only one of the branches is taken.  
**Queries:** ['if-else statement execution']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** No, when an if-else statement runs, only one of the branches (either the if body or the else body) is executed, not both. This means that if the condition of the if statement is true, the if body executes, and if the condition is false, the else body executes. Therefore, both bodies cannot execute simultaneously.  

## q05 — answerable — status: answered
**Q:** Which operator is the main exception to left associativity, and how is 2 ** 3 ** 4 evaluated?  
**Expected:** Exponentiation is right associative, so 2 ** 3 ** 4 is evaluated as 2 ** (3**4).  
**Queries:** ['operator exception to left associativity', '2 ** 3 ** 4 evaluation']  
**Answer:** The main exception to left associativity is the exponentiation operator (**), which is right associative. This means that expressions like 2 ** 3 ** 4 are evaluated from right to left, specifically as 2 ** (3 ** 4) rather than (2 ** 3) ** 4. Therefore, 3 ** 4 is evaluated first, followed by 2 raised to that result.  

This evaluation order is confirmed in the textbook: "Exponentiation is the main exception... and is right associative: that is, evaluated from right to left. Ex: 2 ** 3 ** 4 is evaluated as 2 ** (3**4)." [p0109:c00]  
> [p0109:c00] p.109: 1 . x ** 2 + 6 / 3 a. 6 / 3 b. x ** 2 c. 2 + 6 2 . not 3 * 5 > 10 a. 3 * 5 b. not 3 c. 5 > 10 3 . z == 5 and x / 8 < 100 a. 5 and x b. x / 8 c. 8 < 100 Associativity What if operators beside each other have the same level of precedence? Associativity determines the order of operations when precedence is the same. Ex: 8 / 4 * 3 is evaluated as (8/4) * 3 rather than 8 / (4*3) because multiplication and division are left associative. Most operators are left associative and are evaluated from left t

## q06 — answerable — status: answered
**Q:** How does Python evaluate a chained comparison such as 10 < x <= 20?  
**Expected:** As 10 < x and x <= 20, evaluated from left to right.  
**Queries:** ['chained comparison']  
**Answer:** In Python, a chained comparison like `10 < x <= 20` is evaluated as two separate comparisons: `10 < x` and `x <= 20`. The expression is processed from left to right, meaning both conditions must be true for the entire expression to evaluate as true. This is equivalent to writing `10 < x and x <= 20` [p0109:c01].  
> [p0109:c01] p.109: When comparison operators are chained, the expression is converted into the equivalent combination of comparisons and evaluated from left to right. Ex. 10 < x <= 20 is evaluated as 10 < x and x <= 20.

## q07 — answerable — status: answered
**Q:** Why can two separate if statements give a student a double grade curve, and what fixes it?  
**Expected:** Separate if statements do not guarantee only one branch is taken, so both can execute; chaining with elif fixes it.  
**Queries:** ['two separate if statements double grade curve']  
**Answer:** Two separate if statements can lead to a double grade curve because both conditions can be true independently, causing both branches to execute. For example, if a student's score is 60, the first if statement might add 10 points, and the second if statement could add another 5 points, resulting in an incorrect total score of 75. To fix this issue, chaining decision statements using elif ensures that only one branch is executed based on the conditions, preventing multiple adjustments to the score from occurring simultaneously. This way, if the first condition is met, the subsequent conditions are not evaluated, thus avoiding the double grading issue. [p0111:c02][p0111:c03]  
> [p0111:c02] p.111: elif Sometimes, a complicated decision is based on more than a single condition. Ex: A travel planning site reviews the layovers on an itinerary. If a layover is greater than 24 hours, the site should suggest accommodations. Else if the layover is less than one hour, the site should alert for a possible missed connection. Two separate if statements do not guarantee that only one branch is taken and might result in both branches being taken. Ex: The program below attempts to add a curve based on 
> [p0111:c03] p.111: score = int(input()) if score < 70: score += 10 # Wrong: if 70 <= score < 85: score += 5 Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short for else if) statement checks a condition when the prior decision statement's condition is false. An elif statement is part of a chain and must follow an if (or elif) statement. if-elif statement template: # Statements before if condition: # Body elif condition: # Body # Statements after

## q08 — answerable — status: abstain
**Q:** What precedence do conditional expressions have compared with other Python operations?  
**Expected:** The lowest precedence of all Python operations.  
**Queries:** ['conditional expressions precedence']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** Conditional expressions have the lowest precedence of all Python operations, meaning they are evaluated last compared to other operators in an expression. This is important to consider when combining conditional expressions with other operations in Python code.  

## q09 — answerable — status: answered
**Q:** In a counting while loop, what happens when the step size is negative?  
**Expected:** The counter counts in descending order (positive step counts ascending).  
**Queries:** ['counting while loop negative step size']  
**Answer:** In a counting while loop, if the step size is negative, the counter will count in descending order. This means that the loop will decrease the counter's value with each iteration until the loop condition is no longer satisfied. For example, if the counter starts at a positive number and is decremented, the loop will continue executing until the counter reaches a value that does not satisfy the loop's condition [p0127:c00].  
> [p0127:c00] p.127: determine the number of iterations executed. Ex: A programmer may want to print all even numbers between 1 and 20. The task can be done by using a counter initialized with 1. In each iteration, the counter's value is increased by one, and a condition can check whether the counter's value is an even number or not. The change in the counter's value in each iteration is called the step size. The step size can be any positive or negative value. If the step size is a positive number, the counter coun

## q10 — answerable — status: answered
**Q:** Is the end value included in the sequence produced by range()?  
**Expected:** No. The sequence is inclusive of the start and exclusive of the end.  
**Queries:** ['range() end value included']  
**Answer:** The end value is exclusive in the sequence produced by the range() function. This means that the sequence includes the start value but does not include the end value. For example, range(0, 3) produces the sequence 0, 1, 2, but not 3 [p0130:c01].  
> [p0130:c01] p.130: • Generates a sequence beginning at 0 until end. • Step size: 1 range(4) 0, 1, 2, 3 range(start, end) • Generates a sequence beginning at start until end. • Step size: 1 range(0, 3) 0, 1, 2 range(2, 6) 2, 3, 4, 5 range(-13, -9)

## q11 — answerable — status: answered
**Q:** When should I prefer a for loop over a while loop, including in nested loops?  
**Expected:** When counting with range() or iterating over a container object, including nested situations.  
**Queries:** ['for loop vs while loop', 'when to use for loop']  
**Answer:** You should prefer a **for loop** over a **while loop** when you need to iterate over elements of a container object or when counting using a range of numbers. For example, a for loop is particularly useful in nested situations, such as iterating over multiple lists or collections, where the outer loop iterates over one collection and the inner loop iterates over another [p0135:c00].

In contrast, a **while loop** is more suitable when the number of iterations is not known beforehand and depends on a condition that may change during execution. It continues to execute as long as a specified condition remains true [p0125:c03]. 

Thus, for counting or iterating through known collections, use a for loop; for conditions that determine the loop's continuation, use a while loop.  
> [p0135:c00] p.135: j += 1 i += 1 Nested for loops A nested for loop can be implemented and used in the same way as a nested while loop. A for loop is a preferable option in cases where a loop is used for counting purposes using a range() function, or when iterating over a container object, including nested situations. Ex: Iterating over multiple course rosters. The outer loop iterates over different courses, and the inner loop iterates over the names in each course roster.
> [p0125:c03] p.125: 5.1 While loop Learning objectives By the end of this section you should be able to • Explain the loop construct in Python. • Use a while loop to implement repeating tasks. While loop A while loop is a code construct that runs a set of statements, known as the loop body, while a given condition, known as the loop expression, is true. At each iteration, once the loop statement is executed, the

## q12 — answerable — status: answered
**Q:** What is a loop without a termination condition called, and what statement is essential to leave it?  
**Expected:** An infinite loop; a break statement is essential to exit it.  
**Queries:** ['loop without a termination condition', 'essential statement to leave a loop']  
**Answer:** A loop without a termination condition is called an infinite loop. A break statement is essential to leave such a loop [p0138:c00].  
> [p0138:c00] p.138: INFINITE LOOP A break statement is an essential part of a loop that does not have a termination condition. A loop without a termination condition is known as an infinite loop. Ex: An infinite loop that counts up starting from 1 and prints the counter's value while the counter's value is less than 10. A break condition is triggered when the counter's value is equal to 10, and hence the program execution exits.

## q13 — answerable — status: answered
**Q:** What does a continue statement do inside a loop?  
**Expected:** It skips the remainder of the current loop iteration without exiting the loop entirely.  
**Queries:** ['continue statement loop']  
**Answer:** A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. After the continue statement's execution, the loop expression will be evaluated again, and the loop will continue from the loop's expression. This facilitates the loop's control and readability. [p0139:c00][p0143:c02]  
> [p0139:c00] p.139: i = 1 count = 0 while True: if i%2 == 0 or i%3 == 0: count += 1 if count >= 5: print(i) break i += 1 a. 5 b. 8 c. 30 Continue A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. A continue statement can be used in a for or a while loop. After the continue statement's execution, the loop expression will be evaluated again and the loop will continue from the loop's expression. A continue statement facilitates the loop's control and
> [p0143:c02] p.143: • A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. • A loop else statement runs after the loop's execution is completed without being interrupted by a break statement.

## q14 — answerable — status: abstain
**Q:** Why do functions make code reusable?  
**Expected:** The function body can be executed repeatedly with multiple function calls.  
**Queries:** ['functions reusable code']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** Functions make code reusable because they are named blocks of code that perform specific tasks when called. This allows programmers to write a block of code once and use it multiple times throughout a program by calling it by name. Additionally, functions promote modularity by grouping related code statements together, making it easier to modify and share among programmers, thus avoiding redundancy in code development. This modular and reusable nature of functions contributes to more organized and optimized programs.  

## q15 — answerable — status: abstain
**Q:** Can a variable created inside a function be used after the function finishes?  
**Expected:** No. It has local scope, only exists within the function, and no longer exists after the function finishes executing.  
**Queries:** ['variable scope function']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** No, a variable created inside a function has local scope and only exists within that function. After the function finishes executing, the local variables no longer exist and cannot be accessed outside of the function in which they were created. This means they cannot be used after the function finishes executing.  

## q16 — answerable — status: abstain
**Q:** What must a function do before it can edit a global variable?  
**Expected:** Declare the variable with the global keyword.  
**Queries:** ['function edit global variable']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** Before a function can edit a global variable, the variable must be declared with the global keyword. This tells the function to treat the variable as a global variable rather than a local one, allowing it to modify the global variable's value directly.  

## q17 — answerable — status: abstain
**Q:** What does PEP 8 recommend about spaces around the = sign?  
**Expected:** No spaces around = when indicating keyword arguments and default parameter values.  
**Queries:** ['PEP 8 spaces around = sign', 'PEP 8', 'PEP 8 recommendations']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** PEP 8 recommends no spaces around the = sign when indicating keyword arguments and default parameter values.  

## q18 — answerable — status: answered
**Q:** What is a branch?  
**Expected:** A group of statements that execute based on a condition.  
**Queries:** ['branch']  
**Answer:** A branch is a group of statements that execute based on a condition. In programming, branches allow for multiple possible paths of execution depending on the evaluation of conditions. For example, in an if-else statement, one and only one of the branches (the body of the if or the body of the else) is executed based on whether the condition is true or false [p0095:c01][p0102:c02].  
> [p0095:c01] p.95: 4.6 Nested decisions 4.7 Conditional expressions 4.8 Chapter summary Introduction The Python interpreter follows a single path of execution when executing a program. What if a programmer wants to define multiple possible paths? Ex: Instead of always taking the left path, a program uses the path width to decide which path to take. If the left path is wider, take the right path. Else, take the left path. A branch is a group of statements that execute based on a condition. The Expressions chapter i
> [p0102:c02] p.102: An else statement is used with an if statement and contains a body of statements that is executed when the if statement's condition is false. When an if-else statement is executed, one and only one of the branches is taken. That is, the body of the if or the body of the else is executed. Note: The else statement is at the same level of indentation as the if statement, and the body is indented.

## q19 — answerable — status: answered
**Q:** In a nested loop, what does the outer loop control?  
**Expected:** The number of the inner loop's full executions.  
**Queries:** ['nested loop outer loop control']  
**Answer:** In a nested loop, the outer loop controls the number of times the inner loop is fully executed. This means that for each iteration of the outer loop, the inner loop will run completely before the outer loop proceeds to its next iteration. More than one inner loop can exist within a nested loop structure as well. [p0132:c03]  
> [p0132:c03] p.132: 5.3 Nested loops Learning objectives By the end of this section you should be able to • Implement nested while loops. • Implement nested for loops. Nested loops A nested loop has one or more loops within the body of another loop. The two loops are referred to as outer loop and inner loop. The outer loop controls the number of the inner loop's full execution. More than one inner loop can exist in a nested loop.

## t01 — answerable — status: abstain
**Q:** What value does a function return if it has no return statement?  
**Expected:** None, representing no value.  
**Queries:** ['function return value no return statement']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** If a function has no return statement, it returns None, which represents no value.  

## t02 — answerable — status: answered
**Q:** Why shouldn't a list be used as a default parameter value?  
**Expected:** Default values are defined only once for the function, so mutable objects such as lists should not be used.  
**Queries:** ['list default parameter value']  
**Answer:** A list should not be used as a default parameter value because default parameter values are defined only once when the function is defined. This means that if a mutable object like a list is used as a default value, any modifications to that list will persist across subsequent calls to the function, leading to unexpected behavior. This can cause the function to behave incorrectly if the list is modified in one call and then used in another call without resetting it. Therefore, it is recommended to use immutable objects as default values instead [p0170:c00].  
> [p0170:c00] p.170: a. greeting("Morning", "Morgan", count=3) b. greeting(count=1,"Hi", "Bea") c. greeting("Cheers", "Colleagues", 10) Default parameter values Functions can define default parameter values to use if a positional or keyword argument is not provided for the parameter. Ex: def season(m, d, hemi="N"): defines a default value of "N" for the hemi parameter. Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as lists) should not be used as default val

## t03 — answerable — status: answered
**Q:** If a function changes a list argument, does the caller see the change? What about a string argument?  
**Expected:** Yes for a list (mutable: changes appear outside the function); no for a string (immutable: the function changes a local copy).  
**Queries:** ['function changes list argument', 'function changes string argument']  
**Answer:** If a function changes a list argument, the caller sees the change because lists are mutable objects in Python. This means that modifications to the list within the function will reflect outside the function as well. In contrast, if a function changes a string argument, the caller does not see the change because strings are immutable. Therefore, any modifications made to a string within the function do not affect the original string outside the function. This distinction is due to the nature of mutability in Python, where mutable objects can be modified after creation, while immutable objects cannot [p0162:c02][p0163:c01].  
> [p0162:c02] p.162: a. 2 b. 4 c. 3 d. 6 e. Error Modifying arguments and mutability In Python, a variable is a name that refers to an object stored in memory, aka an object reference, so Python uses a pass-by-object-reference system. If an argument is changed in a function, the changes are kept or lost depending on the object's mutability. A mutable object can be modified after creation. A function's changes to the object then appear outside the function. An immutable object cannot be modified after creation. So a 
> [p0163:c01] p.163: for temp in wknd_temps: print(f"{temp:.2f}{deg_sign}{metric}", end=" ") The output is 9.44°F 10.56°F 6.67°F. type was changed to "C" in the function but didn't keep the change outside of the function. Why is the list argument change kept and not the string argument change? (Hint: A list is mutable. A string is immutable.)

## t04 — answerable — status: answered
**Q:** When does the else block run?  
**Expected:** (Loops chapter) A loop else runs after the loop completes without being interrupted by a break statement.  
**Queries:** ['else block']  
**Answer:** The else block runs after the loop's execution is completed without being interrupted by a break statement. If the loop terminates normally (i.e., it completes all iterations without hitting a break), the else block will execute. Conversely, if the loop is interrupted by a break, the else block will not run. This is useful for identifying whether the loop completed all iterations or was exited early due to a break statement [p0140:c02][p0141:c00].  
> [p0140:c02] p.140: 5.5 Loop else Learning objectives By the end of this section you should be able to • Use loop else statement to identify when the loop execution is interrupted using a break statement. • Implement a loop else statement with a for or a while loop. Loop else A loop else statement runs after the loop's execution is completed without being interrupted by a break
> [p0141:c00] p.141: statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement. Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If 10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else statement will run and print "10 i

## t05 — answerable — status: abstain
**Q:** When a call mixes positional and keyword arguments, which must come first?  
**Expected:** Positional arguments, in the correct order, before any keyword arguments.  
**Queries:** ['positional and keyword arguments']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** When mixing positional and keyword arguments in a function call, positional arguments must come first, before any keyword arguments.  

## t06 — answerable — status: abstain
**Q:** What does elif stand for and where must it be placed?  
**Expected:** Else if; it is part of a chain and must follow an if (or elif) statement.  
**Queries:** ['elif']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** The term 'elif' stands for 'else if'. It must be placed after an 'if' statement or another 'elif' statement in a chain of decision statements.  

## u01 — UNANSWERABLE — status: abstain
**Q:** How do I write a lambda (anonymous) function in Python?  
**Expected:** Corpus = chapters 4-6 only; 'lambda' never occurs. 'anonymous' only occurs as a string default value "Anonymous" (p.170).  
**Queries:** ['lambda function', 'lambda', 'anonymous function']  
**Answer:** The textbook passages do not cover how to write a lambda (anonymous) function in Python.  

## u02 — UNANSWERABLE — status: abstain
**Q:** How does a try/except block handle a ZeroDivisionError?  
**Expected:** No 'try', 'except' or 'ZeroDivision' token in the corpus; calc_mpg avoids division by zero with an if, not exceptions.  
**Queries:** ['try except ZeroDivisionError', 'try except ZeroDivisionError example', 'try except']  
**Answer:** The textbook passages do not cover how a try/except block handles a ZeroDivisionError specifically.  

## u03 — UNANSWERABLE — status: abstain
**Q:** What is the base case of a recursive function?  
**Expected:** No 'recursion'/'recursive'/'base case' in chapters 4-6 (recursion is a later chapter, not indexed).  
**Queries:** ['base case of a recursive function', 'recursive function base case', 'base case']  
**Answer:** The textbook passages do not cover the concept of a base case in a recursive function.  
