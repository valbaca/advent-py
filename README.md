# advent-py 🎄🐍

Advent of Code problems solved in Python

- [Advent of Code](https://adventofcode.com/)

## Install/Setup

Yes, Python package management is a mess. Here's what I use:

1. Install and setup Python 3.10. I prefer using [pyenv](https://github.com/pyenv/pyenv) to manage Python itself. I also prefer [PyPy](https://www.pypy.org/) as the actual Python runtime; it's just faster.
```shell
pyenv install pypy3.10-7.3.16 # for example
```

2. Setup and activate your python `virtualenv`. I prefer using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
```shell
pyenv virtualenv pypy3.10-7.3.16 advent-py
cd <this repo>
pyenv activate advent-py
```

3. Install [pip-tools](https://github.com/jazzband/pip-tools), which help manage dependencies through requirements.in (simple names) and requirements.txt (exact versions)
```shell
pip install pip-tools
pip-sync # pulls the specific versions specified in requirements.txt
```

### Add Dependencies

1. Update `requirements.in`
2. Run `pip-compile` (which comes from pip-tools, mentioned above)


## Running

```shell
# from the project root:
$ export PYTHONPATH=.
$ python advent/year2020/day1.py # or run open file from within VS Code
<part 1 answer>
<part 2 answer>
```

Just simple scripts: Each day's script runs solo (no top-level runner) and reads input from a .txt file with the same prefix in the same directory. For example `day1.py` reads `day1.txt` from within the same directory.

## What's interesting?

- What's Advent of Code?
  - See Advent of Code's ["About"](https://adventofcode.com/2021/about)
- Why Advent of Code?
  - It's fun! As opposed to grinding LeetCode, AoC has fun "flavor" and lets you solve however you want (any language or even none!). Lots of hidden easter eggs and nerdy references.
  - Non-prescriptive: you decide how you want to solve the problem: use whatever language, editor/IDE, debuggers, or libraries you want.
  - "Sneaky" concepts: I like how Advent questions are a bit subtle and uniquely challenging. What works for part 1 may not scale for part 2. Sometimes all it takes is some refactoring; other times a full rewrite might be necessary.
- [elf.py](advent/elf.py) - Santa's little helper! Where I put helper functions
  - For example, using `__file__` within a python script gives the script filename. Then, changing the `.py` to `.txt` makes it simple to put the input file next to the script
  - `septoi` (stands for "separate, to int") is an incredibly useful helper. By safely "trying" to convert to int, it keeps the "non-number" parts as strings and gives ints where possible. It also accepts a regex to split on, so it's adaptive and flexible. This is a tangible advantage of dynamic typing.
- Why Python?
  - I've used AoC to get more familiar with other languages (Go, Clojure) and it's been a fun and useful approach.
  - I'm now looking to get more familiar with Python
  - Python is the #1 language for Advent of Code, and for good reason IMO. Most problems are solved in less than 100 lines of python
  - Compare to other languages, Python has significant advantages:
    - Python emphasizes the developer's time, which for these problems is a more crucial resource vs execution time
    - vs Java: Python is succinct, direct, and operates on a higher level (and just more fun!)
    - vs Go, Crystal, or Clojure: Python has a better debugger (or has one at all!)
    - vs Go or Java: Python's `int` (and dynamic typing in-general) is nicer than strict typing
    - Python is the slowest language to execute, but that's still fast enough. A "correct" solution typically comes down to using the right algorithm or data structures.

## My Advent Progress

- Year 2015: 🎄 DONE! [advent/year2015](advent/year2015)
  - Also solved in Go [valbaca/advent-go](https://github.com/valbaca/advent-go) and Clojure [valbaca/advent](https://github.com/valbaca/advent)
- Year 2016: 🎄 DONE!
  - Days 1-19, 22-25 in Python here: [advent/year2016](advent/year2016)
  - Days 8-18 in Java: [github.com/valbaca/advent](https://github.com/valbaca/advent)
- Year 2017: ❄️ On ice.
- Year 2018: ❄️ On ice.
- Year 2019: ❄️ On ice.
- Year 2020: 🎄 DONE! [advent/year2020](advent/year2020)
- Year 2021: 🎄 DONE! [advent/year2021](advent/year2021)
- Year 2022: 🎄 DONE in Kotlin [valbaca/advent-kt](https://github.com/valbaca/advent-kt)
