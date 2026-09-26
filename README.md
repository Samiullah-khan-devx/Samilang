<div align="center">

# SamiLang

### Easy as Python. On the road to fast as C++.

A tiny programming language with its own lexer, parser, interpreter and
one-command Windows installer — plus a from-scratch NumPy AI lab
(MLP → tokenizer → transformer → CLI) living in the same repo.

[![Python](https://img.shields.io/badge/python-3.12%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-windows-lightgrey?style=flat-square&logo=windows)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![SamiLang](https://img.shields.io/badge/samilang-v0.1.0-orange?style=flat-square)](#)
[![CI](https://github.com/Samiullah-khan-devx/Samilang/actions/workflows/ci.yml/badge.svg)](https://github.com/Samiullah-khan-devx/Samilang/actions)

```text
$ samilang examples/collatz.sm
27
82
41
124
...
1
steps:
111
```

[Quickstart](#-quickstart) ·
[Language tour](#-language-tour) ·
[Examples](#-examples) ·
[Benchmarks](#-benchmarks) ·
[AI lab](#-bonus-myai--tiny-ai-from-scratch) ·
[Roadmap](#-roadmap)

</div>

---

## ✨ What is this?

| Pillar | What | Where |
|---|---|---|
| **SamiLang** | A real, runnable language: variables, strings, `if/else`, `while`, `for i in 0..5`, functions, recursion | `lang/` + `examples/` |
| **Installer** | One PowerShell script puts a `samilang` command on PATH (no admin) | `install-samilang.ps1` |
| **myai lab** | Neural nets from scratch in NumPy: XOR MLP, tokenizer, attention, tiny transformer, training loop, sampling CLI | `myai/` |
| **Quality gates** | Smoke tests assert exact program outputs; CI runs them + the TS build on every push | `tests/smoke.py`, `.github/workflows/ci.yml` |

## 🚀 Quickstart

```powershell
# One line, fresh PC to running programs (installs Python via winget if missing)
irm https://raw.githubusercontent.com/Samiullah-khan-devx/Samilang/main/install-pc.ps1 | iex
```

Or the manual way:

```powershell
# 1. Clone
git clone https://github.com/Samiullah-khan-devx/Samilang.git
cd samilang

# 2. Install the language (adds `samilang` to your user PATH)
powershell -ExecutionPolicy Bypass -File install-samilang.ps1

# 3. Open a NEW terminal and run
samilang --version            # samilang 0.1.0
samilang examples/hello.sm    # the full tour
samilang                      # REPL — type exit to quit
```

> No admin rights needed. The installer drops a shim in
> `%LOCALAPPDATA%\Programs\samilang` and appends it to your **user** PATH.

## 📖 Language tour

```python
print "hello world"

name = "sami"
print "hi " + name          # string concat

x = 10
print x + 5                 # 15

if x > 5 {
  print "big"
} else {
  print "small"
}

for i in 0..5 {
  print i * i               # 0 1 4 9 16
}

func fib(n) {
  if n < 2 {
    return n
  }
  return fib(n - 1) + fib(n - 2)
}
print fib(15)               # 610
```

**Cheat sheet**

| Feature | Syntax |
|---|---|
| Comment | `# like this` |
| Types | ints, floats, strings, `true` / `false` |
| Arithmetic | `+ - * / %`, comparisons `== != < <= > >=` |
| Logic | `and`, `or`, `not` |
| Loop | `for i in 0..5 { }` (inclusive–exclusive), `while cond { }` |
| Functions | `func name(a, b) { return a + b }` |
| Errors | `error: line 3: undefined variable 'x'` — always with a line number |

## 📦 Examples

| File | Demonstrates | Verified output |
|---|---|---|
| `examples/hello.sm` | Full tour: strings, math, branches, loops, recursion | `hello world … 610` |
| `examples/fizzbuzz.sm` | Nested `if/else`, `%` | `1 2 Fizz 4 Buzz … FizzBuzz` |
| `examples/primes.sm` | Functions returning booleans | `2 3 5 7 11 13 17 19 23 29` |
| `examples/collatz.sm` | `while`, reassignment | `27 … 1, steps: 111` |
| `examples/fib.sm` | Recursion speed check | `17711` in ~0.4 s |

```powershell
samilang examples/fizzbuzz.sm
samilang examples/primes.sm
```

## 📊 Benchmarks

Measured on this machine, not estimated:

| Test | Result |
|---|---|
| `fib(22)` in SamiLang | **~0.44 s** (tree-walking interpreter — Python-class speed) |
| XOR MLP (NumPy, 2000 epochs) | loss **0.019**, outputs `[0.11, 0.84, 0.86, 0.15]` |
| Tiny transformer forward | `(seq, vocab)` logits, **17,344 params** |
| `python tests/smoke.py` | **4 programs + Phase 1 checks, all green** |

> Honest note: v0.1 is an AST interpreter, so it won't beat C++.
> The lexer → parser → AST → interpreter split exists precisely so a
> bytecode compiler + VM can slot in later — that's the road to C++ speed.

## 🧠 Bonus: myai — tiny AI from scratch

The same repo contains a 15-phase build-your-own-AI project (NumPy only):

```powershell
python -m myai.phase1.check   # vectors, softmax, gradients, GD — must print Phase 1 OK
python -m myai.cli info       # params=17344 vocab=15 ctx=16
python -m myai.cli generate "hello"
python -m myai.cli train --steps 5
python -m myai.cli benchmark
```

MLP with real backprop (XOR) · word tokenizer with `encode/decode` ·
scaled dot-product + causal self-attention · 2-layer transformer ·
greedy / temperature / top-k / top-p sampling · short- + long-term
memory · sandboxed `calculator` tool · 3-task benchmark.

## 🗂️ Project structure

```text
samilang/
├── lang/                 # the language: lexer, parser, interpreter, CLI
├── examples/             # hello, fizzbuzz, primes, collatz, fib (.sm)
├── tests/smoke.py        # asserts exact outputs of every example
├── install-samilang.ps1  # one-command Windows installer (no admin)
├── requirements.txt      # numpy
├── myai/                 # from-scratch AI lab (NumPy)
│   ├── phase1/           # math: dot, matmul, softmax, gradients, GD
│   ├── phase2/           # MLP + backprop (XOR)
│   ├── tokenizer.py attention.py transformer.py
│   ├── lm.py             # training step + sampling/generation
│   ├── extras.py         # memory, tools, eval benchmark
│   └── cli.py            # myai chat/train/generate/info/benchmark
├── samilang/             # TypeScript host project (VS solution)
├── samilang.slnx         # Visual Studio solution (TS + Python)
└── .github/workflows/ci.yml
```

## 🗺️ Roadmap

- [x] v0.1 — lexer, parser, interpreter, installer, smoke tests
- [ ] Bytecode compiler + VM (the C++-speed milestone)
- [ ] `input()` builtin + string library (`len`, `split`)
- [ ] VS Code syntax highlighting for `.sm` files
- [ ] SamiLang self-hosting: write the lexer in SamiLang

## 🤝 Contributing & License

Issues and PRs welcome — run `python tests/smoke.py` before pushing.
MIT licensed, see [LICENSE](LICENSE).
