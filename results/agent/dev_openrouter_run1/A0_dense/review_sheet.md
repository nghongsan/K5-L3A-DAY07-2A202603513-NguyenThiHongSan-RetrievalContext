# Review sheet (grade manually; gold shown for the reviewer only)

## q01 — answerable — status: abstain
**Q:** Which values does bool() convert to False?  
**Expected:** 0 and the empty string (any non-zero number or non-empty string becomes True).  
**Queries:** ['bool() convert to False', 'boolean values that evaluate to False']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** The values that bool() converts to False include 0 and an empty string. These are the only specific examples mentioned in the textbook passages.  

## q02 — answerable — status: answered
**Q:** What goes wrong if I write is_zero = num=0 when I meant to test whether num is zero?  
**Expected:** It assigns 0 to both is_zero and num regardless of num's original value; = is assignment, == is comparison.  
**Queries:** ['is_zero = num=0']  
**Answer:** If you write `is_zero = num=0`, it will always assign both `is_zero` and `num` the value of 0, regardless of what `num` was originally. This is because the `=` operator is used for assignment, not comparison. To test whether `num` is zero, you should use `==`, which performs a comparison and does not modify the variable. Thus, the correct statement would be `is_zero = (num == 0)` to properly check if `num` is zero without altering its value. This distinction is crucial in programming to avoid unintended assignments instead of comparisons. [p0099:c01]  
> [p0099:c01] p.99: compare_result = (z == "coriander") a. True b. False 20 . a = "dog" compare_result = (a < "cat") a. True b. False = VS == A common mistake is using = for comparison instead of ==. Ex: is_zero = num=0 will always assign is_zero and num with 0, regardless of num's original value. The = operator performs assignment and will modify the variable. The == operator performs comparison, does not modify the variable, and produces True or False. EXPLORING FURTHER • Unicode Basic Latin Chart (https://openst

## q03 — answerable — status: abstain
**Q:** How many spaces per indentation level does the PEP 8 style guide recommend?  
**Expected:** Four spaces per indentation level.  
**Queries:** ['PEP 8 indentation']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** The PEP 8 style guide recommends four spaces per indentation level.  

## q04 — answerable — status: abstain
**Q:** When an if-else statement runs, can both the if body and the else body execute?  
**Expected:** No. One and only one of the branches is taken.  
**Queries:** ['if-else statement execution']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** No, when an if-else statement runs, only one of the branches (either the if body or the else body) is executed, not both.  

## q05 — answerable — status: answered
**Q:** Which operator is the main exception to left associativity, and how is 2 ** 3 ** 4 evaluated?  
**Expected:** Exponentiation is right associative, so 2 ** 3 ** 4 is evaluated as 2 ** (3**4).  
**Queries:** ['operator exception to left associativity', '2 ** 3 ** 4 evaluation']  
**Answer:** The main exception to left associativity is the exponentiation operator (**), which is right associative. This means that when evaluating expressions with multiple exponentiation operators, they are evaluated from right to left. For example, the expression 2 ** 3 ** 4 is evaluated as 2 ** (3 ** 4) rather than (2 ** 3) ** 4. Thus, 3 ** 4 is calculated first, followed by 2 raised to that result [p0109:c00].  
> [p0109:c00] p.109: 1 . x ** 2 + 6 / 3 a. 6 / 3 b. x ** 2 c. 2 + 6 2 . not 3 * 5 > 10 a. 3 * 5 b. not 3 c. 5 > 10 3 . z == 5 and x / 8 < 100 a. 5 and x b. x / 8 c. 8 < 100 Associativity What if operators beside each other have the same level of precedence? Associativity determines the order of operations when precedence is the same. Ex: 8 / 4 * 3 is evaluated as (8/4) * 3 rather than 8 / (4*3) because multiplication and division are left associative. Most operators are left associative and are evaluated from left t

## q06 — answerable — status: answered
**Q:** How does Python evaluate a chained comparison such as 10 < x <= 20?  
**Expected:** As 10 < x and x <= 20, evaluated from left to right.  
**Queries:** ['chained comparison']  
**Answer:** In Python, a chained comparison like 10 < x <= 20 is evaluated as two separate comparisons: 10 < x and x <= 20. This means that both conditions must be true for the entire expression to be true. The evaluation is done from left to right, effectively converting the chained comparison into a combination of comparisons.  

This is supported by the textbook which states that "When comparison operators are chained, the expression is converted into the equivalent combination of comparisons and evaluated from left to right" [p0109:c01].  
> [p0109:c01] p.109: When comparison operators are chained, the expression is converted into the equivalent combination of comparisons and evaluated from left to right. Ex. 10 < x <= 20 is evaluated as 10 < x and x <= 20.

## q07 — answerable — status: answered
**Q:** Why can two separate if statements give a student a double grade curve, and what fixes it?  
**Expected:** Separate if statements do not guarantee only one branch is taken, so both can execute; chaining with elif fixes it.  
**Queries:** ['two separate if statements double grade curve', 'fix double grade curve']  
**Answer:** Two separate `if` statements can lead to a double grade curve because both conditions may be true independently, causing both branches to execute. For example, if a student's score is 60, and the conditions for both curves are met, the score could be increased by both curves, resulting in an unintended final score (e.g., from 60 to 75) [p0111:c02]. To fix this issue, you can use `elif` statements instead of separate `if` statements. This way, once a condition is met and its corresponding block is executed, the subsequent conditions will not be evaluated. This ensures that only one branch is taken, preventing multiple grade curves from being applied [p0111:c03].  
> [p0111:c02] p.111: elif Sometimes, a complicated decision is based on more than a single condition. Ex: A travel planning site reviews the layovers on an itinerary. If a layover is greater than 24 hours, the site should suggest accommodations. Else if the layover is less than one hour, the site should alert for a possible missed connection. Two separate if statements do not guarantee that only one branch is taken and might result in both branches being taken. Ex: The program below attempts to add a curve based on 
> [p0111:c03] p.111: score = int(input()) if score < 70: score += 10 # Wrong: if 70 <= score < 85: score += 5 Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short for else if) statement checks a condition when the prior decision statement's condition is false. An elif statement is part of a chain and must follow an if (or elif) statement. if-elif statement template: # Statements before if condition: # Body elif condition: # Body # Statements after

## q08 — answerable — status: answered
**Q:** What precedence do conditional expressions have compared with other Python operations?  
**Expected:** The lowest precedence of all Python operations.  
**Queries:** ['conditional expressions precedence']  
**Answer:** Conditional expressions in Python have the lowest precedence of all operations. This means that when evaluating expressions with multiple operators, conditional expressions will be evaluated last, after all other operators have been processed. For example, in the expression `max_num = y if x < y else x`, the conditional expression is evaluated only after the comparison `x < y` is resolved [p0119:c02].  
> [p0119:c02] p.119: Conditional expression template: expression_if_true if condition else expression_if_false A conditional expression is evaluated by first checking the condition. If condition is true, expression_if_true is evaluated, and the result is the resulting value of the conditional expression. Else, expression_if_false is evaluated, and the result is the resulting value of the conditional expression. A variable can be assigned with a conditional expression. Ex: Finding the max of two numbers can be calcul

## q09 — answerable — status: answered
**Q:** In a counting while loop, what happens when the step size is negative?  
**Expected:** The counter counts in descending order (positive step counts ascending).  
**Queries:** ['counting while loop negative step size']  
**Answer:** When the step size in a counting while loop is negative, the counter counts in descending order. This means that the loop will decrease the counter's value with each iteration, allowing it to count downwards instead of upwards. If the step size is positive, the counter counts in ascending order, while a negative step size results in descending counting [p0127:c00].  
> [p0127:c00] p.127: determine the number of iterations executed. Ex: A programmer may want to print all even numbers between 1 and 20. The task can be done by using a counter initialized with 1. In each iteration, the counter's value is increased by one, and a condition can check whether the counter's value is an even number or not. The change in the counter's value in each iteration is called the step size. The step size can be any positive or negative value. If the step size is a positive number, the counter coun

## q10 — answerable — status: answered
**Q:** Is the end value included in the sequence produced by range()?  
**Expected:** No. The sequence is inclusive of the start and exclusive of the end.  
**Queries:** ['range() end value']  
**Answer:** The end value is not included in the sequence produced by the range() function; it is exclusive of the end value. The sequence generated starts at the specified start value and goes up to, but does not include, the end value. This is confirmed in the textbook, which states that the range() function generates a sequence of integers that is inclusive of the start and exclusive of the end of the sequence [p0130:c00].  
> [p0130:c00] p.130: a. A string* b. A*s*t*r*i*n*g* c. A* *s*t*r*i*n*g* Range() function in for loop A for loop can be used for iteration and counting. The range() function is a common approach for implementing counting in a for loop. A range() function generates a sequence of integers between the two numbers given a step size. This integer sequence is inclusive of the start and exclusive of the end of the sequence. The range() function can take up to three input values. Examples are provided in the table below. Ran

## q11 — answerable — status: answered
**Q:** When should I prefer a for loop over a while loop, including in nested loops?  
**Expected:** When counting with range() or iterating over a container object, including nested situations.  
**Queries:** ['for loop vs while loop', 'when to use for loop']  
**Answer:** You should prefer a for loop over a while loop when you need to iterate over elements of a container object or when counting using a range function. For loops are particularly useful in nested situations, such as iterating over multiple lists or rosters, where the outer loop iterates over one set and the inner loop iterates over another. In contrast, while loops are better suited for situations where the number of iterations is not predetermined and depends on a condition being true. For example, a while loop continues until a specific condition changes, while a for loop is typically used when the number of iterations is known beforehand or when iterating through a collection of items. [p0128:c03][p0135:c00][p0143:c01]  
> [p0128:c03] p.128: 5.2 For loop Learning objectives By the end of this section you should be able to • Explain the for loop construct. • Use a for loop to implement repeating tasks.
> [p0135:c00] p.135: j += 1 i += 1 Nested for loops A nested for loop can be implemented and used in the same way as a nested while loop. A for loop is a preferable option in cases where a loop is used for counting purposes using a range() function, or when iterating over a container object, including nested situations. Ex: Iterating over multiple course rosters. The outer loop iterates over different courses, and the inner loop iterates over the names in each course roster.
> [p0143:c01] p.143: 5.6 Chapter summary Highlights from this chapter include: • A while loop runs a set of statements, known as the loop body, while a given condition, known as the loop expression, is true. • A for loop can be used to iterate over elements of a container object. • A range() function generates a sequence of integers between the two numbers given a step size. • A nested loop has one or more loops within the body of another loop. • A break statement is used within a for or a while loop to allow the pr

## q12 — answerable — status: answered
**Q:** What is a loop without a termination condition called, and what statement is essential to leave it?  
**Expected:** An infinite loop; a break statement is essential to exit it.  
**Queries:** ['loop without a termination condition', 'essential statement to leave a loop']  
**Answer:** A loop without a termination condition is called an infinite loop. To exit such a loop, a break statement is essential [p0138:c00].  
> [p0138:c00] p.138: INFINITE LOOP A break statement is an essential part of a loop that does not have a termination condition. A loop without a termination condition is known as an infinite loop. Ex: An infinite loop that counts up starting from 1 and prints the counter's value while the counter's value is less than 10. A break condition is triggered when the counter's value is equal to 10, and hence the program execution exits.

## q13 — answerable — status: answered
**Q:** What does a continue statement do inside a loop?  
**Expected:** It skips the remainder of the current loop iteration without exiting the loop entirely.  
**Queries:** ['continue statement loop']  
**Answer:** A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. After the continue statement's execution, the loop expression will be evaluated again, and the loop will continue from there. This statement can be used in both for and while loops, facilitating control and readability of the loop's execution flow. [p0139:c00][p0143:c02]  
> [p0139:c00] p.139: i = 1 count = 0 while True: if i%2 == 0 or i%3 == 0: count += 1 if count >= 5: print(i) break i += 1 a. 5 b. 8 c. 30 Continue A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. A continue statement can be used in a for or a while loop. After the continue statement's execution, the loop expression will be evaluated again and the loop will continue from the loop's expression. A continue statement facilitates the loop's control and
> [p0143:c02] p.143: • A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. • A loop else statement runs after the loop's execution is completed without being interrupted by a break statement.

## q14 — answerable — status: abstain
**Q:** Why do functions make code reusable?  
**Expected:** The function body can be executed repeatedly with multiple function calls.  
**Queries:** ['functions reusable code']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** Functions make code reusable because they allow programmers to write a block of code once, name it, and call it multiple times throughout the program. This promotes modularity by grouping related code statements together, making it easier to modify and share among programmers. As a result, functions help avoid redundancy and facilitate complex calculations by reading in and returning values as needed. This modular, reusable approach enhances code efficiency and maintainability.  

## q15 — answerable — status: abstain
**Q:** Can a variable created inside a function be used after the function finishes?  
**Expected:** No. It has local scope, only exists within the function, and no longer exists after the function finishes executing.  
**Queries:** ['variable scope function']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** No, a variable created inside a function cannot be used after the function finishes. It has local scope and only exists within the function. Once the function completes execution, the local variables are no longer accessible.  

## q16 — answerable — status: abstain
**Q:** What must a function do before it can edit a global variable?  
**Expected:** Declare the variable with the global keyword.  
**Queries:** ['function edit global variable']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** Before a function can edit a global variable, it must declare the variable with the global keyword. This tells Python that the variable being edited is the global one, not a local one created within the function.  

## q17 — answerable — status: abstain
**Q:** What does PEP 8 recommend about spaces around the = sign?  
**Expected:** No spaces around = when indicating keyword arguments and default parameter values.  
**Queries:** ['PEP 8 spaces around = sign']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** PEP 8 recommends no spaces around the = sign when indicating keyword arguments and default parameter values.  

## q18 — answerable — status: abstain
**Q:** What is a branch?  
**Expected:** A group of statements that execute based on a condition.  
**Queries:** ['branch']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** A branch is a group of statements that execute based on a condition. It allows a program to define multiple possible paths of execution depending on the conditions evaluated during runtime. For example, a program can choose different paths based on specific criteria, such as the width of a path in a decision-making scenario. This concept is essential for making decisions in programming, as explored in Chapter 4 of the textbook.  

## q19 — answerable — status: abstain
**Q:** In a nested loop, what does the outer loop control?  
**Expected:** The number of the inner loop's full executions.  
**Queries:** ['nested loop outer loop control']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** In a nested loop, the outer loop controls the number of times the inner loop is fully executed. This means that for each iteration of the outer loop, the inner loop will run completely before the outer loop proceeds to its next iteration.  More than one inner loop can exist within a nested loop structure.  

## t01 — answerable — status: abstain
**Q:** What value does a function return if it has no return statement?  
**Expected:** None, representing no value.  
**Queries:** ['function return value no return statement']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** If a function has no return statement, it returns None, which represents no value.  

## t02 — answerable — status: abstain
**Q:** Why shouldn't a list be used as a default parameter value?  
**Expected:** Default values are defined only once for the function, so mutable objects such as lists should not be used.  
**Queries:** ['list default parameter value']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** A list should not be used as a default parameter value because default parameter values are defined only once when the function is defined. This means that if a mutable object like a list is used, any modifications to that list will persist across subsequent calls to the function, leading to unexpected behavior. This is a common pitfall in Python programming.  

## t03 — answerable — status: answered
**Q:** If a function changes a list argument, does the caller see the change? What about a string argument?  
**Expected:** Yes for a list (mutable: changes appear outside the function); no for a string (immutable: the function changes a local copy).  
**Queries:** ['function argument list change', 'function argument string change']  
**Answer:** Yes, if a function changes a list argument, the caller sees the change because lists are mutable objects in Python. This means that modifications to the list within the function will reflect outside the function as well. In contrast, if a string argument is changed, the caller does not see the change because strings are immutable. Therefore, any modification to a string within the function does not affect the original string outside the function. This behavior is due to Python's pass-by-object-reference system, where changes to mutable objects are retained, while immutable objects require a local copy for modifications, which do not affect the original object outside the function. [p0162:c02][p0163:c01]  
> [p0162:c02] p.162: a. 2 b. 4 c. 3 d. 6 e. Error Modifying arguments and mutability In Python, a variable is a name that refers to an object stored in memory, aka an object reference, so Python uses a pass-by-object-reference system. If an argument is changed in a function, the changes are kept or lost depending on the object's mutability. A mutable object can be modified after creation. A function's changes to the object then appear outside the function. An immutable object cannot be modified after creation. So a 
> [p0163:c01] p.163: for temp in wknd_temps: print(f"{temp:.2f}{deg_sign}{metric}", end=" ") The output is 9.44°F 10.56°F 6.67°F. type was changed to "C" in the function but didn't keep the change outside of the function. Why is the list argument change kept and not the string argument change? (Hint: A list is mutable. A string is immutable.)

## t04 — answerable — status: answered
**Q:** When does the else block run?  
**Expected:** (Loops chapter) A loop else runs after the loop completes without being interrupted by a break statement.  
**Queries:** ['else block']  
**Answer:** The else block runs after the loop's execution is completed without being interrupted by a break statement. If the loop is terminated normally (i.e., it completes all iterations without hitting a break), the else block will execute. For example, if a loop is searching for a value and does not find it, the else block will run to indicate that the value was not found [p0141:c00][p0143:c02].  
> [p0141:c00] p.141: statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement. Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If 10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else statement will run and print "10 i
> [p0143:c02] p.143: • A continue statement allows for skipping the execution of the remainder of the loop without exiting the loop entirely. • A loop else statement runs after the loop's execution is completed without being interrupted by a break statement.

## t05 — answerable — status: abstain
**Q:** When a call mixes positional and keyword arguments, which must come first?  
**Expected:** Positional arguments, in the correct order, before any keyword arguments.  
**Queries:** ['positional and keyword arguments']  
**Answer:** Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.  
**Rejected (citation guard):** When mixing positional and keyword arguments in a function call, positional arguments must come first, before any keyword arguments.  

## t06 — answerable — status: answered
**Q:** What does elif stand for and where must it be placed?  
**Expected:** Else if; it is part of a chain and must follow an if (or elif) statement.  
**Queries:** ['elif']  
**Answer:** Elif stands for "else if" and must be placed after an if statement or another elif statement in a chain of decision statements. It allows the programmer to check additional conditions when the previous conditions are false. The structure is part of a chained decision statement, following the format: if condition: (body) elif condition: (body) [p0111:c03].  
> [p0111:c03] p.111: score = int(input()) if score < 70: score += 10 # Wrong: if 70 <= score < 85: score += 5 Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short for else if) statement checks a condition when the prior decision statement's condition is false. An elif statement is part of a chain and must follow an if (or elif) statement. if-elif statement template: # Statements before if condition: # Body elif condition: # Body # Statements after

## u01 — UNANSWERABLE — status: abstain
**Q:** How do I write a lambda (anonymous) function in Python?  
**Expected:** Corpus = chapters 4-6 only; 'lambda' never occurs. 'anonymous' only occurs as a string default value "Anonymous" (p.170).  
**Queries:** ['lambda function', 'anonymous function']  
**Answer:** The textbook passages do not cover how to write a lambda (anonymous) function in Python.  

## u02 — UNANSWERABLE — status: abstain
**Q:** How does a try/except block handle a ZeroDivisionError?  
**Expected:** No 'try', 'except' or 'ZeroDivision' token in the corpus; calc_mpg avoids division by zero with an if, not exceptions.  
**Queries:** ['try except ZeroDivisionError', 'try except ZeroDivisionError example']  
**Answer:** The retrieved passages do not contain information about how a try/except block handles a ZeroDivisionError. Therefore, I cannot provide an answer based on the textbook content.  

## u03 — UNANSWERABLE — status: abstain
**Q:** What is the base case of a recursive function?  
**Expected:** No 'recursion'/'recursive'/'base case' in chapters 4-6 (recursion is a later chapter, not indexed).  
**Queries:** ['base case recursive function', 'base case']  
**Answer:** The textbook passages do not cover the concept of a base case in a recursive function.  
