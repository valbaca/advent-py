# advent-py 🎄🐍

Advent of Code problems solved in Python

- [Advent of Code](https://adventofcode.com/)

## Install/Setup: (mise, venv, pip, pip-tools)

1. I recommend [mise](https://mise.jdx.dev/) to install Python >= 3.12
  - Install: `mise install python@<version>`
  - (Optional) Use a specific Python version within this project: `mise use python@<version>`
2. Once, within the project, create a venv: `python -m venv --prompt advent-pypy .venv`
3. Activate it each session: `source .venv/bin/activate`
4. Use [pip-tools](https://pip-tools.readthedocs.io/en/stable/) 
   1. `pip install pip-tools`
   2. `pip-compile`
   3. `pip-sync`

Alternative: manage your Python versions with [pyenv](https://github.com/pyenv/pyenv)  and your virtualenvs with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## Running

Simply run a day's file from within PyCharm.

OR

```shell
python -m advent.year<year>.day<day>
# such as:
python -m advent.year2024.day19
```

OR

```shell
# from the project root:
$ export PYTHONPATH=.
# then run the actual file
$ python advent/year2020/day1.py
<part 1 answer>
<part 2 answer>
```

Just simple scripts: Each day's script runs solo (no top-level runner) and reads input from a .txt file with the same prefix in the same directory. For example `day1.py` reads `day1.txt` from within the same directory.

### Running: VS Code

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

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
- Year 2016: 🎄 DONE! [advent/year2016](advent/year2016)
  - Days 8-18 in Java: [github.com/valbaca/advent](https://github.com/valbaca/advent)
- Year 2017: ❄️ On ice.
- Year 2018: ❄️ On ice.
- Year 2019: ❄️ On ice.
- Year 2020: 🎄 DONE! [advent/year2020](advent/year2020)
- Year 2021: 🎄 DONE! [advent/year2021](advent/year2021)
- Year 2022: 🎄 DONE in Kotlin [valbaca/advent-kt](https://github.com/valbaca/advent-kt)
- Year 2023: 🎁 IN PROGRESS 20/25 complete here: [advent/year2023](advent/year2023)
- Year 2024: 🎁 IN PROGRESS 23/25 complete here: [advent/year2024](advent/year2024)
