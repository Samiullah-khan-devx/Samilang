"""SamiLang tree-walking interpreter: AST -> values."""

class SamiError(Exception):
    pass

class _Return(Exception):
    def __init__(self, value):
        self.value = value

class Func:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

class Env:
    def __init__(self, parent=None):
        self.vars, self.parent = {}, parent
    def get(self, name, line):
        e = self
        while e is not None:
            if name in e.vars:
                return e.vars[name]
            e = e.parent
        raise SamiError(f"line {line}: undefined variable {name!r}")
    def set(self, name, value):
        self.vars[name] = value

def _show(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, Func):
        return "<func>"
    return str(v)

def run(ast, out=None):
    import sys
    _exec(ast, Env(), out if out is not None else sys.stdout)

def _exec(node, env, out):
    kind = node[0]
    if kind == "block":
        for s in node[1]:
            _exec(s, env, out)
    elif kind == "print":
        out.write(_show(_eval(node[1], env, out)) + "\n")
    elif kind == "assign":
        env.set(node[1], _eval(node[2], env, out))
    elif kind == "if":
        (_, c, t, e, ln) = node
        branch = t if _eval(c, env, out) else e
        if branch is not None:
            _exec(branch, env, out)
    elif kind == "while":
        (_, c, b, ln) = node
        while _eval(c, env, out):
            _exec(b, env, out)
    elif kind == "for":
        (_, name, lo, hi, b, ln) = node
        a, z = int(_eval(lo, env, out)), int(_eval(hi, env, out))
        for i in range(a, z):
            env.set(name, i)
            _exec(b, env, out)
    elif kind == "func":
        (_, name, params, body, ln) = node
        env.set(name, Func(params, body, env))
    elif kind == "return":
        raise _Return(_eval(node[1], env, out))
    elif kind == "expr":
        _eval(node[1], env, out)
    else:
        raise SamiError(f"unknown statement {kind}")

def _eval(node, env, out):
    kind = node[0]
    if kind == "num" or kind == "str" or kind == "bool":
        return node[1]
    if kind == "var":
        return env.get(node[1], node[2])
    if kind == "unop":
        v = _eval(node[2], env, out)
        return (not v) if node[1] == "not" else -v
    if kind == "binop":
        op = node[1]
        l = _eval(node[2], env, out)
        if op == "and":
            return l and _eval(node[3], env, out)
        if op == "or":
            return l or _eval(node[3], env, out)
        r = _eval(node[3], env, out)
        try:
            if op == "+":
                return l + r
            if op == "-":
                return l - r
            if op == "*":
                return l * r
            if op == "/":
                return l / r
            if op == "%":
                return l % r
            if op == "==":
                return l == r
            if op == "!=":
                return l != r
            if op == "<":
                return l < r
            if op == "<=":
                return l <= r
            if op == ">":
                return l > r
            if op == ">=":
                return l >= r
        except TypeError:
            raise SamiError("cannot apply that operator to those values")
        raise SamiError(f"unknown operator {op}")
    if kind == "call":
        _, name, args, ln = node
        f = env.get(name, ln)
        if not isinstance(f, Func):
            raise SamiError(f"line {ln}: {name!r} is not a function")
        if len(args) != len(f.params):
            raise SamiError(f"line {ln}: {name} takes {len(f.params)} args, got {len(args)}")
        local = Env(f.env)
        for k, a in zip(f.params, args):
            local.set(k, _eval(a, env, out))
        try:
            _exec(f.body, local, out)
        except _Return as r:
            return r.value
        return 0
    raise SamiError(f"unknown expression {kind}")
