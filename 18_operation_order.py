# Part 1

OPERATORS = {
    '+': 0,
    '*': 0
}


def tokenize(s):
    rpbuf = []
    for t in s.split():
        while t.startswith('('):
            yield '('
            t = t[1:]
        while t.endswith(')'):
            rpbuf.append(')')
            t = t[:-1]
        if t:
            yield t
        while rpbuf:
            yield rpbuf.pop()


def shuntingyard(tokens):
    """Infix -> RPN
    https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    """
    stack = []
    for t in tokens:
        if t.isdigit():
            yield t
        elif t in OPERATORS:
            while stack and stack[-1] in OPERATORS and OPERATORS[stack[-1]] >= OPERATORS[t]:
                yield stack.pop()
            stack.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(':
                yield stack.pop()
            stack.pop()
        else:
            raise ValueError("Unknown token: %s", t)
    while stack:
        yield stack.pop()


def evalrpn(tokens):
    stack = []
    for t in tokens:
        if t.isdigit():
            stack.append(int(t))
        else:
            if t == '*':
                stack.append(stack.pop() * stack.pop())
            elif t == '+':
                stack.append(stack.pop() + stack.pop())
            else:
                raise ValueError('Undefined operator: %s' % t)
    return stack.pop()


def calculate(s):
    return evalrpn(shuntingyard(tokenize(s)))


part_1 = sum(calculate(x) for x in data)

# Part 2

OPERATORS = {
    '+': 1,
    '*': 0
}

part_2 = sum(calculate(x) for x in data)

