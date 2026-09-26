"""Phase 1 checks — run after YOU implement exercises.py. Do not edit."""
import numpy as np
from .exercises import (
    dot_product, matmul, softmax,
    numerical_derivative, numerical_gradient,
    mse, gradient_descent_step,
)

assert dot_product(np.array([1., 2., 3.]), np.array([4., 5., 6.])) == 32.0
A = np.array([[1., 2., 3.], [4., 5., 6.]])
B = np.array([[1., 0.], [0., 1.], [1., 1.]])
assert np.allclose(matmul(A, B), A @ B)
s = softmax(np.array([1.0, 2.0, 3.0]))
assert abs(s.sum() - 1.0) < 1e-6 and np.argmax(s) == 2
assert abs(numerical_derivative(lambda x: x**2, 3.0) - 6.0) < 1e-3
assert np.allclose(numerical_gradient(lambda x: np.sum(x**2), np.array([1., 2., 3.])), [2., 4., 6.], atol=1e-3)
assert mse(np.array([2., 4.]), np.array([0., 0.])) == 10.0
assert gradient_descent_step(5.0, 2.0, 0.1) == 4.8
print("Phase 1 OK")
