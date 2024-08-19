# Univision Programming Language

Welcome to the official repository for **Univision Programming Language**. This language is designed to be simple and easy to use, offering basic operations such as arithmetic, string manipulation, and user input. It's an interpreted language, meaning you can run your scripts directly without the need for compilation.

## Features

**Basic Arithmetic Operations**: Add, subtract, multiply, and divide numbers.
**String Manipulation**: Concatenate strings using the `JOIN` command.
**User Input**: Capture user input and store it in variables.
**Variable Storage**: Store and retrieve values in variables.
**Print Output**: Display messages and results to the user.
**Comments**: Add comments to your code with `//`.
## Language Syntax

### Commands

**LOAD `<value>` `<identifier>`**: Stores a value (number or string) in the specified variable.

Example:
```plaintext
LOAD 42 s1
LOAD "Hello, World!" s2
```

**PRINT `<identifier>`**: Prints the value stored in the specified variable.

Example:
```plaintext
PRINT s1
```

**ADD `<value1>` `<value2>` `<result_identifier>`**: Adds two values and stores the result in the specified variable.

Example:
```plaintext
ADD 5 10 s3
```

**SUBTRACT `<value1>` `<value2>` `<result_identifier>`**: Subtracts the second value from the first and stores the result in the specified variable.

Example:
```plaintext
SUBTRACT 10 5 s3
```

**MULTIPLY `<value1>` `<value2>` `<result_identifier>`**: Multiplies two values and stores the result in the specified variable.

Example:
```plaintext
MULTIPLY 4 5 s3
```

**DIVIDE `<value1>` `<value2>` `<result_identifier>`**: Divides the first value by the second and stores the result in the specified variable.

Example:
```plaintext
DIVIDE 20 4 s3
```

**JOIN `<value1>` `<value2>` `<result_identifier>`**: Concatenates two strings and stores the result in the specified variable.

Example:
```plaintext
JOIN "Hello" " World" s4
```

**INPUT `<prompt>` `<identifier>`**: Displays a prompt to the user and stores their input in the specified variable.

Example:
```plaintext
INPUT "Enter your name: " s1
```

**TOSTRING `<value>` `<result_identifier>`**: Converts a number to a string and stores it in the specified variable.

Example:
```plaintext
TOSTRING s1 s2
```

**TONUMBER `<value>` `<result_identifier>`**: Converts a string to a number and stores it in the specified variable.

Example:
```plaintext
TONUMBER "42" s1
```

### Comments

**Comments**: Use `//` to add comments to your code. Anything after `//` on the same line will be ignored by the interpreter.

Example:
```plaintext
// This is a comment
LOAD 10 s1 // Load the number 10 into s1
```

## Example Scripts

### Basic Arithmetic and Printing

```plaintext
LOAD 5 s1
LOAD 10 s2
ADD s1 s2 s3
PRINT s3
```

This script adds 5 and 10, stores the result in `s3`, and prints the result (`15`).

### User Input and String Manipulation

```plaintext
INPUT "What is your name? " s1
JOIN "Hello, " s1 s2
JOIN s2 "! Welcome to the program." s2
PRINT s2
```

This script asks for the user's name, creates a greeting message, and prints it.

### Combining Strings and Arithmetic

```plaintext
INPUT "Enter a number: " s1
TONUMBER s1 s1
MULTIPLY s1 2 s2
TOSTRING s2 s3
JOIN "Your number doubled is: " s3 s4
PRINT s4
```

This script takes a number from the user, doubles it, converts the result to a string, and prints a message with the result.

### Example Scripts
Example Script:
```plaintext
// Ask the user for their name
INPUT "What is your name? " s1

// Greet the user
JOIN "Hello, " s1 s2
JOIN s2 "! Welcome to the program." s2
PRINT s2

// Ask the user for two numbers
INPUT "Enter the first number: " s3
INPUT "Enter the second number: " s4
TONUMBER s3 s3
TONUMBER s4 s4

// Perform some calculations
ADD s3 s4 s5            // s5 = s3 + s4
SUBTRACT s3 s4 s6       // s6 = s3 - s4
MULTIPLY s3 s4 s7       // s7 = s3 * s4
DIVIDE s3 s4 s8         // s8 = s3 / s4

// Convert the results to strings
TOSTRING s5 s9
TOSTRING s6 s10
TOSTRING s7 s11
TOSTRING s8 s12

// Create and print the final output messages
JOIN "Sum of the numbers: " s9 s13
PRINT s13

JOIN "Difference of the numbers: " s10 s14
PRINT s14

JOIN "Product of the numbers: " s11 s15
PRINT s15

JOIN "Quotient of the numbers: " s12 s16
PRINT s16
```
### Credits

Code and readme by chatgpt cause idk how to make a programming language and im too lazy to make a readme but the programming lang structure is by me
