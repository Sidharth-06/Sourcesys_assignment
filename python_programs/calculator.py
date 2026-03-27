"""A small command-line calculator."""

from __future__ import annotations

import argparse


def calculate(left: float, right: float, operator: str) -> float:
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ValueError("division by zero is not allowed")
        return left / right
    raise ValueError(f"unsupported operator: {operator}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate a basic arithmetic expression.")
    parser.add_argument("left", type=float, help="Left-hand operand")
    parser.add_argument("operator", choices=["+", "-", "*", "/"], help="Arithmetic operator")
    parser.add_argument("right", type=float, help="Right-hand operand")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = calculate(args.left, args.right, args.operator)
    print(f"{args.left:g} {args.operator} {args.right:g} = {result:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
