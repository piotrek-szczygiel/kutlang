# calc-parser

## Installation

```bash
poetry install
```

## Usage

```bash
> poetry run python calc.py

> (1 + sin1.5) ** (cos(0) + ln2.7)
3.9714001717805405
```

```bash
> cat fib.txt

{
	def fib = {
		a = 1;
		b = 1;

		for (i = 0; i < n; i = i 1 +) {
			temp = a;
			a = a b +;
			b = temp;
			b
		}
	};

	n = 5;
	run fib;
}

> poetry run python rpn.py fib.txt
1
2
3
5
8
```
