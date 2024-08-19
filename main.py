import re


# Step 1: Tokenization function with comment handling
def tokenize(line):
    # Remove comments from the line
    line = re.sub(r'//.*', '', line)

    token_specification = [
        ('KEYWORD', r'\b(LOAD|STORE|PRINT|ADD|JOIN)\b'),  # Keywords including JOIN
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

    if command == 'LOAD':
        value = tokens[1][1]
        identifier = tokens[2][1]
        memory[identifier] = value

    elif command == 'ADD':
        identifier1 = tokens[1][1]
        identifier2 = tokens[2][1]
        identifier3 = tokens[3][1]
        result = float(memory[identifier1]) + float(memory[identifier2])
        memory[identifier3] = result

    elif command == 'STORE':
        identifier = tokens[1][1]
        value = tokens[2][1]
        memory[identifier] = value

    elif command == 'PRINT':
        identifier = tokens[1][1]
        print(memory.get(identifier, "Undefined"))

    elif command == 'JOIN':
        value1 = tokens[1][1]
        value2 = tokens[2][1]
        identifier = tokens[3][1]

        if value1 in memory:
            value1 = memory[value1]
        if value2 in memory:
            value2 = memory[value2]

        if value1.startswith('"') and value1.endswith('"'):
            value1 = value1[1:-1]
        if value2.startswith('"') and value2.endswith('"'):
            value2 = value2[1:-1]

        result = value1 + value2
        memory[identifier] = result


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
LOAD 3 s1
LOAD "Hello" s2
JOIN s1 s2 s3
PRINT s3
JOIN "Hello" "4" s4
PRINT s4
PRINT s5
"""

run_code(code)
