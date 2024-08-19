import re


def tokenize(line):
    # Remove comments from the line
    line = re.sub(r'//.*', '', line)

    token_specification = [
        ('KEYWORD', r'\b(LOAD|PRINT|ADD|SUBTRACT|MULTIPLY|DIVIDE|JOIN|TONUMBER|INPUT)\b'),  # Added math operations
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


# Step 2: Parsing and execution function
memory = {}


def parse_and_execute(tokens):
    if not tokens:
        return

    command = tokens[0][1]

    def resolve_value(value):
        """ Resolve a value which can be a literal or an identifier. """
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]  # Remove surrounding quotes and return as string
        if value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
            return float(value)  # Convert numeric literals to float
        return memory.get(value, 0)  # Default to 0 if identifier not found

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
            result = str(value1) + str(value2)
        else:
            result = value1 + value2

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
        identifier = tokens[1][1]
        print(memory.get(identifier, "Undefined"))

    elif command == 'JOIN':
        value1 = tokens[1][1]
        value2 = tokens[2][1]
        result_identifier = tokens[3][1]

        value1 = resolve_value(value1)
        value2 = resolve_value(value2)

        result = str(value1) + str(value2)
        memory[result_identifier] = result

    elif command == 'INPUT':
        prompt_message = resolve_value(tokens[1][1])
        identifier = tokens[2][1]
        user_input = input(prompt_message)  # Get input from the user
        memory[identifier] = user_input

    elif command == 'TONUMBER':
        identifier = tokens[1][1]
        result_identifier = tokens[2][1]
        value = resolve_value(identifier)
        try:
            result = float(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to a number.")
        memory[result_identifier] = result

    elif command == 'TOSTRING':
        identifier = tokens[1][1]
        result_identifier = tokens[2][1]
        value = resolve_value(identifier)
        try:
            result = str(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to a number.")
        memory[result_identifier] = result


# Step 3: Integrate multi-line code processing
def run_code(code):
    lines = code.splitlines()
    lines = [line for line in lines if line.strip()]

    for line in lines:
        tokens = tokenize(line)
        if tokens:  # Only process non-empty tokenized lines
            parse_and_execute(tokens)


# Example usage with comments
code = """
// Put any code here
"""

run_code(code)
