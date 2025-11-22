import argparse

from zac.optimizer import add


def main() -> None:
    parser = argparse.ArgumentParser(prog="zac", description="Zonal Architecture Compiler (ZAC) demo CLI")
    parser.add_argument("a", type=int, help="first integer")
    parser.add_argument("b", type=int, help="second integer")

    args = parser.parse_args()

    result = add(args.a, args.b)
    print(f"{args.a} + {args.b} = {result}")