"""SamiLang command line: `samilang prog.sm`, `samilang -e "print 1+2"`, or REPL."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lang.parser import parse, ParseError
from lang.interp import run, SamiError
from lang.lexer import LexError

VERSION = "0.1.0"

def exec_src(src):
    run(parse(src))

def repl():
    buf = ""
    while True:
        try:
            line = input("... " if buf else ">>> ")
        except EOFError:
            print()
            break
        buf += line + "\n"
        if buf.strip() in ("exit", "quit"):
            break
        if buf.count("{") > buf.count("}"):
            continue
        try:
            exec_src(buf)
        except (SamiError, LexError, ParseError) as e:
            print(f"error: {e}")
        buf = ""

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv in ([], ["-i"]):
        print(f"samilang {VERSION} (type exit to quit)")
        repl()
        return 0
    if argv[0] in ("--version", "-v"):
        print(f"samilang {VERSION}")
        return 0
    if argv[0] == "-e":
        src = argv[1] if len(argv) > 1 else ""
    else:
        with open(argv[0], encoding="utf-8") as f:
            src = f.read()
    try:
        exec_src(src)
    except (SamiError, LexError, ParseError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
