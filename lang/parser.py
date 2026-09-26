"""SamiLang parser: tokens -> AST. Grammar documented in README."""
from .lexer import lex, LexError

class ParseError(Exception):
    pass

class P:
    def __init__(self, toks):
        self.t, self.i = toks, 0
    def peek(self):
        return self.t[self.i]
    def next(self):
        tok = self.t[self.i]; self.i += 1
        return tok
    def expect(self, typ, val=None):
        tt, vv, ln = self.next()
        if tt != typ or (val is not None and vv != val):
            raise ParseError(f"line {ln}: expected {val or typ}, got {vv!r}")
        return vv

def parse(src):
    return _program(P(lex(src)))

def _program(p):
    stmts = []
    while p.peek()[0] != "EOF":
        if p.peek() == ("OP", ";", p.peek()[2]):
            p.next()
        else:
            stmts.append(_stmt(p))
    return ("block", stmts)

def _stmt(p):
    tt, vv, ln = p.peek()
    if (tt, vv) == ("KEY", "print"):
        p.next(); return ("print", _expr(p), ln)
    if (tt, vv) == ("KEY", "if"):
        p.next(); c = _expr(p); t = _block(p); e = None
        if p.peek()[0:2] == ("KEY", "else"):
            p.next(); e = _block(p)
        return ("if", c, t, e, ln)
    if (tt, vv) == ("KEY", "while"):
        p.next(); return ("while", _expr(p), _block(p), ln)
    if (tt, vv) == ("KEY", "for"):
        p.next()
        name = p.expect("IDENT")
        p.expect("KEY", "in")
        lo = _expr(p); p.expect("OP", ".."); hi = _expr(p)
        return ("for", name, lo, hi, _block(p), ln)
    if (tt, vv) == ("KEY", "func"):
        p.next(); name = p.expect("IDENT"); p.expect("OP", "(")
        params = []
        if p.peek()[0:2] != ("OP", ")"):
            params.append(p.expect("IDENT"))
            while p.peek()[0:2] == ("OP", ","):
                p.next(); params.append(p.expect("IDENT"))
        p.expect("OP", ")")
        return ("func", name, params, _block(p), ln)
    if (tt, vv) == ("KEY", "return"):
        p.next(); return ("return", _expr(p), ln)
    if tt == "IDENT" and p.t[p.i + 1][0:2] == ("OP", "="):
        p.next(); p.next()
        return ("assign", vv, _expr(p), ln)
    e = _expr(p)
    return ("expr", e, ln)

def _block(p):
    p.expect("OP", "{")
    stmts = []
    while p.peek()[0:2] != ("OP", "}"):
        stmts.append(_stmt(p))
    p.next()
    return ("block", stmts)

def _expr(p):
    return _or(p)

def _or(p):
    l = _and(p)
    while p.peek()[0:2] == ("KEY", "or"):
        p.next(); l = ("binop", "or", l, _and(p))
    return l

def _and(p):
    l = _cmp(p)
    while p.peek()[0:2] == ("KEY", "and"):
        p.next(); l = ("binop", "and", l, _cmp(p))
    return l

def _cmp(p):
    l = _add(p)
    if p.peek()[0] == "OP" and p.peek()[1] in ("==", "!=", "<", "<=", ">", ">="):
        op = p.next()[1]
        l = ("binop", op, l, _add(p))
    return l

def _add(p):
    l = _mul(p)
    while p.peek()[0] == "OP" and p.peek()[1] in ("+", "-"):
        op = p.next()[1]
        l = ("binop", op, l, _mul(p))
    return l

def _mul(p):
    l = _unary(p)
    while p.peek()[0] == "OP" and p.peek()[1] in ("*", "/", "%"):
        op = p.next()[1]
        l = ("binop", op, l, _unary(p))
    return l

def _unary(p):
    if p.peek()[0:2] == ("KEY", "not"):
        p.next(); return ("unop", "not", _unary(p))
    if p.peek()[0:2] == ("OP", "-"):
        p.next(); return ("unop", "-", _unary(p))
    return _primary(p)

def _primary(p):
    tt, vv, ln = p.next()
    if tt == "NUMBER":
        return ("num", vv)
    if tt == "STRING":
        return ("str", vv)
    if (tt, vv) in (("KEY", "true"), ("KEY", "false")):
        return ("bool", vv == "true")
    if tt == "IDENT":
        if p.peek()[0:2] == ("OP", "("):
            p.next(); args = []
            if p.peek()[0:2] != ("OP", ")"):
                args.append(_expr(p))
                while p.peek()[0:2] == ("OP", ","):
                    p.next(); args.append(_expr(p))
            p.expect("OP", ")")
            return ("call", vv, args, ln)
        return ("var", vv, ln)
    if (tt, vv) == ("OP", "("):
        e = _expr(p); p.expect("OP", ")")
        return e
    raise ParseError(f"line {ln}: unexpected {vv!r}")
