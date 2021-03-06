import regex as re


class LambdaSyntaxError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def _cls(code=437):
    import os
    os.system(f"chcp {code}")
    os.system("cls")


def resize_window(w, h):
    import os
    os.system(f"mode con cols={w} lines={h}")


pattern = re.compile('//.+|/\*\*[\W\w]*?\*/')


def clear_commit(code):
    global pattern
    return re.sub(pattern, "", code)


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] in " \n\t":
        return (trim(s[1:]))
    elif s[-1] in " \n\t":
        return (trim(s[:-1]))
    return s


def tokenize(string):
    def insterBlank(code):
        return re.sub("([\\.()])", " \\g<1> ", code)
    return re.split("\s+", trim(insterBlank(string)))


def file2tokens(file):
    tokens = []
    with open(file, "r", encoding="utf-8") as f:
        nocommit = clear_commit(f.read())
        tokenizes = [trim(t)
                     for t in nocommit .split("\n") if trim(t) is not ""]
        for t in tokenizes:
            tokens += tokenize(t)
    return tokens


def pull(tokens):
    subNode = ["("]
    breakCount = 1
    while len(tokens) is not 0:
        token = tokens.pop(0)
        if token == "(":
            breakCount += 1
        elif token == ")":
            breakCount -= 1
        subNode.append(token)
        if breakCount is 0:
            break
    if breakCount is not 0:
        raise LambdaSyntaxError("Uncaught SyntaxError: Unexpected token )")
    return subNode


fix_pattern = re.compile(r"([\$\(\)\{\}\[\]\*\+\.\?\\^\|])")


def fuzzyfinder(user_input, collection, ignore_case=False):
    global fix_pattern

    def regex_fix(rp):
        return re.sub(fix_pattern, " \\\\g<1> ", rp)
    suggestions = []
    pattern = '.*?'.join(regex_fix(user_input))
    if ignore_case:
        pattern = pattern.upper()
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item.upper() if ignore_case else item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


if __name__ == '__main__':
    code = """
    /**
     * editor: zhzluke96
     */
    // chrch num
    (define
    zero f.x.x)
    (define succ n.f.x.f(n f x)) // num ++
    // EOF
    """
    nocommit = clear_commit(code)
    nospace = tokenize(nocommit)
    print(nocommit)
    tokenizes = [trim(t) for t in nocommit.split("\n") if trim(t) is not ""]
    print(tokenizes)

    print(nospace)

    # def tokenize2(string):
    #     def insterBlank(code):
    #         return re.sub("([\\.()])", " \\g<1> ", code)
    #     print(insterBlank(string))
    #     return re.split("\s+", trim(insterBlank(string)))
    #
    # print("1", tokenize("(define succ n.f.x.f(n f x))"))
    # print("2", tokenize2("(define succ n.f.x.f(n f x))"))

    # tokens = []
    # for t in tokenizes:
    #     tokens += tokenize(t)
    # print(tokens)

    code_tokens = file2tokens("../calculus/SKI.lamb")
    print(code_tokens)
    from interpreter import parse_tokens
    print(parse_tokens(code_tokens))
