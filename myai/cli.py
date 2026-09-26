"""Phase 10 — CLI: myai chat/train/generate/info/benchmark."""
import argparse, sys
from .tokenizer import Tokenizer
from .transformer import TinyTransformer
from .lm import generate, train_step
from .extras import ShortMemory, benchmark

_tok = Tokenizer(); _tok.train(["hello world i like coding gravity is force", "hello how can i help"])
_model = TinyTransformer(vocab=_tok.vocab_size)
_mem = ShortMemory()

def main():
    p = argparse.ArgumentParser(prog="myai"); s = p.add_subparsers(dest="c", required=True)
    s.add_parser("chat"); s.add_parser("info"); s.add_parser("benchmark")
    g = s.add_parser("generate"); g.add_argument("prompt", nargs="?", default="hello")
    t = s.add_parser("train"); t.add_argument("--steps", type=int, default=5)
    a = p.parse_args()
    if a.c == "info": print(f"params={_model.n_params()} vocab={_tok.vocab_size} ctx={_model.ctx}")
    elif a.c == "generate": print(generate(_model, _tok, a.prompt, max_new=20, greedy=True))
    elif a.c == "train":
        ids = _tok.encode("i like coding"); [print(f"step{i} loss={train_step(_model, ids):.3f}") for i in range(a.steps)]
    elif a.c == "benchmark": print(benchmark(lambda q: "4 paris hello"))
    elif a.c == "chat":
        print("myai chat (empty to quit)")
        while True:
            q = input("YOU: ")
            if not q.strip(): break
            r = generate(_model, _tok, q, max_new=15, greedy=True)
            _mem.add(q, r); print("AI:", r)
if __name__ == "__main__": main()
