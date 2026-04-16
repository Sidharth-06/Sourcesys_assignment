import argparse
from pathlib import Path

import numpy as np

from data_processing import prepare_data
from fnn_models import FNNBackprop, FNNNumericalGrad


def evaluate(model, X_test: np.ndarray, y_test: np.ndarray, model_name: str):
    preds = model.predict(X_test)
    acc = np.mean(preds == y_test)
    print(f"{model_name} Test Accuracy: {acc:.4f}")


def build_arg_parser():
    parser = argparse.ArgumentParser(description="NumPy FNN classification (numeric grad vs backprop)")
    parser.add_argument("--data", type=str, default="python_programs/data/iris.csv", help="Path to CSV dataset")
    parser.add_argument("--delimiter", type=str, default=",", help="CSV delimiter")
    parser.add_argument("--target-col", type=int, default=-1, help="Target column index")
    parser.add_argument("--has-header", action="store_true", help="Use when CSV has a header row")
    parser.add_argument("--hidden-size", type=int, default=16, help="Hidden layer size")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--skip-numeric", action="store_true", help="Skip numerical-gradient baseline")
    return parser


def main():
    args = build_arg_parser().parse_args()

    X_train, X_test, y_train, y_test, classes = prepare_data(
        data_path=Path(args.data),
        delimiter=args.delimiter,
        target_col=args.target_col,
        has_header=args.has_header,
        seed=args.seed,
    )

    input_size = X_train.shape[1]
    output_size = len(classes)

    print(f"Loaded dataset: {args.data}")
    print(f"Train shape: X={X_train.shape}, y={y_train.shape}")
    print(f"Test shape : X={X_test.shape}, y={y_test.shape}")
    print(f"Classes: {list(classes)}")

    if not args.skip_numeric:
        numeric_model = FNNNumericalGrad(
            input_size=input_size,
            hidden_size=min(args.hidden_size, 8),
            output_size=output_size,
            seed=args.seed,
        )
        numeric_model.train(X_train, y_train, epochs=8, lr=0.08)
        evaluate(numeric_model, X_test, y_test, "Numeric-Gradient FNN")
        print()

    backprop_model = FNNBackprop(
        input_size=input_size,
        hidden_size=args.hidden_size,
        output_size=output_size,
        seed=args.seed,
    )
    backprop_model.train(X_train, y_train, epochs=250, lr=0.05)
    evaluate(backprop_model, X_test, y_test, "Backprop FNN")


if __name__ == "__main__":
    main()
