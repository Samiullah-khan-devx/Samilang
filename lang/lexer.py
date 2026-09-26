"""SamiLang lexer: source text -> tokens (type, value, line)."""
KEYWORDS = {"print", "if", "else", "while", "for", "in", "func", "return",
            "and", "or", "not", "true", "false"}
TWO_CHAR = {"==", "!=", "<=", ">=", ".."}
SINGLE = set("+-*/%()=<> {},;")

class LexError(Exception):
    pass

def lex(src):
    toks, i, line, n = [], 0, 1, len(src)
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1; i += 1
        elif c in " \t\r":
            i += 1
        elif c == "#":
            while i < n and src[i] != "\n":
                i += 1
        elif c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            if j < n and src[j] == "." and j + 1 < n and src[j + 1].isdigit():
                j += 1
                while j < n and src[j].isdigit():
                    j += 1
                toks.append(("NUMBER", float(src[i:j]), line))
            else:
                toks.append(("NUMBER", int(src[i:j]), line))
            i = j
        elif c == '"':
            j, buf = i + 1, []
            while True:
                if j >= n:
                    raise LexError(f"line {line}: unterminated string")
                if src[j] == "\n":
                    raise LexError(f"line {line}: unterminated string")
                if src[j] == "\\" and j + 1 < n:
                    buf.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(src[j + 1], src[j + 1]))
                    j += 2
                elif src[j] == '"':
                    break
                else:
                    buf.append(src[j]); j += 1
            toks.append(("STRING", "".join(buf), line)); i = j + 1
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            w = src[i:j]
            toks.append(("KEY" if w in KEYWORDS else "IDENT", w, line)); i = j
        elif src[i:i + 2] in TWO_CHAR:
            toks.append(("OP", src[i:i + 2], line)); i += 2
        elif c in SINGLE:
            toks.append(("OP", c, line)); i += 1
        else:
            raise LexError(f"line {line}: unexpected character {c!r}")
    toks.append(("EOF", "", line))
    return toks
