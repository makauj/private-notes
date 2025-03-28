# 0x19. C - Stacks, Queues - LIFO, FIFO
To implement the `push` and `pall` opcodes for a stack in a programming context, we need to define how these operations will function. Below is a simple implementation in C, along with explanations.

#### Stack Structure

First, let's define a basic stack structure and some necessary functions:

```c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define EXIT_FAILURE 1
#define STACK 0
#define QUEUE 1
#define DELIMS " \n\t\a\b"


/**
 * struct stack_s - doubly linked list representation of a stack (or queue)
 * @n: integer
 * @prev: points to the previous element of the stack (or queue)
 * @next: points to the next element of the stack (or queue)
 *
 * Description: doubly linked list node structure
 * for stack, queues, LIFO, FIFO
 */
typedef struct stack_s
{
	int n;
	struct stack_s *prev;
	struct stack_s *next;
} stack_t;

/**
 * struct instruction_s - opcode and its function
 * @opcode: the opcode
 * @f: function to handle the opcode
 *
 * Description: opcode and its function
 * for stack, queues, LIFO, FIFO
 */
typedef struct instruction_s
{
	char *opcode;
	void (*f)(stack_t **stack, unsigned int line_number);
} instruction_t;

void push(int value);
void pall(void);
void free_stack(void);
void error_exit(const char *message, int line_number);
```

#### Push Operation

The `push` operation adds an integer to the top of the stack. It will check for proper usage and handle any errors.

```c
void push(int value) {
    Node *new_node = malloc(sizeof(Node));
    if (!new_node) {
        fprintf(stderr, "Error: malloc failed\n");
        exit(EXIT_FAILURE);
    }
    new_node->value = value;
    new_node->next = stack;
    stack = new_node;
}
```

#### Pall Operation

The `pall` operation prints all values in the stack, starting from the top.

```c
void pall(void) {
    Node *current = stack;
    while (current) {
        printf("%d\n", current->value);
        current = current->next;
    }
}
```

#### Error Handling

We need to define an error handling function that will print the error message with the correct line number.

```c
void error_exit(const char *message, unsigned int line_number) {
    fprintf(stderr, "L%d: %s\n", line_number, message);
    free_stack();
    exit(EXIT_FAILURE);
}
```

#### Main Function

Finally, let's demonstrate how to use the `push` and `pall` operations in a main function. This function will read input commands and execute the appropriate operations.

```c
int main(int argc, char *argv[]) {
    char *command = NULL;
    size_t len = 0;
    int line_number = 1;

    while (getline(&command, &len, stdin) != -1) {
        char *token = strtok(command, " \n");
        if (token == NULL) {
            line_number++;
            continue;  // Ignore empty lines
        }

        if (strcmp(token, "push") == 0) {
            token = strtok(NULL, " \n");
            if (token == NULL) {
                error_exit("usage: push integer", line_number);
            }

            char *endptr;
            long value = strtol(token, &endptr, 10);
            if (*endptr != '\0') {
                error_exit("usage: push integer", line_number);
            }

            push((int)value);
        } else if (strcmp(token, "pall") == 0) {
            pall();
        } else {
            error_exit("unknown instruction", line_number);
        }

        line_number++;
    }

    free(command);
    free_stack();  // Clean up the stack at the end
    return 0;
}
```

#### Free Stack Function

Don't forget to add a function to free the stack when it's no longer needed.

```c
void free_stack(void) {
    Node *current = stack;
    Node *next;
    while (current) {
        next = current->next;
        free(current);
        current = next;
    }
}
```

#### Summary

- The `push` function pushes an integer onto the stack and handles errors related to usage and input validation.
- The `pall` function prints all elements of the stack.
- Error handling provides feedback on incorrect commands or usage, including the line number for context.
- The main function processes commands in a loop, allowing the user to interactively manage the stack.

This implementation serves as a foundational structure for a stack with the specified `push` and `pall` functionalities.

To implement the `pop` opcode, we need to create a function that removes the top element from the stack. This function will also handle the case where the stack is empty, providing the necessary error message.

Here’s how you can implement the `pop` opcode in your code structure:

### Revised Code for `pop` Opcode

#### monty_pop.c
```c
#include "main.h"

/**
 * monty_pop - function to remove the top element of the stack
 * @stack: pointer to the top of a stack
 * @line_number: position of current operation
 */
void monty_pop(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;

    if (!top_node)
    {
        handle_error(line_number, "can't pop an empty stack");
    }

    *stack = top_node->next; // Move the top pointer to the next node
    if (*stack) // If there's a next node, update its previous pointer
    {
        (*stack)->prev = NULL;
    }
    free(top_node); // Free the memory of the popped node
}
```

#### Integration with Main Code
Ensure to include the prototype for `monty_pop` in your header file (`main.h`):

#### main.h
```c
void monty_pop(stack_t **stack, unsigned int line_number);
```

#### Example Command Handling (in main function)
You need to modify your command handling logic to recognize the `pop` command. Here’s a brief example of how to handle it in your main function:

```c
// Example command handling loop (add this in your main function)
if (strcmp(command, "pop") == 0) {
    monty_pop(&stack, line_number);
}
```

#### Summary of Changes
- **Functionality**: The `monty_pop` function checks if the stack is empty. If it is, it calls `handle_error` with the appropriate message. If not, it updates the stack pointer to remove the top node and frees its memory.
- **Error Handling**: Uses the `line_number` to provide context for errors, maintaining consistency with your other opcode implementations.
- **Memory Management**: Ensures that memory for the popped node is properly freed.

With these changes, your `pop` opcode will be fully functional and integrated into the stack operations of your Monty interpreter.

The `monty_swap` function is intended to swap the two top elements of the stack. Your initial implementation has some issues, such as incorrect condition checking, syntax errors, and logic flaws. Let's correct these and provide a complete, functional implementation.

Here’s the corrected version of the `monty_swap` function:

### Revised `monty_swap` Implementation

```c
#include "main.h"

/**
 * monty_swap - function swaps the two top elements of a stack
 * @stack: pointer to the top of a stack
 * @line_number: position of current operation
 */
void monty_swap(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;
    stack_t *next_node;

    // Check if the stack has fewer than 2 elements
    if (!top_node || !top_node->next)
    {
        handle_error(line_number, "can't swap, stack too short");
    }

    next_node = top_node->next; // The second top element

    // Swap the values
    top_node->next = next_node->next; // Link top to the third element (if it exists)
    next_node->prev = NULL; // The new top node has no previous node

    // If there is a third node, update its previous pointer
    if (top_node->next)
    {
        top_node->next->prev = top_node;
    }

    // Now place next_node on top and top_node second
    next_node->next = top_node;
    top_node->prev = next_node;

    // Update the stack pointer
    *stack = next_node; // The new top of the stack
}
```

#### Explanation of Key Changes:
1. **Error Checking**: The code checks if `top_node` is `NULL` or if `top_node->next` is `NULL` (which means there is no second element to swap with). If either condition is true, it calls `handle_error` to report that the stack is too short.

2. **Node Manipulation**: 
   - It identifies `next_node` as the second top element of the stack.
   - It updates the links correctly to swap the top two nodes.

3. **Pointer Updates**: 
   - After swapping, the `*stack` pointer is updated to point to the new top of the stack.

#### Usage in Your Code
Ensure to add the function prototype for `monty_swap` in your `main.h` file:

```c
void monty_swap(stack_t **stack, unsigned int line_number);
```

#### Example Command Handling
In your command handling loop, make sure you include logic to handle the `swap` command:

```c
if (strcmp(command, "swap") == 0) {
    monty_swap(&stack, line_number);
}
```


### Revised `monty_add` Implementation

#### monty_add.c

```c
#include "main.h"

/**
 * monty_add - function adds the top two elements of the stack
 * @stack: pointer to the top of a stack
 * @line_number: position of current operation
 */
void monty_add(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;
    stack_t *next_node;

    // Check if there are fewer than two elements
    if (!top_node || !top_node->next)
    {
        handle_error(line_number, "can't add, stack too short");
    }

    next_node = top_node->next; // The second top element

    // Perform the addition
    next_node->n += top_node->n; // Add the top value to the second top value

    // Update the stack to remove the top element
    *stack = next_node; // Move the stack pointer to the new top
    next_node->next = top_node->next; // Link to the third element (if it exists)
    
    if (top_node->next) // If there's a third node, update its previous pointer
    {
        top_node->next->prev = next_node;
    }
    
    free(top_node); // Free the memory of the old top node
}
```

#### Explanation of Key Components:
1. **Error Checking**: The function checks if the stack has fewer than two elements. If so, it calls `handle_error` to report the error.

2. **Perform Addition**: The value of the top node (`top_node->n`) is added to the value of the next node (`next_node->n`).

3. **Update Stack**: 
   - The stack pointer is moved to point to `next_node`, which now contains the sum.
   - The next pointers are updated to maintain the stack's integrity.

4. **Memory Management**: The old top node is freed after it has been added.

#### Usage in Your Code
Make sure to add the function prototype for `monty_add` in your `main.h` file:

```c
void monty_add(stack_t **stack, unsigned int line_number);
```

#### Example Command Handling
In your command handling loop, include the logic to handle the `add` command:

```c
if (strcmp(command, "add") == 0) {
    monty_add(&stack, line_number);
}
```

This implementation should integrate seamlessly with your existing stack functionality and provide the desired behavior for the `add` opcode.

Implementing the `nop` opcode is straightforward since it doesn't perform any action. You just need to create a function that does nothing. Here's how you can implement the `nop` opcode:

### Implementation of `nop` Opcode

#### monty_nop.c
```c
#include "main.h"

/**
 * monty_nop - function that does nothing
 * @stack: pointer to the top of a stack (not used)
 * @line_number: position of current operation (not used)
 */
void monty_nop(stack_t **stack, unsigned int line_number)
{
    (void)stack;      // Avoid unused parameter warnings
    (void)line_number; // Avoid unused parameter warnings
}
```

#### Explanation
- **Function Definition**: The function `monty_nop` is defined with the required parameters, but it does nothing.
- **Parameter Handling**: The parameters are cast to `(void)` to prevent compiler warnings about unused parameters.

#### Usage in Your Code
Make sure to add the function prototype for `monty_nop` in your `main.h` file:

```c
void monty_nop(stack_t **stack, unsigned int line_number);
```

#### Example Command Handling
In your command handling loop, include the logic to handle the `nop` command:

```c
if (strcmp(command, "nop") == 0) {
    monty_nop(&stack, line_number);
}
```

With this implementation, your `nop` opcode will function as expected, effectively doing nothing when invoked.

### Implementation of `sub` Opcode

#### monty_sub.c

```c
void monty_sub(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;

    // Check if the stack is too short
    if (!top_node || !top_node->next) {
        handle_error(line_number, "can't sub, stack too short");
    }

    stack_t *next_node = top_node->next; // Fix: Declare next_node properly

    // Perform the subtraction
    next_node->n -= top_node->n;

    // Move the top node out of the stack
    *stack = next_node;  // Update stack to point to the new top
    next_node->next = top_node->next;  // Ensure the new top points to the correct next

    // Fix the previous pointer of the next node if it exists
    if (top_node->next) {
        top_node->next->prev = next_node;
    }

    // Free the old top node
    free(top_node);
}
```

#### Explanation:
- **Error Handling:** The error handling is intact, ensuring the function doesn’t operate on an invalid stack state.
- **Subtraction Logic:** The logic for subtraction correctly updates the value of the second node.
- **Memory Management:** Frees the top node after it’s no longer needed, preventing memory leaks.

Here's how you can implement the `div` opcode for your stack-based interpreter. This function will divide the second top element of the stack by the top element and handle the error cases as specified:
### Implementation of `div` Opcode

#### monty_div.c

```c
void monty_div(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;

    // Check if the stack contains less than two elements
    if (!top_node || !top_node->next) {
        handle_error(line_number, "can't div, stack too short");
    }

    // Check if the top element is zero
    if (top_node->n == 0) {
        handle_error(line_number, "division by zero");
    }

    stack_t *next_node = top_node->next;

    // Perform the division
    next_node->n /= top_node->n;

    // Update the stack to point to the new top node
    *stack = next_node;  // Set the new top of the stack
    next_node->next = top_node->next;  // Maintain the link to the next node

    // Update the previous pointer if there's a next node
    if (top_node->next) {
        top_node->next->prev = next_node;
    }

    // Free the old top node
    free(top_node);
}
```

#### Key Points in the Implementation:
1. **Error Handling for Stack Size:** The function checks if there are at least two elements in the stack. If not, it calls `handle_error` with the appropriate message.
  
2. **Division by Zero Check:** Before performing the division, it checks if the top element is zero. If it is, it also calls `handle_error` to handle the division by zero case.

3. **Performing the Division:** The division is performed, updating the second top element with the result of the division.

4. **Updating the Stack:** The stack pointer is updated to point to the new top element, which is the second element after the operation.

5. **Memory Management:** The top node is freed to avoid memory leaks.

This implementation adheres to the requirements and ensures that the stack behaves correctly after the `div` operation. Let me know if you need any further help!

### Implementation of `rotl` Opcode

To implement the `rotl` opcode, which rotates the stack such that the top element becomes the last one and the second top element becomes the new top, you can follow these steps:

1. **Check the Stack Size:** If the stack has fewer than two elements, there’s no need to rotate.
2. **Perform the Rotation:** Adjust the pointers to rotate the stack.

Here’s how you can implement the `rotl` function:

```c
#include "main.h"

/**
 * monty_rotl - opcode to rotate the stack to the top
 * @stack: A pointer to the top of a stack
 * @line_number: current working position
 */
void monty_rotl(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;

    // Check if the stack has at least two elements
    if (!top_node || !top_node->next) {
        return; // No action needed if there's 0 or 1 element
    }

    stack_t *second_node = top_node->next;

    // Update the stack pointers
    top_node->next = NULL; // Remove the top node from its position
    second_node->prev = NULL; // The second node becomes the new top

    // Find the last node of the stack
    stack_t *last_node = second_node;
    while (last_node->next) {
        last_node = last_node->next;
    }

    // Link the last node to the old top node
    last_node->next = top_node;
    top_node->prev = last_node;

    // Update the stack pointer
    *stack = second_node; // Now, the second node is the top of the stack
}
```
#### Explanation:
1. **Check Stack Size:** The function first checks if the stack is empty or has only one element. If so, it simply returns, as no rotation is needed.

2. **Update Pointers:**
   - The top node is stored in `top_node`.
   - The second node is identified as `second_node`.

3. **Disconnect Top Node:**
   - The `next` pointer of the `top_node` is set to `NULL` to remove it from its position.
   - The `prev` pointer of the `second_node` is set to `NULL`, making it the new top.

4. **Find the Last Node:**
   - A loop is used to traverse to the last node of the stack.

5. **Link Last Node to Top Node:**
   - The last node's `next` pointer is updated to point to the old top node, and the old top node’s `prev` pointer is set to the last node.

6. **Update Stack Pointer:** Finally, the stack pointer is updated to point to the new top node (`second_node`).

#### Summary:
This `rotl` implementation rotates the stack correctly while handling the necessary pointer adjustments.

### Implementation of `rotr` Opcode

To implement the `rotr` opcode, which rotates the stack such that the last element becomes the new top element, you can follow these steps:

1. **Check the Stack Size:** If the stack has fewer than two elements, there’s no need to rotate.
2. **Traverse to the Last Element:** Use a `while` loop to find the last element of the stack.
3. **Perform the Rotation:** Adjust the pointers to rotate the stack.

Here’s how you can implement the `rotr` function:

```c
#include "main.h"

/**
 * monty_rotr - opcode to rotate the stack to the bottom
 * @stack: A pointer to the top of a stack
 * @line_number: current working position
 */
void monty_rotr(stack_t **stack, unsigned int line_number)
{
    stack_t *top_node = *stack;

    // Check if the stack has at least two elements
    if (!top_node || !top_node->next) {
        return; // No action needed if there's 0 or 1 element
    }

    stack_t *last_node = top_node;

    // Traverse to the last node using a while loop
    while (last_node->next) {
        last_node = last_node->next;
    }

    // Now last_node points to the last element
    // Update pointers to rotate
    last_node->prev->next = NULL; // Set the second last node's next to NULL
    last_node->prev = NULL; // The last node becomes the new top
    last_node->next = top_node; // The last node points to the old top
    top_node->prev = last_node; // The old top's previous points to the last node

    // Update the stack pointer
    *stack = last_node; // Now the last node is the top of the stack
}
```

#### Explanation:
1. **Check Stack Size:** The function first checks if the stack is empty or has only one element. If so, it simply returns, as no rotation is needed.

2. **Find the Last Node:** A `while` loop is used to traverse the stack until the last node is reached.

3. **Update Pointers:**
   - The `next` pointer of the second-to-last node (which can be accessed via `last_node->prev`) is set to `NULL` to disconnect the last node from its current position.
   - The `prev` pointer of the last node is set to `NULL` since it will become the new top.
   - The `next` pointer of the last node is updated to point to the old top node.
   - The `prev` pointer of the old top node is updated to point to the new top (last node).

4. **Update Stack Pointer:** Finally, the stack pointer is updated to point to the new top node (`last_node`).

#### Summary:
This `rotr` implementation rotates the stack correctly by moving the last element to the top, while using a `while` loop for traversal.

### `stack` and `queue` Opcode implementation

