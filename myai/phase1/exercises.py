"""Phase 1 — Mathematics exercises. Implement each TODO yourself with NumPy only."""
import numpy as np


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product: sum(a_i * b_i). Verify: dot([1,2,3],[4,5,6]) == 32."""
    return float(np.sum(a * b))


def matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Matrix multiply (m,k) @ (k,n) -> (m,n). Verify against np.matmul on 2x3 @ 3x2."""
    return A @ B


def softmax(logits: np.ndarray) -> np.ndarray:
    """Softmax to probabilities. Verify: sum == 1.0, max logit -> max prob."""
    e = np.exp(logits - np.max(logits))
    return e / np.sum(e)


def numerical_derivative(f, x: float, eps: float = 1e-5) -> float:
    """Central difference: (f(x+eps)-f(x-eps))/(2*eps). Verify on f(x)=x**2 at x=3 (~6.0)."""
    return (f(x + eps) - f(x - eps)) / (2 * eps)


def numerical_gradient(f, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """Gradient via finite differences. Verify on f(x)=sum(x**2) at [1,2,3] (~[2,4,6])."""
    g = np.zeros_like(x, dtype=float)
    for i in range(x.size):
        xp = x.astype(float).copy(); xp[i] += eps
        xm = x.astype(float).copy(); xm[i] -= eps
        g[i] = (f(xp) - f(xm)) / (2 * eps)
    return g


def mse(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """Mean squared error. Verify: mse([2,4],[0,0]) == 10.0."""
    return float(np.mean((y_pred - y_true) ** 2))


def gradient_descent_step(x: float, grad: float, lr: float) -> float:
    """One GD step: x - lr*grad. Verify: step(5, grad=2, lr=0.1) == 4.8."""
    return x - lr * grad
