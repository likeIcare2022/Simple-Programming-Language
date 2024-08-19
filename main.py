import re
import sys
import random  # Import the random module for RANDOM command
import math


def tokenize(line):
    # Remove comments from the line
    line = re.sub(r'//.*', '', line)

    token_specification = [
        ('KEYWORD', r'\b(LOAD|PRINT|ADD|SUBTRACT|MULTIPLY|DIVIDE|JOIN|INPUT|TOSTRING|TONUMBER|RANDOM|CLEAR|CEILING|FLOOR|ABS|SQRT)\b'),
        # Updated keywords
        ('STRING', r'"[^"]*"'),  # String literals
        ('NUMBER', r'\b\d+(\.\d+)?\b'),  # Integer or floating-point numbers
        ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),  # Identifiers
        ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
        ('MISMATCH', r'.'),  # Any other character
    ]

    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    get_token = re.compile(token_regex).match

    tokens = []
    pos = 0
    while pos < len(line):
        match = get_token(line, pos)
        if not match:
            raise RuntimeError(f'Unexpected character: {line[pos]}')
        type = match.lastgroup
        if type == 'SKIP':
            pass
        elif type == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {match.group()}')
        else:
            tokens.append((type, match.group()))
        pos = match.end()

    return tokens


# Memory storage
memory = {}


def resolve_value(value):
    """ Resolve a value which can be a literal or an identifier. """
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]  # Remove surrounding quotes and return as string
    try:
        return float(value)  # Try converting to a number
    except ValueError:
        return memory.get(value, 0)  # Return the value from memory if not a number


def parse_and_execute(tokens):
    if not tokens:
        return

    command = tokens[0][1]

    if command == 'LOAD':
        value = tokens[1][1]
        identifier = tokens[2][1]
        memory[identifier] = resolve_value(value)

    elif command == 'ADD':
        operand1 = tokens[1][1]
        operand2 = tokens[2][1]
        result_identifier = tokens[3][1]
        value1 = resolve_value(operand1)
        value2 = resolve_value(operand2)
        if isinstance(value1, str) or isinstance(value2, str):
            raise TypeError("Cannot perform addition on string values.")
        result = value1 + value2
        memory[result_identifier] = result

    elif command == 'SQRT':
        operand1 = tokens[1][1]
        result_identifier = tokens[2][1]
        value1 = resolve_value(operand1)
        if isinstance(value1, str):
            raise TypeError("Cannot perform sqrts on string values.")
        result = math.sqrt(value1)
        memory[result_identifier] = result

    elif command == 'ABS':
        operand1 = tokens[1][1]
        result_identifier = tokens[2][1]
        value1 = resolve_value(operand1)
        if isinstance(value1, str):
            raise TypeError("Cannot perform abs on string values.")
        result = abs(value1)
        memory[result_identifier] = result

    elif command == 'FLOOR':
        operand1 = tokens[1][1]
        result_identifier = tokens[2][1]
        value1 = resolve_value(operand1)
        if isinstance(value1, str):
            raise TypeError("Cannot perform floors on string values.")
        result = math.floor(value1)
        memory[result_identifier] = result

    elif command == 'CEILING':
        operand1 = tokens[1][1]
        result_identifier = tokens[2][1]
        value1 = resolve_value(operand1)
        if isinstance(value1, str):
            raise TypeError("Cannot perform ceilings on string values.")
        result = math.ceil(value1)
        memory[result_identifier] = result

    elif command == 'SUBTRACT':
        operand1 = tokens[1][1]
        operand2 = tokens[2][1]
        result_identifier = tokens[3][1]

        value1 = resolve_value(operand1)
        value2 = resolve_value(operand2)

        if isinstance(value1, str) or isinstance(value2, str):
            raise TypeError("Cannot perform subtraction on strings.")
        result = value1 - value2
        memory[result_identifier] = result

    elif command == 'MULTIPLY':
        operand1 = tokens[1][1]
        operand2 = tokens[2][1]
        result_identifier = tokens[3][1]

        value1 = resolve_value(operand1)
        value2 = resolve_value(operand2)

        if isinstance(value1, str) or isinstance(value2, str):
            raise TypeError("Cannot perform multiplication on strings.")
        result = value1 * value2
        memory[result_identifier] = result

    elif command == 'DIVIDE':
        operand1 = tokens[1][1]
        operand2 = tokens[2][1]
        result_identifier = tokens[3][1]

        value1 = resolve_value(operand1)
        value2 = resolve_value(operand2)

        if isinstance(value1, str) or isinstance(value2, str):
            raise TypeError("Cannot perform division on strings.")
        if value2 == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        result = value1 / value2
        memory[result_identifier] = result

    elif command == 'STORE':
        identifier = tokens[1][1]
        value = tokens[2][1]
        memory[identifier] = resolve_value(value)

    elif command == 'PRINT':
        value = tokens[1][1]
        resolved_value = resolve_value(value)
        print(resolved_value)

    elif command == 'JOIN':
        value1 = tokens[1][1]
        value2 = tokens[2][1]
        result_identifier = tokens[3][1]

        value1 = resolve_value(value1)
        value2 = resolve_value(value2)

        result = str(value1) + str(value2)
        memory[result_identifier] = result

    elif command == 'INPUT':
        prompt = tokens[1][1]
        identifier = tokens[2][1]
        # Remove surrounding quotes from the prompt string
        if prompt.startswith('"') and prompt.endswith('"'):
            prompt = prompt[1:-1]
        user_input = input(prompt + " ")  # Adding a space for better readability
        memory[identifier] = user_input

    elif command == 'TOSTRING':
        identifier = tokens[1][1]
        result_identifier = tokens[2][1]
        memory[result_identifier] = str(memory.get(identifier, ""))

    elif command == 'TONUMBER':
        identifier = tokens[1][1]
        result_identifier = tokens[2][1]
        memory[result_identifier] = float(memory.get(identifier, 0))

    elif command == 'RANDOM':
        min_value = resolve_value(tokens[1][1])
        max_value = resolve_value(tokens[2][1])
        result_identifier = tokens[3][1]

        if not (isinstance(min_value, (int, float)) and isinstance(max_value, (int, float))):
            raise ValueError("RANDOM min and max values must be numbers.")

        if min_value > max_value:
            raise ValueError("RANDOM min value must not be greater than max value.")

        result = random.uniform(min_value, max_value)  # Generates a float in the range [min, max)
        memory[result_identifier] = result

    elif command == 'CLEAR':
        memory.clear()


# Function to run code from a file
def run_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    run_code(code)


# Function to run code directly from a string
def run_code(code):
    lines = code.splitlines()
    lines = [line for line in lines if line.strip()]

    for line in lines:
        tokens = tokenize(line)
        if tokens:  # Only process non-empty tokenized lines
            parse_and_execute(tokens)


# Main entry point when running from the command line
if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Read the script file provided as an argument
        script_file = sys.argv[1]
        run_code_from_file(script_file)
    else:
        # Example usage with embedded code
        while True:
            code = input(">>> ")
            run_code(code)
