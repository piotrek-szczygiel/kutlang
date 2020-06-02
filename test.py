from io import StringIO
import argparse
import sys
import os
from main import execute
from lang.scope import Scope
from colorama import Fore, Style, init
from pathlib import Path


def test(path, verbose=False):
    with open(path, "r") as f:
        _, source, expected = f.read().split("###", 2)
        expected = expected.strip()

        old_stdout = sys.stdout
        sys.stdout = actual = StringIO()

        opt = False
        if expected.startswith("OPTIMIZE"):
            opt = True
            expected = expected[8:].strip()

        lexer_output = expected.startswith("LEXER OUTPUT")
        execute(Scope(), source, draw=False, lexer_output=lexer_output, opt=opt)

        sys.stdout = old_stdout
        actual = actual.getvalue().strip()

        path = str(path)

        print(path + Fore.BLUE + "." * (40 - len(path)), end="")
        if actual == expected:
            print(Fore.GREEN + "PASS" + Style.RESET_ALL)
        else:
            print(Fore.RED + "FAIL" + Style.RESET_ALL)
            if verbose:
                print("=" * 10 + "Expected" + "=" * 10)
                print(Fore.GREEN + expected + Style.RESET_ALL)
                print("=" * 10 + " Actual " + "=" * 10)
                print(Fore.YELLOW + actual + Style.RESET_ALL)


if __name__ == "__main__":
    init()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-v",
        "--verbose",
        help="show actual and expected output in case of an error",
        action="store_true",
    )
    args = arg_parser.parse_args()

    tests_dir = Path("tests")
    (_, _, tests) = next(os.walk(tests_dir))
    for t in tests:
        test(tests_dir / t, verbose=args.verbose)
