"""Phase 2 — 2-layer MLP for XOR (NumPy only)."""
import numpy as np

def sigmoid(z): return 1/(1+np.exp(-z))
def dsigmoid(a): return a*(1-a)

class MLP:
    def __init__(self, n_in=2, n_h=8, n_out=1, seed=0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, 1, (n_in, n_h)); self.b1 = np.zeros(n_h)
        self.W2 = rng.normal(0, 1, (n_h, n_out)); self.b2 = np.zeros(n_out)
    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1; self.a1 = sigmoid(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2; self.a2 = sigmoid(self.z2)
        return self.a2
    def step(self, X, Y, lr=0.5):
        m = X.shape[0]
        out = self.forward(X)
        dz2 = (out - Y) / m * dsigmoid(out)
        dW2 = self.a1.T @ dz2; db2 = dz2.sum(0)
        da1 = dz2 @ self.W2.T; dz1 = da1 * dsigmoid(self.a1)
        dW1 = X.T @ dz1; db1 = dz1.sum(0)
        for p, g in [(self.W2, dW2), (self.b2, db2), (self.W1, dW1), (self.b1, db1)]:
            p -= lr * g
        return float(np.mean((out - Y) ** 2))

def train_xor(epochs=5000, lr=0.5, seed=0):
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    Y = np.array([[0], [1], [1], [0]], float)
    net = MLP(seed=seed)
    for _ in range(epochs):
        loss = net.step(X, Y, lr)
    return net, loss
