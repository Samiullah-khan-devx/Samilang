"""Phases 11+12+13 — memory, tools, eval."""
import numpy as np, math, os

class ShortMemory:
    def __init__(self, n=10): self.n = n; self.hist = []
    def add(self, u, a): self.hist.append((u, a)); self.hist = self.hist[-self.n:]
    def context(self): return "\n".join(f"U:{u}\nA:{a}" for u, a in self.hist)

class LongMemory:
    def __init__(self, d=32): self.d = d; self.items = []
    def _emb(self, t):
        r = np.random.default_rng(abs(hash(t)) % 2**32); return r.normal(0, 1, self.d)
    def store(self, text): self.items.append((text, self._emb(text)))
    def recall(self, q, k=2):
        qv = self._emb(q)
        s = sorted(self.items, key=lambda it: float(qv @ it[1] / (np.linalg.norm(qv) * np.linalg.norm(it[1]) + 1e-9)), reverse=True)
        return [t for t, _ in s[:k]]

TOOLS = {}
def tool(name):
    def d(f): TOOLS[name] = f; return f
    return d
@tool("calculator")
def calc(expr: str) -> str:
    allowed = set("0123456789+-*/(). %")
    if any(c not in allowed for c in expr): return "blocked"
    try: return str(eval(expr, {"__builtins__": {}}))
    except Exception as e: return f"error: {e}"

BENCH = [("math", "2+2", "4"), ("factual", "capital of france?", "paris"), ("instruction", "repeat: hello", "hello")]
def benchmark(answer_fn):
    ok = sum(1 for _, q, a in BENCH if a in answer_fn(q).lower())
    return {"score": ok, "total": len(BENCH)}
