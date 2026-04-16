import numpy as np

from data_processing import one_hot


def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0, z)


def relu_grad(z: np.ndarray) -> np.ndarray:
    return (z > 0).astype(np.float64)


def softmax(z: np.ndarray) -> np.ndarray:
    z_shifted = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)


def cross_entropy(probs: np.ndarray, y_one_hot: np.ndarray) -> float:
    eps = 1e-12
    return -np.mean(np.sum(y_one_hot * np.log(probs + eps), axis=1))


def accuracy_from_logits(logits: np.ndarray, y_true: np.ndarray) -> float:
    preds = np.argmax(logits, axis=1)
    return float(np.mean(preds == y_true))


class FNNBackprop:
    def __init__(self, input_size: int, hidden_size: int, output_size: int, seed: int = 42):
        rng = np.random.default_rng(seed)

        self.W1 = rng.normal(0, np.sqrt(2 / input_size), size=(input_size, hidden_size))
        self.b1 = np.zeros((1, hidden_size), dtype=np.float64)
        self.W2 = rng.normal(0, np.sqrt(2 / hidden_size), size=(hidden_size, output_size))
        self.b2 = np.zeros((1, output_size), dtype=np.float64)

    def forward(self, X: np.ndarray):
        z1 = X @ self.W1 + self.b1
        a1 = relu(z1)
        z2 = a1 @ self.W2 + self.b2
        probs = softmax(z2)
        cache = (X, z1, a1, z2, probs)
        return probs, z2, cache

    def backward(self, cache, y_one_hot: np.ndarray):
        X, z1, a1, _, probs = cache
        m = X.shape[0]

        dz2 = (probs - y_one_hot) / m
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        da1 = dz2 @ self.W2.T
        dz1 = da1 * relu_grad(z1)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        return dW1, db1, dW2, db2

    def step(self, grads, lr: float):
        dW1, db1, dW2, db2 = grads
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 300, lr: float = 0.05):
        y_one_hot = one_hot(y, self.b2.shape[1])

        for epoch in range(epochs):
            probs, logits, cache = self.forward(X)
            loss = cross_entropy(probs, y_one_hot)
            grads = self.backward(cache, y_one_hot)
            self.step(grads, lr)

            if epoch % max(1, epochs // 10) == 0 or epoch == epochs - 1:
                acc = accuracy_from_logits(logits, y)
                print(f"[Backprop] Epoch {epoch:4d} | loss={loss:.4f} | acc={acc:.4f}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        _, logits, _ = self.forward(X)
        return np.argmax(logits, axis=1)


class FNNNumericalGrad:
    """
    Baseline FNN trained with finite-difference gradients.
    This is educational and much slower than backpropagation.
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int, seed: int = 42):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, np.sqrt(2 / input_size), size=(input_size, hidden_size))
        self.b1 = np.zeros((1, hidden_size), dtype=np.float64)
        self.W2 = rng.normal(0, np.sqrt(2 / hidden_size), size=(hidden_size, output_size))
        self.b2 = np.zeros((1, output_size), dtype=np.float64)

    def forward(self, X: np.ndarray):
        z1 = X @ self.W1 + self.b1
        a1 = relu(z1)
        z2 = a1 @ self.W2 + self.b2
        probs = softmax(z2)
        return probs, z2

    def loss(self, X: np.ndarray, y: np.ndarray) -> float:
        probs, _ = self.forward(X)
        y_one_hot = one_hot(y, self.b2.shape[1])
        return cross_entropy(probs, y_one_hot)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 20, lr: float = 0.05, epsilon: float = 1e-4):
        params = [self.W1, self.b1, self.W2, self.b2]

        for epoch in range(epochs):
            grads = [np.zeros_like(p) for p in params]

            for p_idx, param in enumerate(params):
                it = np.nditer(param, flags=["multi_index"], op_flags=[["readwrite"]])
                while not it.finished:
                    idx = it.multi_index
                    original = param[idx]

                    param[idx] = original + epsilon
                    loss_plus = self.loss(X, y)

                    param[idx] = original - epsilon
                    loss_minus = self.loss(X, y)

                    param[idx] = original
                    grads[p_idx][idx] = (loss_plus - loss_minus) / (2 * epsilon)

                    it.iternext()

            for p, g in zip(params, grads):
                p -= lr * g

            probs, logits = self.forward(X)
            current_loss = cross_entropy(probs, one_hot(y, self.b2.shape[1]))
            acc = accuracy_from_logits(logits, y)
            print(f"[Numeric ] Epoch {epoch:4d} | loss={current_loss:.4f} | acc={acc:.4f}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        _, logits = self.forward(X)
        return np.argmax(logits, axis=1)
